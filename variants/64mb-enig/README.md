# Plate-mounted Steno Squid — 64 MB, ENIG gold-artwork variant

[KiCad project](steno-squid.kicad_pro) · [Front](previews/front-pop.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [BOM](BOM.csv) · [Validation](validation.json)

This is the [64 MB capacity board](../64mb/README.md) with one cosmetic change: Pop and the two remaining splats (the 6 small splat dots are removed from the shared artwork, same as the baseline) are exposed, isolated front copper with a matching front soldermask opening, instead of front silkscreen. Under ENIG finish that exposed copper renders gold. A 1 mm no-copper/no-via/no-track keepout halo surrounds the shapes (including inside the eye sockets) so the front ground pour stays clear of them; outside that halo the ground pour extends under the whole board exactly as it does on the 16/32/64 MB silkscreen boards, for a uniform soldermask finish. STENO SQUID and 64 MB stay plain white silkscreen.

Electrically and mechanically this board is identical to [64mb](../64mb/README.md): same 21.78 × 44.82 mm outline, same header position, same routing, same WSON-8 8×6 mm footprint and component placement (shared with [32mb](../32mb/README.md)). Only the Pop/splat treatment and finish differ, so it exists as a separate higher-cost option alongside the strictly-silkscreen capacity board rather than replacing it. It shares the same gold-artwork geometry as the [16 MB ENIG board](../enig/README.md) and the [32 MB ENIG board](../32mb-enig/README.md).

KiCad reports zero ERC, DRC, unconnected items and schematic-parity issues with every ERC and DRC category enabled. [Electrical and RF review](../../docs/design-review.md) · [Capacity-option package/power review](../../docs/capacity-variants.md)

Regenerate the fit template with `python3 tools/make_fit_template.py variants/64mb-enig` from the repo root after any mechanical edit. Final populated-board fit, powered, RF and assembled-daughterboard qualification remain pending, same as the other capacity boards.

The owner approved the shared outline on 2026-11-17: **1.5 mm total removed from the original 46.32 mm length**, leaving **44.82 mm**, with **R5.35 far-end corners**. Header centres, electrical routing and this project's artwork/finish are preserved. Final populated fit, powered and RF testing remain pending.
