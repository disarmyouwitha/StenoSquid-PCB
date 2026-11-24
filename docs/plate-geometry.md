# Production board plate fit

**Approved outline:** all eight PCB projects use 21.78 × 44.82 mm, exactly 1.5 mm shorter than the original 46.32 mm, with R5.35 far-end corners and fixed headers. Owner approved on 2026-11-17.


On 2026-11-16 the owner fitted the full-length paper template to the delivered Boardsource keyboard and confirmed that all eight contacts align. The owner also checked available sockets and reported that the resulting stack allows the daughterboard to sit flush on top of the switch plate. The supplied photos were IMG_5313.heic and IMG_5311.HEIC. These are owner-reported physical checks, not a test of a fabricated, populated StenoSquid board.

The owner selected a full-length outline with **no ears**, initially removing **2 mm from one side**, with the subsequent 0.88 mm width correction retained. The tighter opposite edge and all header centres remain fixed. The top is solid, with no USB notch. The final mechanical envelope is **21.78 × 44.82 mm**, with R5.35 far-end and R1 header-end corner radii and 1.0 mm nominal CAD thickness. Both capacities share this outline across SOIC and WSON packages. The length is reduced by 1.5 mm only at the end away from the header.

## Fixed coordinates

The plate-frame origin is the left end of the plate slot on its centreline. In top view with USB-C above, x increases to the right and y increases toward USB-C. Its KiCad origin remains (25, 70) mm.

| Feature | Current design |
|---|---|
| Switch-facing edge | Plate x = 0.20 mm; KiCad x = 25.20 mm |
| Opposite edge | Plate x = 21.98 mm; KiCad x = 46.98 mm |
| Top edge | Plate y = 42.90 mm; KiCad y = 27.10 mm |
| Bottom edge | Plate y = −1.92 mm; KiCad y = 71.92 mm |
| Pin 1 centre | Plate (2.20, 0) mm; KiCad (27.20, 70) mm |
| Contacts 2–8 | +2.54 mm in x per contact, same y |
| Contact pads / drills | 1.7 mm / 1.0 mm |

The nominal header coordinates are confirmed by the owner's template fit and are not moved to recenter the row after trimming. The new straight edge leaves 1.15 mm to pin 1's copper. On the 64 MB WSON layout it leaves about 1.08 mm to the nearest resistor pad; the rounded corners are also checked by native KiCad DRC. Ground pours are refilled to the new edge. Signal tracks and component placements are retained.

Pop and its splashes retain the current main artwork placement and shape; the length revision does not move them. The source SVG is unchanged. The ground pour now extends under the artwork area on both layers instead of keeping it copper-free, except on the [ENIG variant](../variants/enig/README.md) where the exposed gold shapes keep a 1 mm keepout halo.

## Connector and final assembly

The socket-stack check is recorded as confirmed by the owner. The exact socket manufacturer part number, height and mating pin length have not been supplied; record those for procurement and repeatability. STEP exports show the daughterboard and fitted SMT components, without the host socket stack.

The [revised actual-size template](../pcb/previews/plate-fit-1to1.svg) comes directly from the current KiCad outline and pad coordinates. Check its 50 mm scale bar and 10 mm square when printing. The switch-facing edge and solid top should be rechecked with the USB plug and keycaps installed; the revised template and final populated board have not yet been tested. Keep the previously confirmed header positions fixed.

The earlier [photo-derived plate estimate](plate-fit-estimate.svg) is historical context and is not the current PCB outline. Antenna identity, RF performance and the host switched supply still require their separate checks. [Electrical and RF review](design-review.md)
