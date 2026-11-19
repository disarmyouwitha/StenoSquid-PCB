# Steno Squid 64 MB DIY

[KiCad project](steno-squid.kicad_pro) · [BOM](BOM.csv) · [Front](previews/front.png) · [Back](previews/back.png) · [Schematic](previews/steno-squid.svg) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [Validation](validation.json)

This is the hand-solderable 64 MiB sibling of the [16 MB DIY board](../16mb-diy-soic/README.md). It uses the **Winbond W25Q512JVFIQ** in a 300 mil SOIC-16 package. Its exposed gull-wing leads are on 1.27 mm pitch and there is no center pad. C1 is 100 nF and R1 is 10 kΩ, both 0805. C2 and R2 are omitted. Everything except the mating portion of the header mounts on the front. [Winbond pinout and package drawing, pp. 7 and 89](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf).

The PCB is 21.78 × 44.82 mm and nominally 1.0 mm thick, with the same header centers and white Pop silkscreen as the 16 MB DIY board. The chip can stand **2.64 mm above the PCB** and span **10.64 mm** across its leads. Use the actual-size template to check the outline, and the package dimensions or a real chip to check vertical clearance. The generic KiCad STEP model is for visualization.

| Host contact | Signal | SOIC-16 lead |
|---|---|---:|
| 1 | CS_N | 7 |
| 2 | IO0 | 15 |
| 3 | IO3 | 1 |
| 4 | IO1 | 8 |
| 5 | VCC_SW | 2 |
| 6 | GND | 10 |
| 7 | CLK | 16 |
| 8 | IO2 | 9 |

The dedicated RESET# lead (3) is tied to VCC_SW on the board. Leads 4–6 and 11–14 have isolated lands. Align U1's pin-1 indicator with the board's upper-left marker, tack one corner, check alignment, then solder the remaining leads. Inspect for bridges and verify continuity and no supply short before connecting to the host.

KiCad 10.0.7 reports zero ERC, DRC, unconnected items, and schematic parity issues with every category enabled. The [DIY validator](../../tools/check_diy_soic.py) also checks pad geometry, the header and flash pin maps, and the unchanged board outline. Final populated fit and powered bring-up are pending. Production Gerbers and drills are deferred.

For first power-up, qualify the switched rail for this chip's 2.7–3.6 V range and its read/program/erase load. Check JEDEC ID `EF 40 20` and use the 64 MiB firmware configuration with four-byte addressing. Verify reads and writes across 16 and 32 MiB and near the end of flash, including after power cycling. [Capacity and power review](../../docs/capacity-variants.md).
