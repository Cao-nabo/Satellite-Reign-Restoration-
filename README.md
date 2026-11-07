# Satellite Reign — SR Restoration Mod (Community Release)

An unofficial mod for *Satellite Reign* (Steam, Windows build via Proton or native Windows) that restores and extends several systems, built from decompiled/recompiled game source plus additive plugins. This release intentionally does **not** include an experimental new-area/underground-room feature that's still in development — everything here has been installed and gameplay-tested.

## What's in this release

- **`Assembly-CSharp.dll`** — a replacement for the game's core compiled assembly. Contains the gameplay-level changes below.
- **`Mods/SRRestoration.dll`** — additive plugin: settings panel, camera monitoring, agent behavior policies, taxi service, billboards, bench/appearance systems.
- **`Mods/SRObjectivePreflight.dll`** — optional, read-only diagnostic plugin. Does not alter gameplay or saves; only checks for ID/terminal conflicts before you'd inject a custom objective. Safe to leave out if you don't need it.
- **`Mods/RestorationBillboards/`** — media assets for the animated billboard feature (required alongside `SRRestoration.dll` for billboards to work).
- **`tools/prepare_billboard_gif.py`** — converts your own GIFs into the format billboards use (see "Adding your own GIFs" below).

## Features confirmed working in gameplay

- **Repair drones**: physical repair-drone travel/arrival, repair-wheel completion (~180s), randomized loss replacement, and a per-area drone cap. See "Repair drones & camera maintenance" below for what hacking/destroying a drone actually does.
- **Camera hijack & C4**: hijack hold, paid satchel mounting, and remote detonation.
- **Combat**: idle/holstered agents going to cover and returning fire automatically when hit.
- **Bench sitting**: manual and automatic seating, movement priority, and portrait/HUD seating controls.
- **Vending machine beverage purchase**: order a drink from a nearby native vending machine via the portrait HUD.
- **Clothing/appearance**: individual clothing-piece customization (not just whole-outfit swaps).
- **Billboards**: custom GIF media playing on in-world ad displays (coverage is limited — see below).
- **Taxi service**: squad taxi calling and route travel.
- **Settings/monitoring panel**: in-game panel (F7) for maintenance timing presets, camera-repair monitoring, and agent behavior policies.

## Controls

| Key | Does what |
|---|---|
| **F7** | Open/close the settings panel (maintenance presets, camera monitoring, agent behavior policies, and the Billboard Library). |
| **Shift+C** | Toggle camera-repair monitoring for your current district. |
| **Shift+D** | Show a one-off status popup for nearby camera maintenance. |
| **P** or **Pause** | Toggle tactical pause (on by default; can be turned off in-game). |
| **F11** | "Unstuck" — recovers selected agent(s) to nearby open ground if they're stuck. Not usable in combat, downed, or mid-vehicle-transition. |
| **` (backquote/tilde)** | With one agent selected and your cursor over a parked car: board it. Over your own car: request exit. If you have a taxi booked and waiting, this boards it instead. |
| **Backslash** | With your squad selected near a free bench: sit. |

A chair icon also appears next to an agent's portrait when a bench is usable: **left-click** it to target a specific bench (double-tap to send them running instead of walking), or **right-click** it to sit at the nearest free seat automatically (double-right-click to run there). **Escape** or right-click cancels targeting once it's active.

## Repair drones & camera maintenance

This doesn't add any new controls — it uses the game's existing hack and combat actions, but now those actions actually *do* something against repair drones, which previously just auto-repaired cameras on a timer with no way to interfere:

- **Hack a repair drone** (same native hijack action you'd use on any hackable unit) to hold its repair job in limbo — the camera stays unrepaired for as long as you hold the hijack.
- **Destroy a repair drone** (shoot it down, same as any hostile) and its job is held, then a replacement drone gets dispatched after a delay rather than instantly — destroying one meaningfully buys time, it doesn't just cost the drone a trip.
- Camera repairs take about 180 seconds once a drone arrives, plus travel time. Loss replacement (if a drone itself is lost) samples a 120–240 second wait before a new one is eligible, plus travel. These timings, along with per-owner drone pool caps, are adjustable in the **F7** settings panel.

## Using the vending machine

A cup icon appears next to an agent's portrait when a compatible native beverage machine is within range (holstered, calm, locally-controlled agent, same level, within 15 metres). Hover the icon to preview the native price, then click to send the agent to buy a drink — they'll walk over and the purchase completes automatically. **Escape** or right-click cancels targeting before they arrive; normal movement orders or a sudden threat will also cancel an unfinished purchase. This is single-player only, and doesn't grant any stat bonus — it's a cosmetic/flavor interaction, not a buff.

## Using the taxi service

Open the settings panel (**F7**) and use the taxi option to open the Taxi panel.

- **Pickup is not limited to fixed taxi stands.** Call a taxi from wherever your agent currently is — the game finds the nearest reachable curb/street to your actual position. If you get "No short, reachable pickup on this street," move a little closer to an actual road.
- Press **Call taxi**. It drives to the pickup point near you; board when it arrives (walk up, or use the **`** key described above).
- **The whole squad can ride together** — up to 4 agents. Select multiple agents before calling, or have each one walk up and board individually once the cab arrives; they'll all be picked up as a team (boarding waits for everyone before the taxi leaves).
- Once seated, **destinations are landmark-based** — cycle through known city locations (plus any unlocked relay-beacon landmarks) with the `<`/`>` buttons, then press **Travel**. A flat fare (25, or 75 for the luxury car) is charged once travel starts.
- **Safe exit** / **Cancel booking** are available if you change your mind or need to bail early.

## Using agent behavior policies

Select one or more of your agents, open the settings panel (**F7**), then click **Agent behavior**. This opens a per-agent list with three choices:

- **Follow global return fire** — use whatever the global return-fire setting is (the default).
- **Allow automatic retaliation** — this agent automatically returns fire even if the global setting has it off.
- **Disable added retaliation** — this agent never auto-retaliates, even if the global setting has it on.

This only affects the mod's *added* auto-retaliation behavior — it doesn't touch manual attack commands, current orders, or any other native combat logic. Per-agent overrides reset when you load a save; everyone goes back to following the global setting until you set overrides again.

## Using appearance & clothing customization

This doesn't have its own menu — it extends the game's existing **Customize** screen (the one you already use to set an agent's or clone's appearance). Open Customize normally, and you'll see a new **"Colors / outfit"** button that toggles between the native outfit view and the mod's **"Clothing (Beta)"** view, which lets you set individual clothing pieces and colors instead of only swapping whole outfits.

In the Clothing (Beta) view:

- **Extra pieces** — toggles a view for accessory/extra clothing layers.
- **Saved looks (10)** — browse and apply up to 10 saved outfit slots; `<`/`>` cycle between them.
- **Apply** — commits your current draft changes to the agent, in place (no need to leave the screen).
- **Reset pieces** — reverts to the class's default clothing pieces.
- **Revert draft** — undoes your unsaved changes back to the agent's last applied look.
- **Preview controls**: scroll the mouse wheel over the preview (or use the **+**/**−** buttons) to zoom, **▲**/**▼** buttons to pan up/down, left-click-drag to rotate the model, and right-click-drag to pan freely (including diagonally).

## Billboard screen coverage — this is limited, read before expecting it everywhere

Billboards do **not** work on every poster/screen in the city. The code matches two *specific* existing in-world prop types by their exact name, material, and mesh signature — it isn't a generic "any ad surface" system. The two known-working types are:

- A specific pink fashion display on **Internecion Street** (The Grid district).
- **Downtown** top-lit posters (the horizontal 4×2 poster prop, several ad variants).

If you stand somewhere without one of these nearby, the Billboard Library will tell you "No compatible display nearby" and suggest trying one of those two spots. Whether either prop type is reused elsewhere in the city (other instances of the same poster piece in other districts) hasn't been exhaustively mapped — if you find more working screens elsewhere, that's genuinely useful to report back.

## Optional: busier city (higher pedestrian cap)

By default this release behaves like the base game's normal pedestrian density. There's a gameplay-confirmed option to raise the walker cap to at least 45 (from the native cap of 30) for a busier-feeling city — more pedestrians and traffic observed in testing, no crash markers. It doesn't change spawn cadence or any other population settings, just the cap.

To enable it, add `-sr-crowd-cap-45` to the game's Steam Launch Options (right-click Satellite Reign → Properties → General → Launch Options). No measured FPS impact was established either way — it's purely a density preference, not a performance feature.

## Known limitations — please read before installing

- **A native memory-related crash has been observed and is not fully root-caused.** It is not reliably reproducible, but if you experience a crash, please note what you were doing and report it.
- Combat behavior regression testing (stopped/already-covered agents, other agent classes, suppression, reload, repeated save/reload) is not exhaustive.
- Maintenance-state persistence across saves is not fully verified in every case.
- This is built against the **Windows build run through Proton or natively on Windows** — it has not been tested against the native Linux build.
- **No custom missions/quests are included in this release.** The codebase has an experimental reusable-mission system and a "Street Relay Sweep" objective, but both require undocumented launch flags to even activate, and the Street Relay content's own development notes record that full completion and save/reload were never actually verified by gameplay (the person testing it ran out of time before finishing). Deliberately left out rather than shipping something unfinished.

## Installation

**Back up your existing files first.** This mod replaces a core game file; if anything goes wrong, you'll want your originals back.

1. Close Satellite Reign completely (including Steam's background processes for it).
2. Locate your game's install folder (Steam → right-click Satellite Reign → Manage → Browse local files).
3. **Back up** `SatelliteReignWindows_Data/Managed/Assembly-CSharp.dll` to a safe location outside the game folder.
4. Copy this release's `Assembly-CSharp.dll` into `SatelliteReignWindows_Data/Managed/`, replacing the original.
5. Copy the `Mods/` folder from this release into the game's root install folder (next to `SatelliteReignWindows.exe`), merging with any existing `Mods/` folder you may have.
6. Launch the game normally.

## Adding your own GIFs to billboards

In-world ad screens play GIFs from `Mods/RestorationBillboards/<category>/<clip-name>/`, where `<category>` is `movies`, `merchandise`, or `commercial`. This release includes `tools/prepare_billboard_gif.py`, a converter that turns a GIF into the format the game reads — you can't just drop a raw `.gif` in; it has to be converted first.

**Requirements:** Python 3, with the Pillow library installed (`pip install pillow`).

**Usage:**
```
python3 tools/prepare_billboard_gif.py path/to/your.gif Mods/RestorationBillboards/movies/my-clip-name --category movies
```

- The output folder name (`my-clip-name` above) is just a label — pick anything.
- `--category` must match the folder you put it under: `movies`, `merchandise`, or `commercial`.
- The tool refuses to overwrite an existing output folder — use a new name for each clip.
- In game, press **F7** to open the settings panel, then open the Billboard Library from there. Use **Find nearest screen** to target a nearby ad display, the **`>`** button to cycle to your category, then **Enable / update screen**. New clips you've added are picked up automatically — no restart needed, just reopen the panel. **Restore screen** / **Restore all** puts the original ad back.

**Limits (the converter will reject anything outside these):**
- Input must be an actual `.gif` file, at most 32 MiB.
- At most 4 megapixels (e.g. 2048×2048) per frame.
- At most 1000 frames in the source GIF.
- Total loop duration at most 2 minutes.
- Add `--frames 16` (instead of the default 64) if you want to force the older, lower-detail atlas style used by the original preview clips.

## Uninstalling / reverting

1. Close the game.
2. Delete the `Mods/` folder contents you added (or the whole folder, if you had nothing else there).
3. Restore your backed-up original `Assembly-CSharp.dll` over the modded one.

## Notes

- Steam may silently overwrite `Assembly-CSharp.dll` on the next game update, which will disable the mod's gameplay changes until you reapply it. The `Mods/` plugins are unaffected by game updates since they load alongside the original files.
- This release does not include or depend on any new playable area/district — that work is still in progress and deliberately excluded here.
