# Flash packages, power and firmware

All [production variants](../variants/README.md) use the same eight [host contacts](../README.md#host-wiring-and-firmware) and 21.78 × 44.82 mm outline. Flash leads and pads depend on the package.

| Capacity | Hand-soldered SOIC | Factory-assembled WSON | JEDEC ID | Last byte address |
|---|---|---|---|---|
| 16 MB (128 Mbit) | W25Q128JVSIQ, 208 mil SOIC-8 | W25Q128JVPIQ, 6 × 5 mm WSON-8 | `EF 40 18` | `0x00FFFFFF` |
| 64 MB (512 Mbit) | W25Q512JVFIQ, 300 mil SOIC-16 | W25Q512JVEIQ, 8 × 6 mm WSON-8 | `EF 40 20` | `0x03FFFFFF` |

The 64 MB SOIC-16 has a dedicated RESET# lead tied high to switched VCC and seven isolated lands for unused leads. The 64 MB WSON package is up to 0.8 mm tall and has 1.27 mm terminal pitch. Its custom footprint uses 1.15 × 0.60 mm terminals, a grounded 3.4 × 4.3 mm exposed land and four 1.3 × 1.7 mm paste windows for about 60% coverage. Confirm stencil and paste coverage with the assembler. [16 MB datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf) · [64 MB datasheet](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf)

## Switched-rail qualification

All boards use a 100 nF C1 and a 10 kΩ CS# pull-up R1. WSON boards start with C2 (1 µF) and R2 (100 kΩ) unpopulated. The SOIC boards omit those footprints.

At the datasheet's 50 MHz conditions, the 16 MB chip lists up to 15 mA read current and the 64 MB chip lists up to 35 mA. Both specify up to 25 mA for program or erase. Measure the host rail under read/program/erase load on USB and battery and check startup and discharge. [16 MB electrical specifications, sections 9.2–9.4](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf) · [64 MB electrical specifications, pp. 80–83](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf)

Allow 20 µs from valid VCC to chip selection and 5 ms before write instructions. For a full power cycle, check the required dwell below the selected chip's reset threshold. The 16 MB datasheet gives 0.8 V and the 64 MB datasheet gives 0.9 V, both with a 100 µs dwell. Check for signal-pin backpower during shutdown.

## Firmware and flash checks

The linked Boardsource firmware checks for the 16 MB JEDEC ID. A 64 MB build needs to accept `EF 40 20` and configure four-byte addressing, flash size and storage limits. Check JEDEC ID and SFDP before loading a dictionary. Test distinct data on both sides of `0x01000000` and `0x02000000` on the 64 MB board and verify the last sector. Repeat readback after power cycling and sleep. [Boardsource pin states](https://github.com/disarmyouwitha/StenoSquid/blob/e210af822d156fde14ecfe3dac34ec9727fc1e15/config/boardsource-wireless-corne/qspi.dtsi) · [Firmware JEDEC check](https://github.com/disarmyouwitha/StenoSquid/blob/e210af822d156fde14ecfe3dac34ec9727fc1e15/src/steno_squid/dictionary_flash_qspi.c)
