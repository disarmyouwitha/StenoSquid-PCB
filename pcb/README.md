# Plate-mounted Steno Squid

[KiCad project](steno-squid.kicad_pro) · [Front](previews/front-pop.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [BOM](BOM.csv) · [Validation](validation.json)

Rev D is a 21.78 × 46.32 mm, 1.0 mm PCB with a full-length rounded rectangular outline, no ears, no USB notch and 1 mm corner radii. The switch-facing edge keeps a net 1.12 mm trim from the original full-ear outline: the pin-8 edge was widened 0.88 mm from the first Rev D cut so its silkscreen gap matches pin 1's. The opposite edge, bottom edge, header and electrical placements remain fixed. The local ground pour refills to the new edge on both copper layers. Pop sits centred between the STENO SQUID and 16 MB labels.

It sits on the Choc switch plate with the flash, passives and Pop silkscreen on top. The front silkscreen reads STENO SQUID above Pop and the 16 MB flash capacity below it. Viewed from above with USB-C at the top, the contact row is at the bottom and pin 1 is at the left. Eight soldered pins mate with the owner's host sockets through the plate slot. The owner confirmed paper-template header alignment and checked a socket stack that allows the board to sit flush on the plate. Exact socket MPN and mating pin length have not been supplied. The STEP model represents the board and fitted SMT parts, without the socket stack. The local WSON model has a 3.4 × 4.3 mm exposed pad matching the land pattern.

U1, C1 and R1 are fitted. C2 and R2 remain unpopulated until the breadboard rail test. The 0.40 mm supply route from J1 to C1 to U1 stays on the front without vias, and four stitching vias connect the local ground pours. The artwork area has a copper keepout on both layers. The ground pours extend through the contact row to provide a return path for CLK and IO2. A local antenna cutback is an option if Bluetooth testing shows a problem. The antenna location, required clearance and Bluetooth performance remain unverified. [Electrical and RF review](../docs/design-review.md)

KiCad reports zero ERC, DRC, unconnected items and schematic-parity issues with every ERC and DRC category enabled. The owner-confirmed template retains the 2.54 mm pitch and nominal 2.20 mm pin-1 offset. Final populated-board fit is not yet tested.

The revised fit template comes from the native outline and J1 pad coordinates. Print at actual size and verify its 50 mm bar and 10 mm square; recheck the new edge and solid top with keycaps and USB plug fitted. Keep J1 fixed when editing the outline. Regenerate with `python3 tools/make_fit_template.py`. Confirm the switched rail on USB and battery and measure its fall time with the breadboard flash.

[Plate geometry and provisional antenna assumptions](../docs/plate-geometry.md)
