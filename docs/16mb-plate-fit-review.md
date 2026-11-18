# 16 MB plate-fit candidate

Branch: `revise/16mb-plate-corners`, based on `main` at `cb7d1fc`. Only `pcb/` is revised. All projects in `variants/`, including the ENIG options, remain unchanged pending owner approval.

| Dimension | Main | 16 MB candidate |
|---|---|---|
| Width | 21.78 mm | 21.78 mm |
| Height | 46.32 mm | 45.82 mm |
| End away from header | KiCad y = 25.60 mm | KiCad y = 26.10 mm |
| Corners at that end | R1 mm | R5.35 mm |
| Header-end corners | R1 mm | R1 mm |
| Header centres, component positions and signal routing | Fixed | Unchanged |

The first candidate removed 1.5 mm. At the owner's request, this update restores 1.0 mm at the end away from the header, leaving a net 0.5 mm reduction from main. The R5.35 curve is retained. Header alignment and the socket stack stay fixed. The resulting length still needs approval from a new paper fit.

## Corner source

The radius is measured from the native [BLE screen plate](https://github.com/disarmyouwitha/boardsource-wireless-plate-files/blob/8b61f1b/Kicad/ble_plate_scr.kicad_pcb), rather than estimated from the photo. The no-screen BLE plate has the same outer corner. Both are in the owner's [plate repository](https://github.com/disarmyouwitha/boardsource-wireless-plate-files).

The source upper outer corner has these three KiCad arc points, in millimetres:

```text
start  182.540733, 42.776196
mid    186.145001, 44.434499
end    187.616096, 48.119142
```

Solving the circumcircle gives centre (182.266096, 48.119142) and radius 5.350000 mm. The native plate arc is truncated by its USB notch. This candidate uses that **same 5.35 mm circular radius** as complete tangent quarter-circles at both non-header-end corners, retaining the requested solid, no-notch shape. The switch-facing corner mirrors the outer-corner curvature; it is not a direct copy of the entire plate perimeter. This is a curvature match, not a claim that the daughterboard has been registered to an eight-pin header in the plate CAD.

The plate source was cloned locally to `/Users/nap/Documents/new_code/boardsource-wireless-plate-files`. Source revision: `8b61f1b`. The plate source files are not copied into this repository.

## Review artifacts

- [Actual-size candidate template](../pcb/previews/plate-fit-1to1.svg)
- [Before/after outline comparison](../pcb/previews/outline-comparison.svg) · [PNG](../pcb/previews/outline-comparison.png)
- [Candidate front](../pcb/previews/front-pop.png)
- [Candidate back](../pcb/previews/back.png)
- [Native board](../pcb/steno-squid.kicad_pcb)
- [STEP](../pcb/steno-squid.step)
- [Validation](../pcb/validation.json)

Print the template at 100% and verify the 50 mm bar. Check the shortened end and larger corners with the USB plug and keycaps installed. Approve the 16 MB shape before applying it to any other project. Powered-board and RF qualification remain separate.

Regenerate this candidate only with `python3 tools/check_capacity_variants.py --only 16`. Do not run the capacity builder on this branch before approval; it would copy the candidate outline into other capacities.
