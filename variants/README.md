# Production variants

All eight Steno Squid boards share the 21.78 × 44.82 mm plate outline, R5.35 far-end corners, R1 header-end corners and the same eight Boardsource host contacts. [DIY ordering and host map](../README.md)

| Build | 16 MB | 64 MB |
|---|---|---|
| Hand-solderable SOIC with 0805 passives | [SOIC-8 DIY](16mb-diy-soic/README.md) | [SOIC-16 DIY](64mb-diy-soic/README.md) |
| Hand-solderable SOIC with Pop in exposed gold | [SOIC-8 DIY ENIG](16mb-diy-soic-enig/README.md) | [SOIC-16 DIY ENIG](64mb-diy-soic-enig/README.md) |
| Low-profile WSON with Pop in white silkscreen | [Silkscreen](../pcb/README.md) | [Silkscreen](64mb/README.md) |
| Low-profile WSON with Pop in exposed gold | [ENIG](enig/README.md) | [ENIG](64mb-enig/README.md) |

The DIY boards use a 100 nF capacitor and 10 kΩ pull-up in 0805. The WSON boards use 0603 parts and leave the optional C2 and R2 footprints empty initially. ENIG variants expose Pop and its splats as isolated copper with a 1 mm keepout around the artwork. [Package and power review](../docs/capacity-variants.md)

Run `python3 tools/check_capacity_variants.py` from the repository root with KiCad installed to check all eight projects and refresh their review exports. Add `--checks-only` to leave the board files, STEP models and assembly exports alone.
