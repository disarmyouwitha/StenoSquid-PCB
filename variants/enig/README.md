# Plate-mounted Steno Squid — ENIG gold-artwork variant

[KiCad project](steno-squid.kicad_pro) · [Front](previews/front-pop.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [BOM](BOM.csv) · [Validation](validation.json)

This is the 16 MB [baseline board](../../pcb/README.md) with one cosmetic change: Pop and the two remaining splats (the 6 small splat dots are removed from the shared artwork, same as the baseline) are exposed, isolated front copper with a matching front soldermask opening, instead of front silkscreen. Under ENIG finish that exposed copper renders gold. A 1 mm no-copper/no-via/no-track keepout halo surrounds the shapes (including inside the eye sockets) so the front ground pour stays clear of them; outside that halo the ground pour extends under the whole board exactly as it does on the baseline, 32 MB and 64 MB boards, for a uniform soldermask finish. STENO SQUID and 16 MB stay plain white silkscreen.

Electrically and mechanically this board is identical to [pcb](../../pcb/README.md): same 21.78 × 44.82 mm outline, same header position, same routing, same component placement. Only the Pop/splat treatment and finish differ, so it exists as a separate higher-cost option alongside the strictly-silkscreen baseline rather than replacing it. The same gold-artwork treatment is also available for the [32 MB](../32mb-enig/README.md) and [64 MB](../64mb-enig/README.md) capacity boards, sharing identical halo and Pop geometry.

KiCad reports zero ERC, DRC, unconnected items and schematic-parity issues with every ERC and DRC category enabled. [Electrical and RF review](../../docs/design-review.md) · [Plate geometry and provisional antenna assumptions](../../docs/plate-geometry.md)

Regenerate the fit template with `python3 tools/make_fit_template.py variants/enig` from the repo root after any mechanical edit. Final populated-board fit, powered, RF and assembled-daughterboard qualification remain pending, same as the baseline.

The owner approved the shared outline on 2026-11-17: **1.5 mm total removed from the original 46.32 mm length**, leaving **44.82 mm**, with **R5.35 far-end corners**. Header centres, electrical routing and this project's artwork/finish are preserved. Final populated fit, powered and RF testing remain pending.
