Read README.md, docs/design-review.md and pcb/interface.json before editing. The active KiCad project is in pcb. The owner locked the map CS P0.07, IO0 P0.21, IO3 P0.12, IO1 P0.23, CLK P0.19 and IO2 P0.05. Keep the schematic, layout, interface, validation and firmware pin states synchronized. C2 and R2 start unpopulated.

The owner approved -1.5 mm total height on 2026-11-17 for every production variant: 21.78 × 44.82 mm, R5.35 corners away from the header and R1 header-end corners. Header positions remain fixed. Preserve each project's silkscreen or ENIG treatment and routing. Validate all six current projects with `python3 tools/check_capacity_variants.py`.

Keep every DRC category enabled. Regenerate the actual-size template after mechanical changes with tools/make_fit_template.py.

The owner confirmed paper-template alignment of all eight contacts and a flush-on-plate socket stack on 2026-11-16. Keep the header centres fixed. The no-ears outline retains a net 1.12 mm switch-facing trim after widening the initial 2 mm cut by 0.88 mm. Final populated-board fit, antenna identification, Bluetooth performance and switched-rail qualification remain pending. Do not fabricate, generate production Gerbers or flash hardware without approval.
