# joanie-steel

Exterior steel stairs, cable rail, and master bath landing and stair.
Every drawing is generated from one geometry model, so a dimension change
propagates to all three documents.

**Current revision: Q, issued 23 September 2026.**

## Documents

| Document | Sheets | Source |
|---|---|---|
| Drawing set | 34 (S, R, L series) | `gen3.py` + `gen_rail.py` + `gen_landing.py` → `combine.py` |
| Shop guide, upper stairs | 26 pages | `gen_shop.py` |
| Part guide | sections 1–5 of 13 written | `gen_parts.py` + `draw_parts.py` |

Built copies as published are in `docs/`.

## Build

Run from this directory. All paths are relative to it.

    python3 gen3.py && python3 gen_rail.py && python3 gen_landing.py && python3 combine.py
    python3 gen_shop.py
    python3 gen_parts.py

Output lands in `out/`, which is gitignored.

### PDFs

    pip install playwright && playwright install chromium
    python3 topdf_all.py    # drawing set, 34 sheets, 17x11
    python3 pdf_shop.py     # shop guide, 26 pages, letter

## Files

| File | What |
|---|---|
| `head.py` | Geometry constants and the SVG drawing helper. Everything derives from here. |
| `css.txt` | Shared stylesheet. Light and dark. |
| `gen3.py` | S series: the stairs, plus the shared model other scripts import. |
| `gen_rail.py` | R series: cable rail, guard, fence, gates. |
| `gen_landing.py` | L series: master bath landing and stair. |
| `combine.py` | Joins S + R + L into the drawing set. |
| `gen_shop.py` | Shop guide, one page per part. |
| `gen_parts.py` | Part guide, drawings first then reference. |
| `draw_parts.py` | Isometrics used only by the part guide. |
| `gen_study.py` | Stub width study, 3 vs 6 in the run. Reference only. |
| `gen_revp.py` | Rev P notch review page. Superseded. |
| `topdf.py`, `topdf_all.py`, `pdf_shop.py` | PDF writers. |
| `shot_*.py`, `prev*.py` | Screenshot helpers used while drafting. |

## A caution on the isometrics

`draw_parts.py` hand-rolls its 3D projection with painter's-algorithm depth
sorting and no hidden-line solver. Four separate rendering bugs were found and
fixed in it by eye during drafting. Treat the isometrics as illustrations and
check them visually after any change. The dimensioned orthographic views come
straight from the model and are the dimensional authority.

## Revision history

| Rev | Issued | Change |
|---|---|---|
| O | 21 Sep 2026 | — |
| P | 22 Sep 2026 | Stub to 6 in the run (HSS 6×4×1/4); frame members to 2-1/2×1-1/2×3/16 with 3×1-1/2×3/16 ends on post treads; pocket and collars to 6-1/4; through bolts to 4 apart |
| Q | 23 Sep 2026 | Pad to 1/16 solid neoprene; collar holes slotted 13/32 × 9/16; M2b to 4-3/16 |

Verified 4 November 2026: this source regenerates all three published
documents byte for byte, plus two corrections to the part guide where the
wall spigot stem was still labelled 9 while every other reference said 10.
