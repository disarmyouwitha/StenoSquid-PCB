# Steno Squid PCB

Build a hand-soldered QSPI flash add-on for Javelin stenography on the left half of the **Boardsource Wireless Corne SMT**. Steno Squid sits on top of the switch plate and connects through the eight-contact expansion slot. Choose **16 MB or 64 MB** of flash.

<img src="variants/16mb-diy-soic/previews/front.png" alt="16 MB DIY Steno Squid PCB with exposed SOIC leads and Pop silkscreen" width="360">

## Choose a DIY board

Both DIY boards use exposed SOIC leads and 0805 passives. Use a fine-tip iron, flux and tweezers. Order a bare PCB using the ZIP for your chosen capacity.

| Capacity | Flash package | Board files | Parts |
|---|---|---|---|
| **16 MB** | Winbond W25Q128JVSIQ, SOIC-8 (208 mil) | [Bare-board ZIP](manufacturing/2026-11-18/diy-bare/stenosquid-16mb-diy-bare.zip) · [KiCad and fit template](variants/16mb-diy-soic/README.md) | [16 MB BOM](variants/16mb-diy-soic/BOM.csv) |
| **64 MB** | Winbond W25Q512JVFIQ, SOIC-16 (300 mil) | [Bare-board ZIP](manufacturing/2026-11-18/diy-bare/stenosquid-64mb-diy-bare.zip) · [KiCad and fit template](variants/64mb-diy-soic/README.md) | [64 MB BOM](variants/64mb-diy-soic/BOM.csv) |

### Parts for one board

| Ref. | Qty. | Part |
|---|---:|---|
| U1 | 1 | The Winbond flash listed for your PCB above |
| C1 | 1 | 100 nF X7R ceramic capacitor, 0805. BOM part Yageo `CC0805KRX7R9BB104` |
| R1 | 1 | 10 kΩ, 1% resistor, 0805. BOM part Yageo `RC0805FR-0710KL` |
| J1 | 1 set | Eight solder pins on 2.54 mm pitch. Match the pins to your host sockets and plate stack |

## Build and check

1. Print your board’s fit template at **100%** and verify the scale bar. The PCB is **21.78 × 44.82 mm**. The owner checked all eight paper-template contacts and a flush socket stack. Check your assembled stack, keycaps and USB plug. The 64 MB SOIC can stand up to 2.64 mm above the PCB. [Fit record](docs/plate-geometry.md)
2. Align the chip’s pin-1 mark with the PCB marker. Tack a corner, check alignment and solder the remaining leads. Solder C1, R1 and the eight mating pins. Inspect for bridges and check continuity and for a VCC-to-GND short before connecting to the host.
3. Check the switched rail under load on USB and battery. Read the flash JEDEC ID, verify quad reads and writes, and check data retention across a power cycle. The 64 MB chip requires firmware configured for its capacity and four-byte addressing. [Power and flash checks](docs/capacity-variants.md)
4. Check final populated-board clearance and compare Bluetooth with the board fitted and removed. KiCad validation covers ERC, DRC and schematic parity. Final populated fit, switched-rail qualification and Bluetooth performance remain open. [Electrical and RF review](docs/design-review.md)

## Host wiring and firmware

Viewed from above with USB-C at the top, the contacts run along the bottom with pin 1 on the left.

| Contact | Host GPIO or rail | Signal |
|---|---|---|
| 1 | P0.07 | CS# |
| 2 | P0.21 | IO0 |
| 3 | P0.12 | IO3 |
| 4 | P0.23 | IO1 |
| 5 | VCC switched by P0.31 | VCC |
| 6 | GND | GND |
| 7 | P0.19 | CLK |
| 8 | P0.05 | IO2 |

Use the Boardsource build for 16 MB. The 64 MB boards require firmware support for their JEDEC ID, capacity and four-byte addressing. The left expansion header serves QSPI, and the right half can retain its display. [Steno Squid ZMK firmware](https://github.com/disarmyouwitha/StenoSquid)

[All production variants](variants/README.md) · [Design history](docs/history.md) · [Source credits and license status](ATTRIBUTION.md)

## Factory-assembled 16 MB and 64 MB boards

These low-profile WSON builds have assembly packages for the flash, decoupling capacitor and CS# pull-up. Fit the eight mating pins by hand. C2 and R2 start unpopulated. The assembly packages record a 1.6 mm fabrication thickness.

| **16 MB · White silkscreen** | **64 MB · Gold ENIG artwork** |
|---|---|
| <img src="pcb/previews/front-pop.png" alt="16 MB WSON PCB with white Pop silkscreen" width="230"> | <img src="variants/64mb-enig/previews/front-pop.png" alt="64 MB WSON PCB with exposed gold Pop artwork" width="230"> |
| [KiCad and BOM](pcb/README.md) · [Gerber ZIP](manufacturing/2026-11-18/16mb-silkscreen/16mb-silkscreen-gerbers.zip) · [BOM and placement](manufacturing/2026-11-18/16mb-silkscreen/) | [KiCad and BOM](variants/64mb-enig/README.md) · [Gerber ZIP](manufacturing/2026-11-18/64mb-gold/64mb-gold-gerbers.zip) · [BOM and placement](manufacturing/2026-11-18/64mb-gold/) |
