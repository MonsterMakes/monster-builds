# Part guide: one browser page, one section per part (see PROJECT_STATE.md, Deliverables and Parts).
# Runs gen3.py for the shared model and drawings, and reuses the drawing helpers in gen_shop.py
# (everything above its "# ---- index and assembly" marker). No counts, no step lists, no sign-off.
import math

OUT = 'part-guide'
REV, ISSUED = 'Q', '23 September 2026'

g = {}
exec(open('gen3.py').read(), g)
_shop = open('gen_shop.py').read()
_shop = _shop.split('# ------------------------------------------------------------------ index and assembly')[0]
sh = {'G0': g}
exec(_shop.replace("exec(open('gen3.py').read(), ns)", "ns.update(G0)"), sh)

fr, D = g['fr'], g['D']
mitred, miter_end, bar, p1_placement, base_field, wall_field = sh['mitred'], sh['miter_end'], sh['bar'], sh['p1_placement'], sh['base_field'], sh['wall_field']
HOLD = '<span class="hold">HOLD</span>'
r = {}
exec(open('gen_rail.py').read()
     .replace('open("out/cable-rail-drawings.html", "w").write(html)', 'pass')
     .replace('open("part_R.html", "w").write("".join(html_sheets))', 'pass'), r)
exec(open('draw_parts.py').read())


def fig(svg, cap, cls="big"):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


def table(head, rows, cls="grid"):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section(no, name, includes, body, drawings=""):
    return (f'<article class="sheet part" id="p{no}">'
            f'<header class="tb"><div class="num">{no}</div><div class="ttl"><h2>{name}</h2><p>{includes}</p></div></header>'
            f'<div class="body">{drawings}<div class="ref">{body}</div></div></article>')


def hero(svg, cap, cls="hero"):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


def pair(*figs):
    return '<div class="pair">' + "".join(f'<figure class="hero"><div class="scroll">{s}</div><figcaption>{c}</figcaption></figure>' for s, c in figs) + '</div>'


# ------------------------------------------------------------------ drawings new to the part guide
def frame_variants():
    """Plan of each tread frame variant: stems, screw holes and the front edge."""
    W, Dp = 48.0, 11.25
    d = D(-6, 111, -30.5, 15, 6.4, "tfv")

    def frame(ox, oy, stems, landing, title, ends=None):
        P = lambda u, v: (ox + u, oy + v)
        M = 2.5
        E = 3.0 if stems else 2.5      # post treads take the wider end member
        d.poly([P(0, 0), P(W, 0), P(W - E, M), P(E, M)], "steel ob")
        d.poly([P(0, Dp), P(W, Dp), P(W - E, Dp - M), P(E, Dp - M)], "steel ob")
        d.poly([P(0, 0), P(E, M), P(E, Dp - M), P(0, Dp)], "steel ob")
        d.poly([P(W, 0), P(W - E, M), P(W - E, Dp - M), P(W, Dp)], "steel ob")
        for u in (11.5, 36.5):
            d.rect(*P(u - 0.75, M), *P(u + 0.75, Dp - M), "steel ob")
        d.rect(*P(21.5625, M), *P(26.4375, Dp - M), "steel ob")
        for u in (6, 18, 30, 42):
            for v in (1.5, Dp - 1.5):
                d.circle(*P(u, v), 0.3, "redc")
        for u in (11.5, 36.5):
            for v in (4.25, 7.0):
                d.circle(*P(u, v), 0.3, "redc")
        for u in (1.5, W - 1.5):
            for v in (2.75, 8.4375):
                if landing and v == 2.75:
                    continue
                d.circle(*P(u, v), 0.3, "redc")
        for u, v in stems:
            d.rect(*P(u - 1.25, v - 1.25), *P(u + 1.25, v + 1.25), "coral ob")
        d.text(ox + W / 2, oy - 1.9, "front edge, the nose", "sm", "middle")
        d.text(ox + W / 2, oy + Dp + 1.6, title, "vt", "middle")
        if ends:
            d.text(ox + 1, oy + Dp + 1.6, ends[0], "sm", "start")
            d.text(ox + W - 1, oy + Dp + 1.6, ends[1], "sm", "end")

    frame(0, 0, [], False, "Plain")
    frame(58, 0, [(1.5, 5.625), (W - 1.5, 5.625)], False, "Post tread, both ends")
    d.dim((58.0, Dp), (58.25, Dp), 1.9, "1/4")
    d.dim((58.0, 0), (59.5, 0), -2.6, "1-1/2 to stem \u2104")
    frame(0, -21, [(1.5, 1.5), (W - 1.5, 1.5)], True, "Landing")
    d.dim((-1.6, -21.0), (-1.6, -19.5), 0, "1-1/2")
    frame(58, -21, [(W - 1.5, 5.625)], False, "Post tread, one end", ("house end", "outboard end"))
    d.text(-6, -26.0, "Stem placement: the stem face sits 1/4 in from the frame's outer edge, which is the 3/16 post wall plus 1/16 slip,", "sm", "start")
    d.text(-6, -27.6, "so the 3\u00d73 post finishes flush with the frame. Same set-back at the nose on the landing tread, so the post face", "sm", "start")
    d.text(-6, -29.2, "lands on the nosing line. Stem centre is therefore 1-1/2 from whichever edge it aligns to.", "sm", "start")
    return d.svg("Tread frame variants, plan from above")



# ------------------------------------------------------------------ section 4, tread frame
def tread_frame():
    b = []
    b.append('<p class="lede">The steel frame under each tread. A picture frame of HSS laid flat, two joists, and a '
             'centre connection of two M8 collars with the M3 plate welded between them. The frame drops over its stub, '
             'bears on the stub through an EPDM pad under M3, and is held by two through bolts. The ash planks screw on '
             'from below at the bench. Post treads also carry the P1 stems their guard posts sleeve over. '
             'One tread system everywhere: the upper stair, its landing tread and the master bath stair all use this frame.</p>')
    b.append('<p class="fm"><b>Field measurement:</b> none. Every dimension in this section is fixed, so the frame can be built before the survey.</p>')

    b.append("<h3>Components and material</h3>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("F1", "Front and back members", '<span class="nw">HSS 3×1-1/2×1/8</span>', '<span class="nw">A500 Gr C</span>', "48 long point, 42 short point",
         "Laid flat, 3 in wide. 45° miter both ends, mirror images, long point on the outside edge."),
        ("F2", "End members", '<span class="nw">HSS 3×1-1/2×1/8</span>', '<span class="nw">A500 Gr C</span>', "11-1/4 long point, 5-1/4 short point",
         "As F1. On post treads the P1 stem welds to its top."),
        ("F3", "Joists", '<span class="nw">HSS 1-1/2×1-1/2×1/8</span>', '<span class="nw">A500 Gr C</span>', "5-1/4, square both ends",
         "Fit between F1 members at ±12-1/2 from the frame centreline."),
        ("M8", "Collars", "Flat bar 3/8 × 1-1/2", "A36", "5-1/4, square",
         "Two per frame, identical. Full frame depth, standing on edge between the F1 members, 4-1/8 clear between them."),
        ("M3", "Plate", "Flat bar 3/8 × 4", "A36", "5-1/4, square",
         "Between the collars, top flush with the frame top. Caps the open stub."),
        ("P1", "Guard stem", '<span class="nw">HSS 2-1/2×2-1/2×3/16</span>', '<span class="nw">A500 Gr C</span>', "7, square both ends",
         "Post variants only. Welded to the top of F2; the 3×3 guard post sleeves over it."),
    ]))
    b.append('<p class="note">Frame overall 48 × 11-1/4 × 1-1/2. The frame top is the plane the planks sit on and the plane M3 is flush with.</p>')

    b.append("<h3>Variants</h3>")
    b.append('<p>The frame, the centre connection and the joists are the same in every variant. Only the stems and one pair of screw holes change.</p>')
    b.append(table(["Variant", "Used at", "P1 stems", "F2 screw holes", "Planks (part 5)"], [
        ("Plain", "Upper stair treads 2, 3, 5 and 6; master bath stair treads without a post", "None", "Both holes in each F2", "Plain"),
        ("Post tread, both ends", "Upper stair treads 1 and 4", "Both ends, centred on F2: 5-5/8 from the front edge", "Both holes; the stem sits between them", "Notched both ends"),
        ("Landing", "Upper stair landing tread, flush with the top of wall", "Both ends, in line with the nose: 1-1/2 from the front edge, post front face flush with the nose", "Front hole omitted in each F2, under the stem", "Front plank notched at both ends"),
        ("Post tread, one end", "Master bath stair, the post tread on L-103", "Outboard end only, centred on F2: 5-5/8 from the front edge", "Both holes in each F2", "Notched one end"),
    ]))
    b.append('<p class="note">Across the tread every stem is centred on the 3 in end tube, 1/4 in from each side of it, 22-1/2 from the frame centreline. '
             'Lower stairs use this same frame; which variant goes where follows from its geometry, still open.</p>')
    b.append(fig(frame_variants(), "Plan of each variant, front edge down. Coral: P1 stems. Red: 7/32 screw holes. On the landing the stem sits over the F1/F2 miter, so the front F2 holes are omitted and the miter weld is ground flush under the stem."))

    b.append("<h3>Hardware</h3>")
    b.append(table(["Mark", "Item", "Where"], [
        ("H1", "3/8-16 × 5-1/2 type 316 through bolts, nylock nuts, EPDM-bonded or nylon washers at each steel face, anti-seize on the threads",
         "Two per frame, through both collars and the stub, 1-1/2 apart, in 13/32 holes drilled at dry fit"),
        ("H2", "1/8 EPDM pad, 4 × 3", "On the open stub top, under M3"),
        ("H3", "#10 × 2-3/4 type 316 wood screws, pan or washer head, 1/8 pilot in the ash",
         "Up through every 7/32 frame hole into the planks, 1-1/4 into the ash. Listed with part 5"),
        ("—", "Guard post through bolts", "Through the P1 stem holes. Listed with part 6"),
    ]))

    b.append("<h3>Fabrication detail</h3>")
    b.append(fig(g['tread_frame_plan'](), "The whole frame from above, stem shown for a centred post tread. Build on a flat jig and check both diagonals before welding out."))
    b.append(fig(g['tread_frame_section'](), "Section across the frame at the stub."))
    b.append(fig(g['saddles'](), "M3 and the M8 collars from below. The collars run full depth between the F1 members. M3 sits between them on 1/16 shims, flush with the frame top, and is groove-welded from the top and ground flush. Set on shims this way, any frame fits any stub."))
    b.append(fig(g['tread_centre_detail'](), "How the frame drops over its stub: 1/16 clear each side, the stub rising 1 in between the collars and bearing on M3 through the pad."))

    b.append(fig(mitred(48, 3, taps=[(6, 1.5), (18, 1.5), (30, 1.5), (42, 1.5)], drains=[(1.5, 0.9), (46.5, 0.9)], title="F1, plan, laid flat"),
                 "F1. Four 7/32 holes on the member centreline, 6 and 18 either side of centre, through both walls. On one F1 of each frame, a 3/16 drain in the underside near each end."))
    b.append(fig(mitred(11.25, 3, taps=[(2.75, 1.5), (8.4375, 1.5)], stem=(5.625, 1.5), title="F2, plan, laid flat"),
                 "F2. Two 7/32 holes on the centreline at the plank centres, 2-3/4 and 8-7/16 from the front edge, through both walls. Dashed: a centred stem. Landing: the front hole is omitted."))
    b.append(fig(miter_end(3, 1.5, "F1 and F2 end, enlarged"), "Both ends of F1 and F2 mitred 45° across the 3 in face, long point on the outside edge."))
    b.append(fig(bar(5.25, 1.5, [(1.25, 0.75, 0.11, "void ob"), (4.0, 0.75, 0.11, "void ob")], [(1.25, 0.75, "7/32 holes through both walls, 1-1/4 from each end")], "F3, top face", 48),
                 "F3. Square both ends. One hole lands in each plank."))
    b.append(fig(bar(5.25, 1.5, [(1.875, 0.5, 0.2, "hidc"), (3.375, 0.5, 0.2, "hidc")], [(1.875, 0.5, "13/32 through-bolt holes, drilled at dry fit")], "M8 collar, face", 48),
                 "M8. Both collars identical. Holes 1-1/2 apart, centred on the length, 1/2 up from the bottom edge, drilled through both collars and the stub together at dry fit."))
    b.append(fig(bar(2.5, 7, [(1.25, 2.5, 0.22, "void ob"), (1.25, 5.75, 0.22, "void ob"), (1.25, 0.4, 0.09, "void ob")],
                     [(1.25, 5.75, "7/16 holes, both faces, at 2-1/2 and 5-3/4"), (1.25, 0.4, "3/16 drain just above the weld")], "P1, face", 40),
                 "P1. Square both ends. Holes through both faces for the post bolts; drain in the wall just above the frame."))
    b.append(fig(p1_placement(), "P1 placement, right end of the tread; the left end is the mirror image. Dimensions run from the front edge to the stem centre."))

    b.append("<h4>Welds</h4>")
    b.append(table(["Joint", "Weld", "Note"], [
        ("F1 and F2 corners", "Full perimeter at each miter", "Check the frame flat and square before welding out."),
        ("F3 joists to F1", "Fitted, welded both faces", "At ±12-1/2 from the frame centreline."),
        ("M8 collars to F1", "3/16 fillet both sides at each end", "Collars run between the F1 members, never notched into them."),
        ("M3 plate to M8 collars", "Square groove, 1/16 root opening, full 3/8 penetration from the top, ground flush",
         "Continuous: this weld is the water seal over the open stub. Set the gap with 1/16 shims."),
        ("P1 stem to F2", "1/4 fillet all around", "Plumb. The stem load goes into the side walls of the 3 in end tube. On the landing, grind the F1/F2 miter weld flush where the stem lands."),
    ]))

    b.append("<h4>Holes, drains and vents</h4>")
    b.append(table(["Feature", "Size", "Location", "Drilled"], [
        ("Plank screw holes, F1", "7/32, both walls", "On the centreline, 6 and 18 either side of centre", "Before coating"),
        ("Plank screw holes, F2", "7/32, both walls", "On the centreline, 2-3/4 and 8-7/16 from the front edge; landing omits the front hole", "Before coating"),
        ("Plank screw holes, F3", "7/32, both walls", "On the centreline, 1-1/4 from each end", "Before coating"),
        ("Frame drains", "3/16", "Underside of one F1, near each end", "Before coating"),
        ("Plate drains, M3", "3/16", "On the plate centreline, clear of the stub footprint, one each side", "Before coating"),
        ("Through-bolt holes, M8 and stub", "13/32", "1-1/2 apart, centred on the collar, 1/2 up", "At dry fit, collars and stub together"),
        ("Post bolt holes, P1", "7/16, both faces", "2-1/2 and 5-3/4 up from the bottom", "Before coating"),
        ("Stem drain, P1", "3/16", "Just above the weld", "Before coating"),
    ]))
    b.append('<p class="note">The screw holes are also the coating vents for F1, F2 and F3; no other vents. All drilling before coating.</p>')

    b.append("<h4>Finish</h4>")
    b.append('<p>Grind welds smooth and break every sharp edge. SSPC-SP10 blast, zinc-rich primer, TGIC powder topcoat. '
             'Cold galvanizing compound on the P1 stems. No oil, layout dye or wax crayon on faces that stay. '
             'Leave all holes and drains open after coating.</p>')

    b.append("<h3>Checks</h3>")
    b.append(table(["Check", "Target"], [
        ("F1 long point / short point", "48 / 42, ± 1/32"),
        ("F2 long point / short point", "11-1/4 / 5-1/4, ± 1/32"),
        ("F3, M8, M3 length", "5-1/4 ± 1/32, ends square"),
        ("P1 length", "7 ± 1/32, ends square"),
        ("Miters", "45°, square to the face"),
        ("Frame diagonals", "Equal within 1/16"),
        ("Frame flat", "Within 1/16 over 48"),
        ("Joist position", "±12-1/2 from the frame centreline, ± 1/16"),
        ("Clear between collars", "4-1/8 ± 1/32"),
        ("M3 flush with the frame top", "Within 1/32"),
        ("Plank screw holes", "7/32, ± 1/16"),
        ("Stem centre from the frame centreline", "22-1/2 ± 1/16"),
        ("Stem centre from the front edge", "Centred variants 5-5/8 ± 1/16; landing 1-1/2 ± 1/16"),
        ("Stem plumb", "Within 1/32 over 7"),
        ("Stem holes", "± 1/32"),
    ]))
    return section(4, "Tread frame", "M7: F1, F2, F3, M8 collars, M3 plate, P1 stems, screw holes", "".join(b))



# ------------------------------------------------------------------ section 1, base plate
def base_plate_sec():
    top = []
    top.append('<p class="lede">M4 is the plate the foot of the upper stair stands on: bearing on the existing pier over flashing, held down by the four existing rods, '
               'with the M1 level cut and the M2b tread 1 stub welded to its top.</p>')
    top.append(f'<p class="fm"><b>Field measurement:</b> rod holes only, drilled at dry fit to the rods as set {HOLD}. The plate can be cut now. '
               'M4 is not shimmed; the pitch and cross slope it takes on the pier go into the M1 level cut in part 3.</p>')
    top.append(hero(base_iso(), "The base assembled, seen from downhill. M4 is welded to the stringer and coated with it."))
    top.append(hero(base_plan(), f"M4 from above, uphill to the right. Dimensions from the first riser. Hidden: the M2b stub and M1 level cut footprints. Rod positions are as measured; drill to the rods as set {HOLD}."))
    top.append(hero(base_section(), "Section A–A at the uphill rod row, to scale. The rod sits 5/8 off the stub face, less than the washer's 5/8 radius plus the 1/4 fillet; red is where the washer meets the fillet."))
    top.append(hero(g['base_detail'](), "Side view along the stair: M4 on the pier, M2b rising into the tread 1 collars, the M1 level cut uphill of it."))
    top.append(hero(base_field(), cls="hero narrow", cap= f"The two angles measured on M4 once it sits on the pier {HOLD}. They go into the M1 level cut, not the plate."))

    b = ['<h3>Reference</h3>']
    b.append("<h4>Components and material</h4>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("M4", "Base plate", "Plate 1/2", "A36", "12 × 30, square", "Break all edges."),
        ("A2", "Pier rods, existing", "1/2 threaded rod", "As found", "In place", "Measured and drilled to; not supplied."),
        ("F", "Flashing", "Self-adhered membrane", "—", "Lapped past each plate edge", "Supplied with the hardware."),
    ]))
    b.append("<h4>Variants</h4>")
    b.append('<p>One.</p>')
    b.append("<h4>Hardware</h4>")
    b.append(table(["Mark", "Item", "Where"], [
        ("A2", "1/2-13 nut, 1-1/4 OD hardened round washer and acorn cap", "Each existing rod, over M4"),
        ("F", "Self-adhered flashing", "Between the pier and M4, full bearing"),
    ]))
    b.append("<h4>Notes, concerns and callouts</h4>")
    b.append('<p><b>The washer runs into the stub weld. Unresolved.</b> The uphill rod row sits 2-5/8 each side of centre and the '
             'M2b stub face is at 2, so a 1-1/4 OD washer reaches exactly to the stub and then overlaps its 1/4 fillet by 1/4. '
             'A standard nut lands almost on the fillet, with no socket clearance and little for a wrench. Options: a smaller washer '
             'with a flat ground on the stub side, a lighter fillet local to the rod, or setting and torquing those two nuts before the '
             'stub is welded on. Decide before the stub goes on M4; after that the third option is gone.</p>')
    b.append(f'<p><b>The M2b notch cannot be cut in the shop.</b> Its depth is whatever the trimmed M1 level cut leaves, and nobody '
             f'knows that until M4 is on the pier {HOLD}. Cut, weld and grind it at dry fit before coating.</p>')

    return section(1, "Base plate", "M4, rod nuts and washers", "".join(b), "".join(top))



# ------------------------------------------------------------------ section 2, wall plate
def wall_plate_sec():
    WPT, WPB = g['WP_TOP'], g['WP_BOT']
    TR = g['TOTAL_RISE']
    top = []
    top.append('<p class="lede">M6 is the plate the head of the upper stair hangs on: bolted flat to the concrete wall on six adhesive '
               'anchors, with the stringer\'s plumb cut welded to its face. It carries the whole upper end of the flight.</p>')
    top.append(f'<p class="fm"><b>Field measurement:</b> the plate is fixed and can be cut and drilled now. Where the anchors land waits '
               f'on a rebar scan {HOLD}. The wall\'s lean and plan angle are measured here too, but they change the M1 plumb cut in part 3, not this plate.</p>')
    top.append(hero(wall_iso(), "The head of the stair. M6 on the wall face, six anchors through it, the stringer welded to its outboard face."))
    top.append(hero(g['wall_face'](), cls="hero asis", cap=f"M6 from outside the wall. Anchors 9 apart across and 5 apart vertically, three rows. Hatched: the stringer tube behind the plate. The pattern shifts to clear the wall verticals {HOLD}."))
    top.append(hero(g['wall_detail'](), cls="hero asis", cap="Section at the wall: the plate, the plumb cut welded to it, and the top two treads."))
    top.append(hero(wall_field(), cls="hero narrow", cap=f"The two wall angles to measure once the plate location is marked {HOLD}. Both go into the M1 plumb cut."))

    b = ['<h3>Reference</h3>']
    b.append("<h4>Components and material</h4>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("M6", "Wall plate", "Plate 1/2", "A36", "12 × 16, square", "Long dimension vertical. Break all edges."),
        ("A1", "Wall anchors", "1/2 threaded rod", "316", "Cut to suit", "Six. Adhesive set, 3-1/2 to 4-1/2 embedment."),
    ]))
    b.append("<h4>Variants</h4>")
    b.append('<p>One.</p>')
    b.append("<h4>Hardware</h4>")
    b.append(table(["Mark", "Item", "Where"], [
        ("A1", "1/2 type 316 threaded rod in Simpson SET-3G, 3-1/2 minimum to 4-1/2 maximum embedment, 9/16 hole, nut and washer at each", "Six, through M6 into the wall"),
        ("—", "EPDM-bonded or nylon washer under each nut", "Stainless against coated steel"),
    ]))
    b.append("<h4>Notes, concerns and callouts</h4>")
    b.append('<p><b>Embed 3-1/2 minimum, 4-1/2 maximum.</b> The stem is 6 thick, so embedment is bounded at both ends: '
             'deeper is stronger, since bond grows with depth and breakout with depth to the 1.5 power, but the hole has to stop '
             'short of the back face and clear of the bar layer, which sits about 4 in from the front. 4-1/2 is the practical ceiling. '
             'Drill 9/16 for the 1/2 rod, the same bit as the plate holes, with a carbide hammer bit. Brush and blow each hole clean '
             'and dry before the adhesive: a hole full of dust is the usual reason an adhesive anchor underperforms.</p>')
    b.append('<p><b>1-1/2 minimum edge distance, and it is my addition.</b> The drawing set says to shift the anchors clear of the wall '
             'verticals but never says how far they may move. The nominal pattern leaves 1-1/2 to the plate sides and 2 top and bottom. '
             'If the scan forces a hole closer than 1-1/2 to any edge, the plate grows rather than the edge distance shrinking.</p>')
    return section(2, "Wall plate", "M6, anchors", "".join(b), "".join(top))



# ------------------------------------------------------------------ section 3, stringer weldment
def stringer_sec():
    fr_, DEG_ = g['fr'], g['DEG']
    LONG, SHORT = g['LONG_PT'], g['SHORT_PT']
    STUB_LONG, STUB_SHORT = g['STUB_LONG'], g['STUB_SHORT']
    top = []
    top.append('<p class="lede">The backbone: one length of HSS 8×4×1/4 cut level at the base and plumb at the wall, with six stubs '
               'welded along its top face and the two plates welded to its ends. Everything else in the stair hangs off this weldment, '
               'and almost every dimension on it comes from the field.</p>')
    top.append(f'<p class="fm"><b>Field measurement:</b> nearly all of it {HOLD}. The total rise and run set the length, both cut angles '
               f'and every stub mark. The pier\'s pitch and cross slope trim the level cut; the wall\'s lean and plan angle trim the plumb '
               f'cut. Cut nothing until the readings from parts 1 and 2 are in hand.</p>')
    top.append(hero(stringer_iso(), "The weldment. Tread 1 stands on M2b off the base plate; treads 2 to 7 stand on the six stubs along the stringer."))
    top.append(hero(g['stringer_cut'](), f"M1 along its own axis: both cuts, the six stub centrelines from the long point, and the 3/16 hole under each stub. Lengths and marks shown are design values {HOLD}."))
    top.append(hero(g['side_elev'](), "The assembled flight, for where each stub lands."))

    b = ['<h3>Reference</h3>']
    b.append("<h4>Components and material</h4>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("M1", "Mono stringer", '<span class="nw">HSS 8×4×1/4</span>', '<span class="nw">A500 Gr C</span>',
         f"{fr_(LONG)} long point, {fr_(SHORT)} short point",
         f"Level cut {90 - DEG_:.2f}° off square at the base, plumb cut {DEG_:.2f}° off square at the wall. Both trimmed in the field."),
        ("M2a", "Stubs, treads 2 to 7", '<span class="nw">HSS 6×4×1/4</span>', '<span class="nw">A500 Gr C</span>',
         f"{fr_(STUB_LONG)} long, {fr_(STUB_SHORT)} short",
         f"Six, identical. 4 across the stair, 6 in the run, 6 at the centreline, single {DEG_:.2f}° cut, open top."),
        ("M2b", "Stub, tread 1", '<span class="nw">HSS 6×4×1/4</span>', '<span class="nw">A500 Gr C</span>', "4-3/16, square both ends",
         "Welded to M4, not to M1. Detailed in part 1."),
    ]))
    b.append("<h4>Variants</h4>")
    b.append('<p>Three: the upper stair as drawn here, the lower stairs, and the master bath stair. Same section, same stub, same '
             'connection; the length, the cut angles and the stub marks come from each flight\'s own geometry.</p>')
    b.append("<h4>Hardware</h4>")
    b.append('<p>None. M1 carries no fasteners of its own: the treads bolt to the collars in part 4, the plates are welded, '
             'and the anchors and rods belong to parts 1 and 2.</p>')
    b.append("<h4>Notes, concerns and callouts</h4>")
    b.append('<p><b>Drill the vent holes before the stubs go on.</b> Each stub needs a 3/16 hole through the stringer\'s top face, '
             'its downhill edge flush with the inside of the stub\'s downhill wall, so the stub drains and vents into the stringer. '
             'Once the stub is welded down, that hole is inside a closed box and cannot be drilled. A stub welded shut with no vent '
             'can blow its weld in the cure oven.</p>')
    b.append(f'<p><b>One stub angle, and it moves with the rise.</b> All six stubs share a single {DEG_:.2f}° cut, which is the stringer\'s '
             f'slope. That angle comes from the total rise and run recorded in parts 1 and 2 {HOLD}. If either changes, the angle, both '
             f'stub face lengths and every stub mark along the tube change with it. Cut one stub, check it on the slope jig, then cut the rest.</p>')
    b.append(f'<p><b>The weep notch is cut last.</b> A 3/16 notch in the bottom edge of M1 at whichever corner sits lowest on M4 as set {HOLD}. '
             f'Which corner that is depends on the pier\'s cross slope, so it cannot be chosen in the shop. Tape it and the stub holes '
             f'while blasting, pull the tape before coating, and leave everything open afterwards.</p>')
    return section(3, "Stringer weldment", "M1, M2a stubs, M2b tread-1 stub, stub holes, weep", "".join(b), "".join(top))



# ------------------------------------------------------------------ section 4, tread frame
def tread_frame_sec():
    top = []
    top.append('<p class="lede">The steel frame under each tread: a picture frame of HSS laid flat, two joists, and a centre '
               'connection of two collars with the M3 plate between them. It drops over its stub, bears on the stub through a '
               'neoprene pad under M3, and is held by two through bolts. The ash screws on from below at the bench. '
               'Post treads also carry the P1 stems their guard posts sleeve over.</p>')
    top.append('<p class="fm"><b>Field measurement:</b> none for the frame itself. Every dimension here is fixed, so all seven can '
               f'be built before the survey. Only the through-bolt holes wait, and they are drilled at dry fit onto the actual stub {HOLD}.</p>')
    top.append(hero(tread_iso(), "One frame from above and outboard, ash off. The stub rises through the middle between the collars; M3 caps it, flush with the frame top."))
    top.append(hero(g['tread_frame_plan'](), "The frame from above, stem shown for a centred post tread. Build on a flat jig and check both diagonals before welding out."))
    top.append(hero(frame_variants(), "The four variants in plan, front edge down. Coral: P1 stems. Red: 7/32 screw holes, which also vent the frame for coating."))
    top.append(hero(g['tread_frame_section'](), cls="hero asis", cap="Section across the frame at the stub."))
    top.append(hero(g['saddles'](), cls="hero asis", cap="M3 and the collars from below. The collars run full depth between the F1 members; M3 sits between them on 1/16 shims, flush with the frame top, groove welded from above and ground flush."))
    top.append(hero(g['tread_centre_detail'](), cls="hero asis", cap="How the frame drops over its stub: 1/16 clear each side, the stub rising 1 in between the collars and bearing on M3 through the pad."))

    b = ['<h3>Reference</h3>']
    b.append("<h4>Components and material</h4>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("F1", "Front and back members", '<span class="nw">HSS 2-1/2\u00d71-1/2\u00d73/16</span>', '<span class="nw">A500 Gr C</span>',
         "48 long point; 43 short point on plain treads, 42 on post treads",
         "Laid flat. Mitred both ends, mirror images, long point on the outside edge."),
        ("F2", "End members, plain treads", '<span class="nw">HSS 2-1/2\u00d71-1/2\u00d73/16</span>', '<span class="nw">A500 Gr C</span>',
         "11-1/4 long point, 6-1/4 short point", "45\u00b0 miter to F1."),
        ("F2", "End members, post treads", '<span class="nw">HSS 3\u00d71-1/2\u00d73/16</span>', '<span class="nw">A500 Gr C</span>',
         "11-1/4 long point, 6-1/4 short point", "Wider so the P1 stem lands on it with 1/4 either side. Unequal miter, about 50/40."),
        ("F3", "Joists", '<span class="nw">HSS 1-1/2\u00d71-1/2\u00d71/8</span>', '<span class="nw">A500 Gr C</span>', "6-1/4, square both ends",
         "Between the F1 members at \u00b112-1/2 from the frame centreline."),
        ("M8", "Collars", "Flat bar 3/8 \u00d7 1-1/2", "A36", "6-1/4, square",
         "Two per frame, identical, full frame depth between the F1 members, 4-1/8 clear between them."),
        ("M3", "Plate", "Flat bar 3/8 \u00d7 4", "A36", "6-1/4, square", "Between the collars, top flush with the frame top. Caps the open stub."),
        ("P1", "Guard stem", '<span class="nw">HSS 2-1/2\u00d72-1/2\u00d73/16</span>', '<span class="nw">A500 Gr C</span>', "7, square both ends",
         "Post variants only. Welded to the top of F2; the 3\u00d73 guard post sleeves over it."),
    ]))
    b.append('<p class="note">Frame overall 48 \u00d7 11-1/4 \u00d7 1-1/2. The frame top is the plane the planks sit on and the plane M3 is flush with.</p>')
    b.append("<h4>Variants</h4>")
    b.append(table(["Variant", "Used at", "P1 stems", "F2 screw holes"], [
        ("Plain", "Upper stair treads 2, 3, 5 and 6", "None", "Both holes in each F2"),
        ("Post tread, both ends", "Upper stair treads 1 and 4", "Both ends, centred on F2, 5-5/8 from the front edge", "Both holes; the stem sits between them"),
        ("Landing", "The landing tread, flush with the top of wall", "Both ends, in line with the nose, 1-1/2 from the front edge", "Front hole omitted in each F2, under the stem"),
        ("Post tread, one end", "Master bath stair, the post tread on L-103", "Outboard end only, centred on F2", "Both holes in each F2"),
    ]))
    b.append("<h4>Hardware</h4>")
    b.append(table(["Mark", "Item", "Where"], [
        ("H1", "3/8-16 \u00d7 5-1/2 through bolts, black oxide stainless, nylon insert nuts, isolating washers at each steel face, anti-seize",
         "Two per frame, through both collars and the stub, 4 apart, left to right"),
        ("H2", "1/16 solid neoprene pad, 6 \u00d7 4, self-adhesive backed", "On the open stub top, under M3"),
        ("H3", "#10 \u00d7 2-3/4 type 316 wood screws, 1/8 pilot in the ash", "Up through every 7/32 frame hole into the planks. Listed with part 10"),
    ]))
    b.append("<h4>Notes, concerns and callouts</h4>")
    b.append('<p><b>Drill with the pad in the joint.</b> The frame bears on the pad, so the pad sets how high it rides on the stub. '
             f'Drill the bolt holes with the real pad in place, or an offcut of it, and slot the collar holes 13/32 \u00d7 9/16 vertically {HOLD}. '
             'Drilled dry and round, every hole ends up 1/16 out, and the clearance on a 3/8 bolt is 1/32 \u2014 the bolt will not start.</p>')
    b.append('<p><b>Two different F2 sections, and they are not interchangeable.</b> Post treads take the 3 wide end member so the stem '
             'has a landing; plain treads take 2-1/2. The F1 short point differs to match, 42 against 43. A 2-1/2 end member on a post '
             'tread leaves the stem overhanging its own support, and the miters will not close.</p>')
    b.append('<p><b>Once drilled, a tread belongs to its stub.</b> The holes are bored through collars and stub together, so the frames '
             'stop being interchangeable at that moment. Stamp each frame and its stub before anything comes apart for coating.</p>')
    return section(4, "Tread frame", "F1, F2, F3, M8 collars, M3 plate, P1 stems, screw holes", "".join(b), "".join(top))


# ------------------------------------------------------------------ section 5, spigots
def spigot_sec():
    top = []
    top.append('<p class="lede">How a guard post meets concrete. A plate bolted down with adhesive rods, a stem welded to it, and '
               'the post sleeved over the stem and through-bolted. Two variants: the single-rod wall spigot used under every level '
               'and raked post on the wall or a pier, and the wider two-rod plate under a gate hinge post.</p>')
    top.append(f'<p class="fm"><b>Field measurement:</b> the parts are fixed and can be built now. Where each rod lands is not: '
               f'the wall is scanned at every spigot and the hole set between the verticals {HOLD}.</p>')
    top.append(hero(spigot_iso(), "The wall spigot assembled, post cut away. The stem is welded to the plate; the post slides over it and is bolted through both walls."))
    top.append(hero(r['wall_spigot'](), cls="hero asis", cap="Wall spigot in elevation, with the post over it. The three lowest cable holes pass through the stem and are drilled 9/16 there; post and stem are drilled together."))
    top.append(hero(r['spigots'](), cls="hero asis", cap="The three pieces side by side: wall spigot, hinge-post plate in plan, and the tread stem from part 4 for comparison."))

    b = ['<h3>Reference</h3>']
    b.append("<h4>Components and material</h4>")
    b.append(table(["Mark", "Component", "Stock", "Grade", "Cut", "Notes"], [
        ("K-5", "Wall spigot plate", "Plate 3/8", "A36", "6 \u00d7 6, square", "One 9/16 hole for the rod, on the wall centreline. Shimmed level and bedded in adhesive."),
        ("K-5", "Wall spigot stem", '<span class="nw">HSS 2-1/2\u00d72-1/2\u00d73/16</span>', '<span class="nw">A500 Gr C</span>', "10, square both ends",
         "Welded all around to the plate. 3/16 drain just above the weld. Cable holes 9/16 here, oversize to the post."),
        ("K-5", "Hinge-post plate", "Plate 3/8", "A36", "5 \u00d7 12", "Two rods at 6 centres, along the wall. Same 10 stem."),
        ("A", "Rods", "1/2 threaded rod", "316", "Cut to suit", "One per wall spigot, two per hinge plate. 6 embedment in SET-3G, 9/16 hole."),
    ]))
    b.append("<h4>Variants</h4>")
    b.append(table(["Variant", "Plate", "Rods", "Used at"], [
        ("Wall spigot", "6 \u00d7 6 \u00d7 3/8", "One, on the wall centreline", "Every level and raked guard post on a wall or pier"),
        ("Hinge post", "5 \u00d7 12 \u00d7 3/8", "Two at 6 centres, along the wall", "Gate hinge posts, where the leaf hangs off the post"),
    ]))
    b.append("<h4>Hardware</h4>")
    b.append(table(["Mark", "Item", "Where"], [
        ("A", "1/2 type 316 threaded rod in SET-3G, 6 embedment, 9/16 hole, nut and washer", "One per wall spigot, two per hinge plate"),
        ("\u2014", "(2) 3/8 through bolts per post", "Through post and stem, drilled together at dry fit"),
        ("\u2014", "Horseshoe shims, structural polymer, slipped around the rod", "Under the plate, as many as the level needs"),
        ("\u2014", "Polyurethane construction adhesive", "Bedding the plate and sealing its underside"),
    ]))
    b.append("<h4>Notes, concerns and callouts</h4>")
    b.append('<p><b>Shim before the nut goes on, not after.</b> The plate levels on horseshoe shims slipped around the rod, '
             'then beds in adhesive. Torque the nut onto an unshimmed plate and a 3/8 plate will bend to the concrete rather than '
             'the concrete yielding to it, and the stem goes out of plumb with it. Shim first, adhesive, then torque.</p>')
    b.append('<p><b>Three cable holes pass through the stem, and they are oversize there.</b> Measured from the top of the plate '
             'the grid lands at 2-11/16, 5-13/16 and 8-15/16, all inside the 10 stem. The post holes are 7/16; the stem holes are '
             '9/16, so a cable slightly out of line with the stem still passes without bearing on it. Drill post and stem together '
             'with the post on the stem; drilled apart they will not line up at all.</p>')
    b.append('<p><b>The hinge post plate is not a bigger version of the other one.</b> Its two rods run along the wall, so the plate '
             'resists the gate leaf trying to twist the post about the wall line. Turn that plate 90\u00b0 and the rods sit in line with '
             'the load, which is the one orientation that does nothing.</p>')
    b.append(f'<p><b>6 of embedment, and the wall is 6 thick.</b> Unlike the wall plate in part 2, these rods are specified at full '
             f'depth. They sit on the wall centreline rather than in its face, so the cone is not cut short by a free edge, but it '
             f'does mean the hole is nearly through the stem {HOLD}: scan first, and stop the bit short of the far face.</p>')
    return section(5, "Spigots", "Plate, stem, rods", "".join(b), "".join(top))

# ------------------------------------------------------------------ the guide
PARTS = [
    (1, "Base plate", base_plate_sec), (2, "Wall plate", wall_plate_sec), (3, "Stringer weldment", stringer_sec),
    (4, "Tread frame", tread_frame_sec), (5, "Spigots", spigot_sec), (6, "Guard post", None),
    (7, "Splines", None), (8, "Top rail", None), (9, "Deck frame", None), (10, "Tread planks", None),
    (11, "Deck slats", None), (12, "Gates", None), (13, "Handrail", None),
]
built = [(n, name, f()) for n, name, f in PARTS if f]
nav = "".join(
    (f'<a href="#p{n}"><b>{n}</b>{name}</a>' if f else f'<span class="todo"><b>{n}</b>{name}</span>')
    for n, name, f in PARTS)

css = open('css.txt').read() + """
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
.hidp{stroke:var(--mark);stroke-width:1.2;stroke-dasharray:5 3;fill:none}
.coral{fill:var(--steeld)}
.redc{fill:none;stroke:var(--hold);stroke-width:1.6}
.hold{font:700 11px 'Archivo Narrow',sans-serif;color:var(--hold);border:1px solid var(--hold);border-radius:3px;padding:0 4px}
.note{color:var(--ink2);font-size:14px}
.lede{font-size:16px;max-width:78ch;margin-top:0}
.part h4{font-family:"Archivo Narrow",sans-serif;font-size:16px;font-weight:600;margin:16px 0 6px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink2)}
.part h3{border-top:1px solid var(--line);padding-top:14px;margin-top:24px}
nav .todo{color:var(--ink2);opacity:.55}
nav .todo b{color:var(--ink2)}
.cols figure{margin-bottom:10px}
main{grid-template-columns:minmax(0,1fr)}
.fm{background:color-mix(in srgb,var(--steel) 25%,transparent);border-left:3px solid var(--mark);padding:8px 12px;max-width:none}
.nw{white-space:nowrap}
.hero{margin:0 0 22px}
.hero .scroll svg{width:100%;height:auto;min-width:640px}
.hero figcaption{font-size:14.5px}
.vt{font-size:15px;font-weight:600;fill:var(--ink)}
.asis{display:flex;flex-direction:column;align-items:center}
.asis .scroll svg{width:auto;max-width:100%;min-width:0}
.asis figcaption{max-width:80ch}
.iwF{fill:color-mix(in srgb,var(--steeld) 85%,var(--ink) 15%)}
.inF{fill:color-mix(in srgb,var(--steeld) 80%,var(--ink) 20%)}
.narrow{max-width:720px}
.narrow .scroll svg{min-width:0}
.asis{display:flex;flex-direction:column;align-items:center}
.asis .scroll svg{width:auto;max-width:100%;min-width:0}
.asis figcaption{max-width:80ch}
.isB{fill:color-mix(in srgb,var(--steel) 60%,var(--ink) 40%)}
.icB{fill:color-mix(in srgb,var(--conc) 62%,var(--ink) 38%)}
.iwB,.inB{fill:color-mix(in srgb,var(--steeld) 55%,var(--ink) 45%)}
.ifB{fill:var(--pad)}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(460px,1fr));gap:22px;align-items:start}
.ref{border-top:2px solid var(--ink);margin-top:8px;padding-top:4px}
.ref h3{border-top:0;margin-top:10px}
.io{stroke:var(--ink);stroke-width:1;stroke-linejoin:round}
.isT{fill:var(--steel)}.isS{fill:color-mix(in srgb,var(--steel) 72%,var(--ink) 28%)}.isF{fill:color-mix(in srgb,var(--steel) 86%,var(--ink) 14%)}
.icT{fill:var(--conc)}.icS{fill:color-mix(in srgb,var(--conc) 75%,var(--ink) 25%)}.icF{fill:color-mix(in srgb,var(--conc) 88%,var(--ink) 12%)}
.ifT,.ifS,.ifF{fill:var(--pad)}
.iwT{fill:var(--steeld)}.iwS{fill:color-mix(in srgb,var(--steeld) 70%,var(--ink) 30%)}
.inT{fill:var(--steeld)}.inS{fill:color-mix(in srgb,var(--steeld) 65%,var(--ink) 35%)}
.iv{fill:color-mix(in srgb,var(--steel) 45%,var(--ink) 55%)}
.clash{fill:var(--hold);stroke:var(--hold);stroke-width:1}
@media (max-width:640px){.pair{grid-template-columns:1fr}}
@media (max-width:640px){.cover{grid-template-columns:1fr}.stamp{justify-self:start}}
"""
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Part guide – stairs, rail and landing</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Part guide</h1>
<p>Stairs, rail and landing. One section per part: its components, variants, material, hardware, fabrication detail and checks. Numbers come from the same model as the drawing set, rev {REV}, {ISSUED}. Quantities are in the complete shop guide and the BOM. {HOLD} marks anything that waits on field measurement.</p></div>
<div class="stamp">Build to the<br>drawing set rev {REV}</div></header>
<nav aria-label="Parts">{nav}</nav>
<main>{''.join(s for _, _, s in built)}</main></body></html>"""
open(f'out/{OUT}.html', 'w').write(html)
print("ok", [n for n, _, _ in built])


