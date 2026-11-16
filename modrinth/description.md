# Vanilla Together

Vanilla Minecraft, just smoother. Vanilla Together is a Fabric pack for Minecraft 26.3 that keeps the game as Mojang made it: vanilla terrain, no new blocks, items or mobs. What it adds is performance, a better interface, maps, land claims and proximity voice chat, for playing together on a small server.

## 📦 Which pack?

- **Vanilla Together**: everything. The right choice for most computers.
- **Vanilla Together Essential**: only what you need to join a Vanilla Together server and talk, plus the performance mods. For slow machines, or if you'd rather add your own client mods.

Both packs join the same server, and you can switch at any time.

## 💻 Installing

**Modrinth App:** click `Install` on the version you want.

**Prism Launcher:** Add Instance, then Import, and pick the downloaded `.mrpack` file or paste the version's Modrinth link.

The launcher sets up Java and Fabric by itself.

## 🖥️ Running a server

The full pack is also the server pack. Every file carries its side, so a server installs only the server and shared mods and skips the client-only ones. With the `itzg/minecraft-server` image that is `TYPE=MODRINTH` with `MODRINTH_MODPACK` pointing at the `.mrpack`. Voice chat needs UDP port 24454 open on the server next to the game port.

## 🎙️ Voice chat

**Simple Voice Chat** is in both packs and works by proximity: you hear the players near you.

- On first start a setup assistant walks you through microphone, speakers, and push to talk or voice activation.
- Push to talk has no default key. Set one in the assistant, or later under Controls in the Voice Chat category.
- `V` opens the voice chat menu, with the settings and the microphone test.
- `M` mutes your microphone, `N` turns voice chat off, `H` hides the icons.

## 🛡️ Land claims

**Open Parties and Claims** runs on the server, so players install nothing and everything works through chat commands:

- `/oclaims claim` claims the chunk you stand in, and `/oclaims unclaim` releases it.
- `/oparties create` starts a party, and `/oparties member invite <player>` invites someone, who accepts with a click in chat.

Members of your party may build on your claims.

## 🧩 What's inside

- **Performance:** Sodium, Lithium, FerriteCore, ModernFix, Krypton, ImmediatelyFast, Entity Culling, More Culling and Dynamic FPS. All of them are in Essential too.
- **Interface:** Jade, AppleSkin, Roughly Enough Items, Inventory Profiles Next, Mouse Tweaks, Shulker Box Tooltip, Better Advancements, Chat Heads and Mod Menu.
- **Maps:** Xaero's Minimap and Xaero's World Map.
- **Looks and sound:** Iris Shaders, Continuity, BetterGrassify, LambDynamicLights, Sound Physics Remastered, AmbientSounds and a few resource pack helpers.
- **Comfort:** No Chat Reports, Ping Wheel, controller support and Crash Assistant.
- **Server only:** Open Parties and Claims, Ledger, Chunky, spark and the server-side optimizers.

68 mods in all, not counting libraries. The source repository holds the full list and the script that builds both packs.
