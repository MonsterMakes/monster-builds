# Handoff and plan of attack

For a Claude Code session picking this up. Read this first, then do the review
in §1 before writing anything.

Project: **joanie-steel** — exterior steel stairs, cable rail, and a master bath
deck and stair. Owner-fabricated. Reno, Nevada: snowmelt, de-icer, freeze-thaw,
high UV at 4,500 ft.

---

## 0. Where things live

Two sources of truth, and they are not the same thing.

**This repo** is the source of truth for the *generators*. Everything is drawn
from one geometry model, so a dimension change in `head.py` or `gen3.py`
propagates to all three documents. Build and diff before you believe anything.

**The claude.ai artifacts** are the source of truth for the *published
documents* and for the *design record*. They are live links, updated in place,
and they are what gets shared with a fabricator or an engineer.

| Artifact | Link | State |
|---|---|---|
| Drawing set, 34 sheets | `claude.ai/artifact/NdPmN2ccgATfFqixj7hLv9` | Current, rev Q |
| Shop guide, upper stairs | `claude.ai/artifact/G5Wob6Lu3aZhZstCeZGtH9` | Current, rev Q. Becomes the Complete shop guide |
| Part guide | `claude.ai/artifact/1rmH7cAX7jAhbT9wX8csWQ` | Sections 1–5 of 13 written |
| Project state | `claude.ai/artifact/1xNJ9H4kLEa9Q2XMJGxUXn` | **Has drifted — see §2** |
| Structural Details | `claude.ai/artifact/HVsaRFss7NibyVjPJ9BBbn` | Claude Doc, not generated from this repo |
| Archive | `claude.ai/artifact/3DSvXywYS3t7gYqatTPggV` | Retired artifacts, revision snapshots, studies |
| Source bundle | `claude.ai/artifact/VJKRZJ3WDmGq5Ww4tdY451` | **Superseded by this repo** — see §5 |
| Stub width study | `claude.ai/artifact/T4prh3cc4cWjtwim75A2e9` | Reference only |

Current revision: **Q, issued 23 September 2026.** Rev O, P and Q PDFs plus
frozen source bundles are in the Archive and the user's project files.

---

## 1. Start here: the review

Do this before touching anything. It is the reason this file exists.

1. **Build and diff.** From `packages/joanie-steel`, run the build in its
   README and `cmp` each file in `out/` against the same name in `docs/`. All
   three must be byte-identical. They were on 4 Nov 2026. If they are not,
   someone changed the source without rebuilding and that is the first bug.

2. **Reconcile the Project state artifact against the model.** It is stale in
   about a dozen places, catalogued in §2. This is the highest-value task in
   this file: that artifact is the design record a fabricator or engineer would
   read, and it currently disagrees with the drawings.

3. **Read Part guide sections 1–5** and check each against the drawing set.
   They were written one at a time over a long conversation spanning three
   revisions; section 1 was drafted at rev P and revised, and the published
   document was found on 4 Nov to still carry two stale labels (fixed since).
   Assume more of that kind exists.

4. **Eyeball every isometric.** See §4. They are the least trustworthy thing in
   the repo and four separate rendering bugs were found in them by eye.

5. **Check the open design items in §3** are still open and still phrased right.

---

## 2. Known drift: Project state vs the model

The Project state artifact still carries pre-rev-P and pre-rev-Q values.
Authoritative values below are computed from the model as of rev Q. Fix the
artifact; do not change the model to match it.

| Field | Artifact says | Model says |
|---|---|---|
| M1 long point | 81-1/2 | **81-5/8** |
| M1 short point | 63-9/16 | **63-11/16** |
| Stub marks on M1 | 9-9/16 from long point, then five at 13-3/16, to centrelines | **6-3/16 then five at 13-3/16, to the downhill face of each stub** |
| M2a long / short face | 6-15/16 / 5-1/16 | **7-13/16 / 4-3/16** |
| M2b length | 4-1/8 | **4-3/16** |
| F1 / F2 section | mitred 45° throughout | **unequal miter on post treads; F2 is 3×1-1/2×3/16 there, 2-1/2×1-1/2×3/16 elsewhere** |
| F3 joists | 5-1/4 | **6-1/4** |
| M8 collars | 3/8×1-1/2 × 5-1/4 | **× 6-1/4** |
| M3 plate | 3/8×4 × 5-1/4 | **× 6-1/4** |
| Tread through bolts | two 3/8 type 316 | **two 3/8 black oxide stainless, nylon insert nuts, 4 apart, collar holes slotted 13/32 × 9/16** |
| M6 wall anchors | 3-1/2 embed | **3-1/2 min to 4-1/2 max, 9/16 hole** |
| Wall spigot stem | 9 | **10** |
| Wall spigot bedding | (not stated) | **horseshoe shims at the rod, bedded in polyurethane adhesive. No grout.** |
| Part guide status | "section 1 drafted at rev P, in review" | **sections 1–5 written at rev Q** |

Also: the stringer toe moved to **8-9/16** and the heel to **23-15/16** when the
pad went from 1/8 to 1/16 at rev Q. Anything quoting the old toe is stale.

---

## 3. Plan of attack

### 3a. Part guide, sections 6–13

One section at a time. Draft, show the user, revise, then start the next. Do
not run ahead.

| § | Part | Variants | Field measured? |
|---|---|---|---|
| 6 | Guard post | 6: stair, level, corner, landing transition, gate jamb, end | **Yes — every post's length** |
| 7 | Splines | 4: straight, flat corner L, compound corner, backing bar | Some: compound corner, any non-square flat corner |
| 8 | Top rail | 4: level, raked, ends, stair transitions | **Yes — every segment's length and end cuts** |
| 9 | Deck frame | 1 | No |
| 10 | Tread planks | 4, matching the frame variants | No |
| 11 | Deck slats | 1 | No |
| 12 | Gates | 2: walk path, stairwell | Yes — openings confirmed first |
| 13 | Handrail | 3: upper, lower, master | **Yes — lengths** |

Section 6 is next. It is the first part where *every* piece has a field-measured
length, so expect the HOLD marks to do real work.

### 3b. Complete shop guide

Build order, part counts per step, notes, and links into the Part guide. Takes
over the existing shop guide link. Worked through as field measurements arrive.

### 3c. Project BOM

One artifact, a quote package per supplier:

- **Steel** — tube, plate and bar by size, with lengths.
- **Wood** — thermally modified ash, planks and slats.
- **Fasteners and hardware** — stainless bolts, screws, anchors, adhesive;
  cable, fittings, tensioners; flashing, neoprene, shims.
- **Powder coating** — every piece with overall size for oven and rack fit,
  surface area, weight, quantity, masking and blast taping, venting, and the
  finish spec.

---

## 4. Traps

**The isometrics are hand-rolled and have been wrong four times.**
`draw_parts.py` does its own 3D projection with painter's-algorithm depth
sorting and no hidden-line solver. Bugs found and fixed by eye during drafting:
a stringer drawn rising away from the wall instead of falling; stub bottoms
drawn flat instead of cut to the slope; uphill parts painted over downhill ones;
a box built with reversed bounds, flipping its face normals so the underside
rendered. Every one of these came from the drawing code, never from the model.
**Check isometrics visually after any change. The dimensioned orthographic views
come from the model and are the dimensional authority.**

**Two unresolved design items are flagged in the Part guide**, not here, because
they belong with their parts:

- *Section 1:* the 1-1/4 OD washer on the uphill rod row overlaps the M2b stub's
  1/4 fillet by 1/4, leaving no socket clearance. Three options are listed. One
  of them disappears once the stub is welded to the plate, so decide before then.
- *Section 2:* the 1-1/2 minimum anchor edge distance is an addition, not
  something the drawing set states.

**Notes in the Part guide have a bar.** A note earns its place only if it can be
shown to be a problem: a geometric clash, a step that cannot happen in the order
implied, or something added beyond what the drawing set states. No warnings
about unreviewed engineering, no restating standard shop practice, no caution
for its own sake. The user has cut notes twice for failing this.

**Label collisions.** Callout stacking on the older drawing-set sheets is manual
— each label's y is a hand-typed number. The newer isometrics compute stacking
from the target points. If labels overlap on a `gen3.py` or `gen_rail.py` sheet,
it is a manual respace.

---

## 5. Working rules

Carried from the Project state artifact. These are the user's rules, not
suggestions.

- **No design change until explicitly agreed.**
- Any change to what gets built gets a **new revision letter and issue date**.
  Drafting fixes keep the letter.
- **No history in the plan set.** Every sheet states the current design only.
- **Normal stock material sizes only.**
- **One system everywhere:** one tread system, one post system, same parts.
- Weep and drain holes **3/16 maximum**.
- **Terms are fixed:** stub, collar, plate, frame, stem, post, spline. No new
  names for existing parts.
- **Counts live only** in the complete shop guide and the BOM, taken from the plans.
- **Archive, not delete.** A retired artifact keeps its link and moves to the
  Archive page with the date and reason.
- **Update artifacts in place** by passing their links. Never publish a new copy.
- **Work in one chat at a time** — the last chat to save an artifact wins.

**Part guide format.** One artifact, a section per part, read in a browser, so
no letter-size pagination. Each section is drawings first — a 3D view of the
assembled part, then dimensioned plan, sections and details, full width with
labels at reading size — then a short reference: components and material,
variants, hardware, and the notes section described in §4. Dimensions, welds,
tolerances and checks live on the drawings, not in tables. No step lists, no
sign-off, no counts. `HOLD` marks anything that depends on field measurement.

**A change in this repo is not done until it is published.** The repo holds the
generators; the artifacts are what people read. Build, diff, commit, then
republish the affected artifacts in place.

**The Source bundle artifact is superseded by this repo.** It was a manual
snapshot and it silently went stale — on 4 Nov 2026 it was found to predate five
rounds of edits, which had to be hand-reconstructed and verified by diffing
against the published documents. That is precisely the failure git prevents.
Either keep republishing it after every change or retire it to the Archive and
point at this repo. Do not leave it half-maintained.

---

## 6. Open design items

- **Lower stairs geometry** — rise, riser count, base and top connection.
  Blocks the lower stringer and handrail variants. Placeholders only today.
- **Field survey** — S-002 and the field-measurement tables on U-M4 and U-M6.
  Drives M1 cuts, stub angle, weep locations, raked run angle, the 110° corner,
  post lengths and rail lengths. Almost everything in sections 3, 6, 8 and 13
  waits on this.
- **Master deck slat fastening** — still tapped channels with machine screws.
  Revisit with the through-hole approach when the deck section is built.
- **Landing posts and piers** — size and footing held for the engineer.
- **Gate hardware** — latch and hinge selection.
- **Engineer of record** — items listed in section 8 of Structural Details.

---

## 7. Carried over from the Master Design chat

*To be filled in.* The long-running design conversation covered material
selection, code compliance (2018 IRC/IBC, the 4 in sphere check), the finish
system for the Reno climate, and the reasoning behind decisions this repo only
records the outcome of. Pull the parts worth keeping into this file or into the
Project state artifact, then say where the rest lives.
