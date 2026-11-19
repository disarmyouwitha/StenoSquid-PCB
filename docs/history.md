# Design history

The [current production variants](../variants/README.md) each have a KiCad project. Earlier layouts, review notes, artwork studies and tooling are available in Git at the snapshots below.

On 2026-11-16 the owner selected a full-length no-ears shape with an initial 2 mm switch-side trim and recentered artwork. Header positions, signal tracks and component placements are preserved. [Fit record](plate-geometry.md)

| Snapshot | What it contains |
|---|---|
| [Capacity studies before the physical-fit update](https://github.com/disarmyouwitha/StenoSquid-PCB/tree/5d51189) | Layouts with the earlier stepped full-ear outline |
| [Initial electrical and SOIC studies](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/2afdddb) | Breakout proof of concept, compatibility research and the first routed daughterboard |
| [Low-profile WSON layout](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/19645d1/draft-2) | Locked QSPI wiring, Inkling artwork and improved power and ground routing |
| [Back-mounted comparison](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/45ae03b/draft-3) | Components below the board and rotated front artwork |
| [Plate-top layout with antenna cutback](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/ed61a56/draft-4) | Fallback with ground pulled back near contacts 6–8, available for comparison if Bluetooth testing calls for it |
| [Last snapshot before consolidation](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/bc5cb17) | All previous folders, alternate paper templates and [review records](https://github.com/disarmyouwitha/Boardsource-StenoSquid/tree/bc5cb17/docs) |

On 2026-11-17 the owner selected the **-1.5 mm total length** option, yielding **21.78 × 44.82 mm** with R5.35 far-end corners from the native plate CAD. The approved outline is propagated to the current production variants while preserving the per-project electrical layout and artwork. [Approved fit revision](16mb-plate-fit-review.md)
