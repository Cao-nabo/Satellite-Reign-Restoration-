# SR Restoration + Underground Black Market

Combined single-player mod for the Windows 32-bit Unity 5.3.5p4 build of Satellite Reign. Includes the existing restoration systems and the underground market. Linux/Proton is the tested environment; native Windows validation is pending.

## Install

Close the target game. Extract this release outside the game folder. With Python 3.9 or newer:

    python install.py --game "PATH/TO/SatelliteReign" --check
    python install.py --game "PATH/TO/SatelliteReign"

The installer accepts the certified vanilla core or the tested prior restoration core, checks payload hashes, and backs up every file it replaces. Other modified cores are refused rather than overwritten. The installation does not modify save/profile files. No lab launcher, copied profile or special market command-line flag is needed.

To remove it while the game is closed:

    python install.py --game "PATH/TO/SatelliteReign" --uninstall

Removal restores the previous files and removes only files owned by this installation. It refuses to remove files changed after installation. Keep the backup folder inside the game directory until removal is complete. Exit the shop before disabling or removing the mod.

## Visit the market

Select one or more agents. In the Grid's Center Square, use the blue vending machine closest to the drink machine in the adjacent blue pair. Hover for the normal interaction cursor, then click. Agents approach briskly and enter together.

Inside, right-click to walk; Shift-right-click or double-right-click to sprint. Mouse wheel zooms, middle-drag pans. Counter popups consume scrolling and lock the room camera while browsing. Click the EXIT doorway to return all inside agents to their individual street positions.

- **Arms Exchange:** icons, item details and prototype purchases. Research/equip through the usual game menus.
- **Gene Clinic:** tiered DNA stock; stored DNA fusion consumes both inputs and produces one improved sample. Live augmentation consumes only the donor and preserves the recipient's identity/body/equipment. Assigned or queued DNA is protected. Read **How it works** and the confirmation before a procedure.
- **Identity Exchange:** free agent and DNA renaming.

Normal saves capture market records. Agents are returned to the street before their positions are captured. This feature is single-player only.

Existing restoration features remain included: repair drones, camera hijack/C4, combat policies, bench sitting, drinks, appearance, billboards, taxis and the F7 settings panel. Their world shortcuts are suspended while the market owns input, then resume outside.

The optional read-only objective preflight plugin is included. Room geometry is authored content; native item art and meshes are read from the player's installed game at runtime. The copied test game and test profiles are not distributed.

For the hardware-specific Linux/Proton FPS workaround, see FPS-LAUNCHER.md. Keep the existing eight-core setup on the validated host; it is not a universal CPU mapping for other PCs.
