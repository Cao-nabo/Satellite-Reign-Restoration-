# Sharing the Satellite Reign FPS workaround

This is a launch configuration, not a patched game. You can share this text without distributing any game files or the restoration mod.

## Verified setup

Tested on Linux using Proton 10.0 with an Intel Core i9-14900KF. Limiting the processors exposed to this game to eight physical performance cores improved this lab from roughly 20–30 FPS to around 60 FPS at 1280×720 in both the underground room and the city. Higher resolutions and occasional frame spikes still affect performance. This does not fix the separate native memory-allocation crash.

For the exact tested CPU layout, Steam → Satellite Reign → Properties → Launch Options:

```text
PROTON_CPU_TOPOLOGY=8:0,2,4,6,8,10,12,14 %command%
```

Close the game before changing the option. Remove the line to revert. It changes only this game launch, not system-wide processor settings. It does not require our market mod, new saves, modified assemblies or a game reinstall. Keep existing launch options if you have any; do not silently replace them.

## Other computers

The CPU numbers above are specific to the tested machine. Do not assume they identify performance cores on another computer, even one with a similar processor. On Linux, inspect the processor/core mapping with `lscpu -e=CPU,CORE,SOCKET,MAXMHZ` and select one logical processor from each of eight physical performance cores, if available. A mapping needs testing on that hardware; eight is the tested count, not a universal recommendation. Measure the same save, location, resolution and camera before and after.

This syntax is for Proton/Wine. It is not a Windows Steam launch option. A Windows process-affinity equivalent has not been validated here, and this guide does not promise 60 FPS on every system.

## Evidence and limits

The installed Proton 10.0 launcher explicitly forwards PROTON_CPU_TOPOLOGY to WINE_CPU_TOPOLOGY. Runtime logs confirmed SystemInfo.processorCount=8. The player confirmed smoother movement and supplied screenshots showing approximately 60 FPS in the room and city. The standalone launch line is documented from the same setting; a clean-install A/B test without the restoration lab remains useful before advertising a universal game fix. Room-specific rain/camera improvements are separate mod changes, not part of this launch option.
