# 32 MB and 64 MB hardware drafts

The [capacity projects](../variants/README.md) extend the locked Rev D electrical interface. All three capacities now share the owner-selected **20.9 × 46.32 mm full-length, no-ears outline**, 1.0 mm thickness and top-side mounting. The 2026-11-16 mechanical update trims 2 mm from the switch-facing edge, fills the former USB notch and recenters Pop without changing its shape. All header centres and the opposite edge stay fixed. [Physical fit record](plate-geometry.md) Each version has a complete native KiCad project and its own BOM. The 16 MB project in `pcb/` remains the baseline.

## Package selection

| | 32 MB | 64 MB |
|---|---|---|
| Exact selected part | W25Q256JVEIQ | W25Q512JVEIQ |
| Catalog candidate | [JLC C2682312](https://jlcpcb.com/partdetail/WinbondElec-W25Q256JVEIQ/C2682312) | [JLC C3034691](https://jlcpcb.com/partdetail/WinbondElec-W25Q512JVEIQ/C3034691) |
| JEDEC ID, bytes in wire order | EF 40 19 | EF 40 20 |
| Address range | 0x00000000–0x01FFFFFF | 0x00000000–0x03FFFFFF |

Both package-E drawings specify an 8 × 6 mm nominal body, 0.8 mm maximum height, 1.27 mm terminal pitch and 3.4 × 4.3 mm nominal exposed pad. Terminal numbering is identical. [W25Q256JV Rev G, pp. 6, 24, 85](https://www.mouser.com/datasheet/2/949/w25q256jv_spi_revg_08032017-1489574.pdf) · [W25Q512JV Rev G, pp. 6, 24, 88](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf)

The shared custom footprint uses 1.15 × 0.60 mm terminal lands centered at x = ±3.825 mm, a grounded 3.4 × 4.3 mm exposed land and the four existing 1.3 × 1.7 mm paste windows (about 60% exposed-pad coverage). The EP track/via keepout is retained. Confirm land dimensions, stencil and paste coverage with the assembler. The 3D model is an assembly representation, not a manufacturing authority.

Select the **EIQ WSON parts** when ordering assembly for these layouts. The **FIQ SOIC-16 parts** discussed for breadboarding use a different footprint. The assembly catalog numbers are candidates checked on 2026-11-16; availability and procurement price require a current quote.

## Shared host map

| Contact | Host GPIO / rail | Signal | WSON pad |
|---|---|---|---|
| 1 | P0.07 | CS# | 1 |
| 2 | P0.21 | IO0 | 5 |
| 3 | P0.12 | IO3 | 7 |
| 4 | P0.23 | IO1 | 2 |
| 5 | VCC switched by P0.31 | VCC | 8 |
| 6 | GND | GND | 4 |
| 7 | P0.19 | CLK | 6 |
| 8 | P0.05 | IO2 | 3 |

No additional GPIO or reset header is needed. Local exposed pad 9 is grounded. The larger body required new pad escapes and repositioned passives. Both layouts keep the 0.40 mm front-layer supply, ground pours through the contact area, four ground stitching vias and copper-free artwork area. All fitted components remain on the front.

## Power qualification

C1 remains 100 nF and R1 remains a 10 kΩ CS pull-up to switched VCC. C2 (1 µF) and R2 (100 kΩ) remain DNP. The selected capacity alone does not determine a different resistor or capacitor value. Measure the actual supply before changing population.

The reviewed 32 MB datasheet lists up to 15 mA read current at 50 MHz and 25 mA program/erase current. The 64 MB version lists up to 35 mA read current at 50 MHz and 25 mA program/erase current. At the datasheets' 104 MHz read conditions, the limits are 20 mA and 40 mA respectively. Qualify the host switched rail, voltage droop and startup against the selected part and actual operating conditions. A shared footprint does not establish that the host supply can support either chip. [32 MB electrical specifications, pp. 78–80](https://www.mouser.com/datasheet/2/949/w25q256jv_spi_revg_08032017-1489574.pdf) · [64 MB electrical specifications, pp. 80–83](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf)

Both reviewed parts require 20 µs from valid VCC to chip selection and 5 ms before write instructions. For full power cycling, use the selected part's low-voltage threshold and dwell requirement; the reviewed 64 MB datasheet specifies below 0.9 V for at least 100 µs. Measure rail discharge and signal-pin backpower with C2 and R2 initially empty. [64 MB power sequencing, pp. 81–82](https://www.mouser.com/datasheet/2/949/Winbond_W25Q512JV_Datasheet-3240039.pdf)

## Firmware handoff

Firmware is owned by the project owner and was not changed here. Update accepted chip identification, configured size, address mode/opcodes, memory mapping and dictionary/storage limits. The reviewed IQ parts have fixed QE = 1; do not assume the 16 MB initialization sequence applies unchanged. Check the selected device's read alignment and timing requirements.

Test distinct data around 0x00FFFFFF / 0x01000000 and, on 64 MB, 0x01FFFFFF / 0x02000000. Verify the last sector and confirm that writes above each boundary do not alias or alter earlier data. Repeat after reset, power cycling and reconnect. Read JEDEC ID and SFDP before loading a dictionary.

## Review and release

The generated reports cover ERC, DRC, schematic parity, all eight nets, grounded EP, supply minimum width, local footprint pad geometry, shared copper, original outline and artwork. All rule categories remain enabled. The draft position CSV includes fitted SMT parts only; J1 is assembled manually and C2/R2 are excluded. Confirm footprint rotation with the assembler.

The owner confirmed paper-template header alignment and the flush socket stack. The revised outline and final populated-board fit, switched supply, Bluetooth performance, panelization and stencil approval remain to be checked under the existing [pre-order checklist](pre-order-checklist.md). These drafts include no production Gerbers or drill files.
