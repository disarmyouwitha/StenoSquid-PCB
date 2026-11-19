# JLCPCB cart — 2026-11-18

This record captures the saved quotes before checkout. The owner subsequently confirmed fabrication. The manifests retain their original quote-stage metadata.

| Variant | Finish | Thickness | Made | Assembled | Merchandise |
|---|---|---|---|---|---|
| 16 MB white silkscreen | OSP | 1.6 mm | 5 | 2 | $50.47 |
| 64 MB gold artwork | ENIG, 1 microinch | 1.6 mm | 5 | 2 | $79.57 |

Combined merchandise: $130.04 before shipping/tax. Black mask; top assembly; U1, C1, R1 only. C2/R2 DNP, J1 manual. Each quantity of 5 includes the 2 assembled boards, leaving 3 bare spares. Depaneling service is OFF: assembly rails remain attached.

Owner approved 1.6 mm for both quotes. Native CAD still specifies 1.0 mm; order thickness is a fabrication selection and was verified in the cart. Gerber copper/outline files were not altered for this selection.

16 MB cart: Y7-5381534A / SMT026111861334-5381534A. This retained quote had its U1 orientation corrected in the site viewer in the earlier session. Local CPL uses 270 degrees for C190862; do not assume KiCad rotation zero matches JLC's model.

64 MB cart: Y8-5381534A / SMT026111861452-5381534A. Assembly project: https://cart.jlcpcb.com/smt-order/?pcbFileNo=81f0444d1bd04bd6a3fda65d2ab64d63

The original 64 MB catalog entry C3034691 was unavailable. Selected C7389628: the exact same manufacturer part W25Q512JVEIQ, 512 Mbit, 2.7–3.6 V, WSON-8 8x6 mm. Site reported 4,776 available; two chips cost $18.6774. Local order BOM updated to match. U1 CPL rotation zero matches the new catalog model with pin 1 at upper left. Viewer model bears generic 25Q256FVEG text; the matched BOM part remains W25Q512JVEIQ. Recheck BOM and polarity in JLC's engineering production files before release.

The separate unfinished 16 MB alternate project fc8cc26fb52143bda3913740dd74fcc3 was not added to cart. Only the two intended designs are in the cart.
