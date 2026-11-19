# Steno Squid 16 MB DIY

[KiCad project](steno-squid.kicad_pro) · [Bare-board ZIP](../../manufacturing/2026-11-18/diy-bare/stenosquid-16mb-diy-bare.zip) · [BOM](BOM.csv) · [Front](previews/front.png) · [Back](previews/back.png) · [Schematic](previews/steno-squid.svg) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [Validation](validation.json)

The 16 MB DIY production variant uses **Winbond W25Q128JVSIQ** in a 208 mil SOIC-8 package with exposed leads at 1.27 mm pitch. The leads span up to 8.10 mm across the package. [Winbond package drawing, section 10.1](https://www.mouser.com/datasheet/2/949/Winbond_Electronics_Corporation_09_06_2024_W25Q128-3501276.pdf) Fit the 100 nF C1 and 10 kΩ R1 in 0805. The board uses the shared **21.78 × 44.82 mm** outline, fixed header centres and white Pop silkscreen. C2 and R2 are omitted from this layout.

Follow the [DIY build guide](../../README.md#build-and-check) for the parts, orientation, socket fit and first power-up. Check for JEDEC ID `EF 40 18` and verify quad reads and writes on the assembled board.

KiCad reports zero ERC, DRC, unconnected items and schematic-parity issues with every category enabled. Final populated fit and powered bring-up are pending. [Electrical and RF review](../../docs/design-review.md)
