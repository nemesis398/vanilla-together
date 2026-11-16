#!/usr/bin/env python3
"""Build the Vanilla Together packs as Modrinth .mrpack files from mods.toml.

  ./build.py            build from lock.json (resolve only what is missing)
  ./build.py --update   resolve every mod to its newest 26.3 Fabric version

For each mod in mods.toml it takes the newest Modrinth version for the pack's
Minecraft version and the Fabric loader (a release if one exists, otherwise
the newest beta or alpha), adds its required dependencies with the same packs,
and pins the result in lock.json, so a rebuild without --update is the same
pack. It writes dist/vanilla-together-<version>.mrpack ("full") and
dist/vanilla-together-essential-<version>.mrpack.

The env of each file follows the mod's side: a server-only mod is
"unsupported" on the client and the other way round, so Prism and the Modrinth
App skip server mods and the server (itzg TYPE=MODRINTH) skips client mods.
Standard library only; the Modrinth API needs no key.
"""
import hashlib
import json
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = "https://api.modrinth.com/v2"
UA = {"User-Agent": "vanilla-together-pack-builder/1.0"}
RANK = {"release": 0, "beta": 1, "alpha": 2}


def get(path, **params):
    q = "?" + urllib.parse.urlencode({k: json.dumps(v) if isinstance(v, list) else v for k, v in params.items()}) if params else ""
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + path + q, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(10)
                continue
            raise
    raise RuntimeError("unreachable")


def side_of(project):
    c, s = project["client_side"], project["server_side"]
    if s == "unsupported":
        return "client"
    if c == "unsupported":
        return "server"
    if c == "required" and s != "required":
        return "client"
    if s == "required" and c != "required":
        return "server"
    return "both"


def resolve(slug, cfg):
    versions = get(f"/project/{slug}/version", loaders=["fabric"], game_versions=[cfg["minecraft"]])
    if not versions:
        sys.exit(f"STOP: {slug} has no Fabric {cfg['minecraft']} version on Modrinth")
    # the newest version within the best channel available
    best = min(RANK.get(x["version_type"], 3) for x in versions)
    v = max((x for x in versions if RANK.get(x["version_type"], 3) == best), key=lambda x: x["date_published"])
    f = next((x for x in v["files"] if x["primary"]), v["files"][0])
    return {
        "project_id": v["project_id"],
        "version_id": v["id"],
        "version_number": v["version_number"],
        "version_type": v["version_type"],
        "filename": f["filename"],
        "url": f["url"],
        "size": f["size"],
        "sha1": f["hashes"]["sha1"],
        "sha512": f["hashes"]["sha512"],
        "requires": [d["project_id"] for d in v["dependencies"] if d["dependency_type"] == "required" and d.get("project_id")],
    }


def main():
    update = "--update" in sys.argv
    spec = tomllib.loads((ROOT / "mods.toml").read_text())
    cfg = spec["pack"]
    lock_path = ROOT / "lock.json"
    lock = {} if update or not lock_path.exists() else json.loads(lock_path.read_text())

    want = {}  # slug -> {"side", "packs", "name", "library"}
    for m in spec["mod"]:
        want[m["slug"]] = {"side": m["side"], "packs": set(m["packs"]), "name": m["name"], "library": False}

    by_id = {}      # project id -> slug, or None for a dependency Fabric never loads
    queue = list(want)
    while queue:
        slug = queue.pop(0)
        if slug not in lock:
            lock[slug] = resolve(slug, cfg)
            time.sleep(0.25)
        entry = lock[slug]
        by_id[entry["project_id"]] = slug
        for pid in entry["requires"]:
            if pid not in by_id:
                proj = get(f"/project/{pid}")
                if "fabric" not in proj["loaders"]:
                    # some multi-loader mods list their Forge-only libraries
                    # as required for every loader; Fabric never loads them
                    print(f"skip {proj['slug']}: required by {slug}, but has no Fabric build")
                    by_id[pid] = None
                    continue
                by_id[pid] = proj["slug"]
                if proj["slug"] not in want:
                    want[proj["slug"]] = {"side": side_of(proj), "packs": set(), "name": proj["title"], "library": True}
                    queue.append(proj["slug"])
            dep = by_id[pid]
            if dep is None:
                continue
            # a library inherits every pack of every mod that needs it
            before = set(want[dep]["packs"])
            want[dep]["packs"] |= want[slug]["packs"]
            if want[dep]["packs"] != before and dep not in queue:
                queue.append(dep)

    lock = {k: lock[k] for k in sorted(want)}
    lock_path.write_text(json.dumps(lock, indent=1, sort_keys=True) + "\n")

    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for pack, fname, title in (("full", f"vanilla-together-{cfg['version']}.mrpack", cfg["name"]),
                               ("essential", f"vanilla-together-essential-{cfg['version']}.mrpack", cfg["name"] + " Essential")):
        files = []
        for slug in sorted(want):
            w, e = want[slug], lock[slug]
            if pack not in w["packs"]:
                continue
            files.append({
                "path": f"mods/{e['filename']}",
                "hashes": {"sha1": e["sha1"], "sha512": e["sha512"]},
                "env": {"client": "unsupported" if w["side"] == "server" else "required",
                        "server": "unsupported" if w["side"] == "client" else "required"},
                "downloads": [e["url"]],
                "fileSize": e["size"],
            })
        index = {
            "formatVersion": 1, "game": "minecraft", "versionId": cfg["version"], "name": title,
            "summary": cfg["summary"], "files": files,
            "dependencies": {"minecraft": cfg["minecraft"], "fabric-loader": cfg["fabric_loader"]},
        }
        with zipfile.ZipFile(out / fname, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("modrinth.index.json", json.dumps(index, indent=1))
            ov = ROOT / "overrides" / pack
            if ov.is_dir():
                for p in sorted(ov.rglob("*")):
                    if p.is_file():
                        z.write(p, "overrides/" + str(p.relative_to(ov)))
        n_srv = sum(1 for f in files if f["env"]["server"] == "required")
        n_cli = sum(1 for f in files if f["env"]["client"] == "required")
        print(f"{fname}: {len(files)} files ({n_cli} client, {n_srv} server)")
    nonrelease = sorted(f"{s} ({lock[s]['version_type']})" for s in want if lock[s]["version_type"] != "release")
    print("not a release:", ", ".join(nonrelease) or "none")


if __name__ == "__main__":
    main()
