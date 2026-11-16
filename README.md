# Vanilla Together

A Fabric modpack for Minecraft 26.3 that keeps vanilla terrain and adds no new
content: performance, interface, maps, land claims and proximity voice chat.
Two packs come out of one list:

- **Vanilla Together** (`vanilla-together-<version>.mrpack`): every mod in `mods.toml`.
  It doubles as the server pack, because a server installs only the files
  that are not client-only.
- **Vanilla Together Essential** (`vanilla-together-essential-<version>.mrpack`): what a
  player needs to join a Vanilla Together server and talk, plus the performance mods.

Both import into the Modrinth App and Prism Launcher.

## Using it

Two files serve three uses. Every file in a pack is marked client-only,
server-only or both, and launchers and server installers read those marks,
so one file can be the player pack and the server pack at once.

| Use | File | How |
|---|---|---|
| Player, full | `vanilla-together-<version>.mrpack` | Modrinth App: install from the project page. Prism Launcher: Add Instance, Import, pick the file. |
| Player, lite | `vanilla-together-essential-<version>.mrpack` | The same way. Joins any Vanilla Together server. |
| Server | `vanilla-together-<version>.mrpack` | `itzg/minecraft-server` with `TYPE=MODRINTH`, or any tool that installs a server from an `.mrpack`. It installs Fabric and only the server and shared mods. |

There is no zip of mod jars. An `.mrpack` holds only download links and
hashes from Modrinth, so it can be shared freely; a zip would redistribute
mods whose licenses may not allow that.

### Known issues

- **e4mc and Krypton crash the game together.** Both change the same
  encryption call at login, and the game stops at startup with a Krypton
  mixin error. The packs do not contain e4mc; if you add it to your own
  instance, disable Krypton there. A player does not need Krypton to join.
- **Crash Assistant** (full pack) opens a "game crashed" window whenever the
  game ends abnormally, also when it is killed rather than closed.

## Building

    ./build.py            # from lock.json, the same pack every time
    ./build.py --update   # newest Fabric 26.3 version of every mod

`build.py` needs Python 3.11 and nothing else. Edit `mods.toml` to add or
drop a mod (`packs = ["full"]` or `["full", "essential"]`), run it, and
commit `mods.toml` with `lock.json`. Required libraries are added by
themselves. Files in `overrides/<pack>/` land in that pack's overrides.
`dist/` is not committed.

`build.py --update` takes each mod's newest version on its own and does not
check the version ranges mods require of each other, so start both packs
once in a launcher before a release. When a newest version needs something
the pack does not ship, pin the older one with `version = "..."` in
`mods.toml`, with a note on why.

## Running a server

With the `itzg/minecraft-server` image: `TYPE=MODRINTH` and
`MODRINTH_MODPACK=/data/packs/vanilla-together-<version>.mrpack`. Simple Voice
Chat needs UDP 24454 open next to the game port.

## License

MIT for the build script, the mod list and the texts (`LICENSE`). Every mod
keeps its own license; the packs only link to the files on Modrinth.
