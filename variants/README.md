# Capacity options

These complete 32 MB and 64 MB drafts derive from the locked Rev D electrical and mechanical design, with the current Pop artwork. The original 16 MB project remains in [pcb](../pcb/README.md).

| Capacity | Flash to populate | Project | BOM | Checks |
|---|---|---|---|---|
| 32 MB / 256 Mbit | W25Q256JVEIQ | [32 MB](32mb/steno-squid.kicad_pro) | [BOM](32mb/BOM.csv) | [Validation](32mb/validation.json) |
| 64 MB / 512 Mbit | W25Q512JVEIQ | [64 MB](64mb/steno-squid.kicad_pro) | [BOM](64mb/BOM.csv) | [Validation](64mb/validation.json) |

Both use the same WSON-8 package-E footprint and copper routing. The capacity marking, selected U1, schematic, BOM and interface metadata distinguish the two projects. The host still needs exactly eight contacts. Neither uses the taller SOIC-16 breadboard part. These 8 × 6 mm parts need the new layout; they are not approved drop-in replacements for the 16 MB project's 6 × 5 mm footprint.

| 32 MB | 64 MB |
|---|---|
| ![32 MB front](32mb/previews/front.png) | ![64 MB front](64mb/previews/front.png) |

Each directory includes the native schematic and board, local symbols and footprints, flash STEP model, assembled-board STEP, schematic SVG, front/back renders, actual-size fit template, full BOM, draft SMT positions and ERC/DRC/netlist reports. Open the project from its own directory so its local libraries resolve.

The designs are complete routed drafts. Host fit, switched supply, RF behavior and assembler approval remain pending. Production Gerbers and drill files are deferred. [Package, power and firmware handoff](../docs/capacity-variants.md)

To regenerate from the 16 MB baseline:

```sh
python3 tools/build_capacity_variants.py
python3 tools/check_capacity_variants.py
```

The build command replaces the generated CAD in both directories. Preserve any manual edits before rebuilding. The check command exports review artifacts and draft assembly positions; it generates no Gerbers. It verifies that both versions share copper, that the original outline and Pop artwork are preserved, and that the eight host contacts agree with the schematic and board.
