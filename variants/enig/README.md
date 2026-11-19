# Steno Squid 16 MB WSON · gold ENIG

[KiCad project](steno-squid.kicad_pro) · [BOM](BOM.csv) · [Front](previews/front-pop.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [Validation](validation.json)

This production variant uses a Winbond **W25Q128JVPIQ** in a 6 × 5 mm WSON-8 package, with a 100 nF C1 and 10 kΩ R1. Leave C2 and R2 unpopulated and fit J1 manually. The [matching finish option](../../pcb/README.md) uses the same header positions, component placement and signal routing.

Pop and the two splats use isolated exposed copper with a matching soldermask opening and a 1 mm copper keepout. The ENIG finish makes these shapes gold. The capacity and STENO SQUID labels use white silkscreen.

The board uses the shared **21.78 × 44.82 mm** outline, R5.35 far-end corners, R1 header-end corners and fixed header centres. The CAD specifies 1.0 mm nominal thickness. The owner checked paper-template alignment and a flush socket stack. Final populated fit, switched-rail qualification and Bluetooth performance remain pending. [Fit record](../../docs/plate-geometry.md) · [Package and power review](../../docs/capacity-variants.md)
