# Steno Squid 16 MB — DIY hand-solderable SOIC-8 edition

[KiCad project](steno-squid.kicad_pro) · [Front](previews/front.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [BOM](BOM.csv) · [Validation](validation.json)

This is an independent, low-cost sibling of the [16 MB WSON board](../../pcb/README.md), aimed at a soldering iron, flux and tweezers instead of a hot plate or reflow oven. It is **not a modification** of the six existing WSON/ENIG projects — those are untouched; this is an additional project living in its own directory.

## What's different from the WSON baseline

- **U1** is a **Winbond W25Q128JVSIQ**, the same 16 MiB QSPI NOR as the WSON boards but in a **SOIC-8, 208 mil (`StenoSquid:SOIC-8_5.3x5.3mm_P1.27mm`)** gull-wing package — visible, accessible leads, no hidden center pad, no hot plate required. QE is factory-fixed to 1 and the JEDEC ID (`EF 40 18`) matches the WSON part, so the existing firmware/installer should apply unchanged, but that is proven on the WSON Adafruit breakout, not yet on this routed board.
- **C1** (100 nF decoupling) and **R1** (10 kΩ CS# pull-up) move from 0603 to **0805** for easier hand soldering. Same electrical role and placement intent as the baseline — C1 stays close to U1 pin 8 and its ground return.
- **C2 and R2 are omitted entirely** (not just left DNP) — schematic, layout and BOM. The actual tested 16 MB breadboard proof ran with C1/R1 only, and two unpopulated footprints add visual confusion and build steps for no benefit on a hand-solder board.
- Board outline, 1 mm corner radii, 1.0 mm thickness, J1 header position (bit-for-bit identical, verified by [tools/check_diy_soic.py](../../tools/check_diy_soic.py)), and all eight host net assignments are the same owner-approved geometry as the other six projects. Pop, STENO SQUID and 16 MB stay plain white silkscreen, unmoved.
- U1's net-to-pin map is unchanged in *name* (CS_N/IO0/IO1/IO2/IO3/CLK/GND/VCC_SW tied to the same J1 contacts), but the SOIC-8's physical pin layout differs from the WSON's, so the board is fully rerouted around it: the SOIC body is noticeably wider than the WSON, so the stitching vias, the CLK and IO2 detours, and the VCC_SW/CS_N runs to C1/R1 all take different physical paths to clear the bigger pads. C1 and R1 moved to open board area to clear the wider body. There is no U1 pad 9 — no WSON-style exposed-pad land, no paste window, no net-9 copper.

## Validation

This board cannot use `tools/validate.py` as-is — it hard-codes the WSON's pad-9-is-GND and C2/R2-exist assumptions. Instead, [tools/check_diy_soic.py](../../tools/check_diy_soic.py) is the package-aware validator for this project: it reuses the same ERC/DRC/netlist/header-position checks, replaces the WSON-specific assertions with the SOIC-8 contract (exactly 8 numbered pads, no pad 9, 1.27 mm pitch, visible pin-1 marker, 0805 C1/R1, no C2/R2), and additionally asserts via `git diff` that the six original WSON/ENIG projects are untouched. Run it with:

```sh
python3 tools/check_diy_soic.py variants/16mb-diy-soic
```

Current result: zero ERC violations, zero DRC violations (every category enabled), zero unconnected items, zero schematic-parity issues, and the six original projects confirmed unmodified.

**Not yet done:** any hand assembly, continuity/short checks, powered bring-up, JEDEC/quad-read verification, Lapwing install, or host fit of a populated board. See "Suggested regression/bringup tests" below before trusting a built unit.

## Cost (sourced 2026-11-18, not a live quote — recheck before ordering)

These are DigiKey/LCSC/JLCPCB list prices referenced in the DIY handoff brief, not a cart total. Expect them to move.

| | Estimate | Basis |
|---|---|---|
| (a) Per-board BOM only (parts, no PCB) | **~$2.85** | W25Q128JVSIQ ~$2.50–3 (LCSC C97521) + C1/R1 a few cents each in reasonable quantity |
| (b) 5-board bare-PCB fab, amortized, no shipping | **~$0.40/board** | JLC's advertised 2-layer 5-board promo (~$2 before options/shipping) ÷ 5; add BOM parts on top for ~$3.25/board in parts+bare-PCB |
| (c) Delivered one-off build | **roughly $10–20** | One assembled unit needs the 5-board minimum fab run (4 bare spares left over), shipping (commonly $5–15 for a small China-to-US/EU parcel, highly carrier/speed dependent), J1 pins/socket stack, and consumables (flux, fine-tip iron) — **not sourced from a live cart**; get an actual JLCPCB quote with your address and options before committing to a number |

J1 pins, taxes, shipping, and tooling are real costs that a per-board BOM number hides — don't quote "$5 complete" without doing that arithmetic against an actual saved cart.

## Fabrication

Suggested bare-board options to **quote, not assume**: standard green mask (likely cheaper than this project's usual black) vs. black; OSP vs. lead-free HASL vs. ENIG for the exposed SOIC leads' solderability over time; 1.0 mm vs. 1.6 mm (this project's other boards have shipped at both thicknesses — pick one and verify it against the actual connector/socket stack, don't inherit a value silently). No PCBA/assembly order is needed for the base DIY workflow — this is meant to be hand-built.

**No Gerbers have been generated and no order has been placed for this variant.** Per the project's standing rule, fabrication outputs need explicit owner approval first.

## Known open items

- Exact socket MPN and mating pin length (same gap as the other six projects).
- First hand-assembled board: continuity, no shorts, JEDEC ID, quad-read/write, Lapwing install, power-cycle data retention.
- Sourcing lifecycle: Winbond flags `W25Q128JVSIQ` "not recommended for new design" even though it's currently stocked — fine for a prototype, worth tracking for a repeat build.
- 1.0 mm vs. 1.6 mm board thickness has not been chosen for this specific variant.

[Electrical and RF review](../../docs/design-review.md) · [Plate geometry](../../docs/plate-geometry.md)
