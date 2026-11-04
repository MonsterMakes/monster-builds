import json

# Section being built. One shop guide artifact per section; see PROJECT_STATE.md for codes and links.
SECTION_CODE = 'U'
SECTION_NAME = 'Upper stairs'
SECTION_NO = 1
OUT = 'shop-guide-upper-stairs'
ns = {}
exec(open('gen3.py').read(), ns)
g = ns
fr = g['fr']

SHEETS = []


def fig(svg, cap, cls="big"):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


def sheet(num, title, body):
    SHEETS.append((num, title))
    return (f'<article class="sheet" id="s{num}">'
            f'<header class="tb"><div class="num">{num}</div><div class="ttl"><h2>{title}</h2><p>Upper stairs</p></div></header>'
            f'<div class="body">{body}</div></article>')


def table(head, rows, cls="grid"):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def steps(items):
    return '<ol class="steps">' + "".join(f'<li><span class="box"></span>{s}</li>' for s in items) + "</ol>"


def checks(rows):
    return table(["Check", "Target", "Measured"], [(a, b, '<span class="blank"></span>') for a, b in rows], "grid checks")


HOLD = '<span class="hold">HOLD</span>'
LP, SP = g['LONG_PT'], g['SHORT_PT']
SL_, SS_ = g['STUB_LONG'], g['STUB_SHORT']
DEG = g['DEG']
D = g['D']


def page(mark, name, qty, material, hardware, figs, chk, note="", field=None):
    body = f'<p class="qty"><b>Quantity:</b> {qty}</p>'
    body += "<h3>Material</h3>" + table(["Stock", "Grade", "Cut", "Total for this flight"], material)
    body += "<h3>Hardware</h3>" + (table(["Mark", "Qty", "Item"], hardware) if hardware else '<p class="note">None on this part.</p>')
    body += "<h3>Fabrication detail</h3>" + "".join(fig(s, c) for s, c in figs)
    if field:
        body += "<h3>Field measurements</h3>" + field
    body += "<h3>Checks</h3>" + checks(chk)
    if note:
        body += f'<p class="note">{note}</p>'
    return sheet(f"U-{mark}", f"{mark} {name}", body)


def mitred(L, W, taps=(), drains=(), stem=None, title=""):
    d = D(-3, L + 22, -5, W + 4, min(560 / (L + 25), 40), "mt" + str(int(L)))
    d.poly([(0, 0), (L, 0), (L - W, W), (W, W)], "steel ob")
    for x, y in taps:
        d.circle(x, y, 0.12, "nut")
    for x, y in drains:
        d.circle(x, y, 0.1, "void ob")
    if stem:
        d.rect(stem[0] - 1.25, stem[1] - 1.25, stem[0] + 1.25, stem[1] + 1.25, "hid")
    d.dim((0, 0), (L, 0), -2.0, fr(L) + " long point, outside")
    d.dim((W, W), (L - W, W), 1.6, fr(L - 2 * W) + " short point, inside")
    d.dim((L, 0), (L, W), -1.2, fr(W))
    d.text(L + 5, W / 2, "45° miter both ends", "sm", "start")
    return d.svg(title)


def miter_end(W, H, title):
    d = D(-2, 34, -3.5, 9.5, 22, "me" + str(W))
    d.poly([(0, 0), (10, 0), (10 - W, W), (0, W)], "steel ob")
    _arc(d, 10, 0, 2.2, 135, 180)
    d.text(7.3, 0.9, "45°", "sm", "middle")
    d.dim((0, 0), (10, 0), -1.2, "long point, outside edge")
    d.dim((10 - W, W), (10, W), 1.0, fr(W) + " setback")
    d.dim((10.6, 0), (10.6, W), -0.1, fr(W))
    d.text(5, W + 2.4, "Plan, laid flat: the 45° is across the 3 in face", "sm", "middle")
    d.rect(16, 3.2, 30, 3.2 + H, "steel ob")
    d.dim((30.6, 3.2), (30.6, 3.2 + H), -0.1, fr(H))
    d.text(23, 3.2 + H + 2.2, "Side view: the end looks square", "sm", "middle")
    d.text(23, 1.9, "blade at 45°, cutting down through the 1-1/2", "sm", "middle")
    return d.svg(title)


def bar(L, H, holes=(), labels=(), title="", sc=None):
    s = sc or min(520 / (L + 12), 48)
    d = D(-2, L + 26, -2.2, H + 1.2, s, "br" + str(int(L * 10)))
    d.rect(0, 0, L, H, "steel ob")
    for x, y, r, cls in holes:
        d.circle(x, y, r, cls)
    d.dim((0, 0), (L, 0), -1.2, fr(L))
    d.dim((L, 0), (L, H), -1.2, fr(H))
    for i, (x, y, t) in enumerate(labels):
        d.tag(x, y, L + 2, H - i * 1.1, str(i + 1), t)
    return d.svg(title)


def plank():
    d = D(-3, 96, -9, 6.8, 7.6, "pl")
    d.rect(0, 0, 48, 5.5, "WD ob")
    d.rect(0, -7, 48, -1.5, "WD ob")
    for x in (0, 44.875):
        d.rect(x, 4.0625, x + 3.125, 5.5, "hid")
        d.rect(x, -7, x + 3.125, -5.5, "hid")
    d.dim((0, 5.5), (48, 5.5), 1.0, '48')
    d.dim((0, 4.0625), (3.125, 4.0625), -0.1, '3-1/8')
    d.dim((50, 4.0625), (50, 5.5), -0.1, '1-7/16')
    d.dim((50, -7), (50, -5.5), -0.1, '1-1/2')
    d.text(24, 2.75, "front plank", "sm", "middle")
    d.text(24, -4.25, "back plank", "sm", "middle")
    d.tag(1.5, 4.8, 54, 5, "1", "Post treads only: notch at both ends")
    d.tag(46.4, -6.2, 54, -1, "2", "Notches face each other across the reveal")
    d.tag(24, 0.5, 54, -5, "3", "Pilot holes located from the frame holes at dry fit")
    return d.svg("W1, front and back planks, plan")



def fieldt(rows):
    return table(["Measure in the field", "Design", "How", "Recorded"], [(a, b, c, '<span class="blank"></span>') for a, b, c in rows], "grid checks")


def effects(rows):
    return table(["Measured", "Goes into the M1 cut as"], rows)


import math as _m
def _arc(d, cx, cy, r, a0, a1):
    x0, y0 = cx + r * _m.cos(_m.radians(a0)), cy + r * _m.sin(_m.radians(a0))
    x1, y1 = cx + r * _m.cos(_m.radians(a1)), cy + r * _m.sin(_m.radians(a1))
    d.add(f'<path d="M {d.X(x0):.1f} {d.Y(y0):.1f} A {r*d.S:.1f} {r*d.S:.1f} 0 0 0 {d.X(x1):.1f} {d.Y(y1):.1f}" class="dl" fill="none"/>')


def base_field():
    d = D(-2, 82, -9, 22, 7.0, "bf")
    sl = _m.tan(_m.radians(DEG))
    t = _m.tan(_m.radians(4))
    yp = lambda x: 0.5 + (x - 1) * t
    d.rect(0, -5, 32, 0, "CC ob")
    d.poly([(1, 0), (31, 30 * t), (31, 30 * t + 0.5), (1, 0.5)], "steel ob")
    d.line(1, 0.5, 33, 0.5, "cl")
    _arc(d, 1, 0.5, 24, 0, 4)
    d.text(26, 3.1, "pitch", "sm", "start")
    A, B = 5.0, 20.3
    d.poly([(A, yp(A)), (31, yp(A) + (31 - A) * sl), (31, yp(B) + (31 - B) * sl), (B, yp(B))], "hidp")
    d.text(24, 13, "stringer", "sm", "middle")
    d.text(16, -7.6, "Pitch: side view along the stair", "sm", "middle")
    c = _m.tan(_m.radians(4))
    yq = lambda x: 0.5 + (x - 45) * c
    d.rect(44, -5, 78, 0, "CC ob")
    d.poly([(45, 0), (77, 32 * c), (77, 32 * c + 0.5), (45, 0.5)], "steel ob")
    d.line(45, 0.5, 79, 0.5, "cl")
    _arc(d, 45, 0.5, 26, 0, 4)
    d.text(71, 3.4, "cross slope", "sm", "start")
    d.rect(59, yq(63), 63, 15, "hidp")
    d.poly([(59, yq(59)), (59, yq(63)), (63, yq(63))], "holdf")
    d.text(61, 16.5, "stringer end", "sm", "middle")
    d.text(55.5, 5, "gap = bevel", "sm", "end")
    d.text(61, -7.6, "Cross slope: end view across the stair", "sm", "middle")
    return d.svg("M4 field angles, exaggerated")


def wall_field():
    d = D(-2, 86, -13, 26, 6.4, "wf")
    sl = _m.tan(_m.radians(DEG))
    tl = _m.tan(_m.radians(4))
    xf = lambda y: 28 - (y + 10) * tl
    d.poly([(28, -10), (36, -10), (36, 24), (xf(24), 24)], "CC ob")
    d.line(28, -10, 28, 25, "cl")
    _arc(d, 28, -10, 30, 90, 94)
    d.text(23.5, 22, "lean", "sm", "end")
    d.poly([(xf(0) - 0.5, 0), (xf(16) - 0.5, 16), (xf(16), 16), (xf(0), 0)], "steel ob")
    yt, yb = 12.9, 3.5
    xt, xb = xf(yt) - 0.5, xf(yb) - 0.5
    d.poly([(xt, yt), (xt - 22, yt - 22 * sl), (xb - 22, yb - 22 * sl), (xb, yb)], "hidp")
    d.text(10, 6, "stringer", "sm", "middle")
    d.text(18, -12, "Lean: side view along the stair", "sm", "middle")
    tp = _m.tan(_m.radians(4))
    xw = lambda y: 72 - (y - 6) * tp
    d.poly([(xw(-10), -10), (80, -10), (80, 22), (xw(22), 22)], "CC ob")
    d.line(72, -10, 72, 23, "cl")
    d.line(48, 6, 74, 6, "cl")
    d.rect(50, 4, xw(8), 8, "hidp")
    d.poly([(xw(8), 4), (xw(4), 4), (xw(8), 8)], "holdf")
    _arc(d, 72, -10, 28, 90, 86)
    d.text(75, 15, "plan angle", "sm", "start")
    d.text(58, 9.5, "stringer", "sm", "middle")
    d.text(66, -12, "Plan angle: looking down", "sm", "middle")
    return d.svg("M6 field angles, exaggerated")


def p1_placement():
    d = D(-8, 52, -14.5, 3.5, 15, "p1pl")
    def corner(ox, stem_v, post=False):
        d.poly([(ox - 5, 0), (ox + 3, 0), (ox, -3), (ox - 5, -3)], "steel ob")
        d.poly([(ox - 5, -11.25), (ox + 3, -11.25), (ox, -8.25), (ox - 5, -8.25)], "steel ob")
        d.poly([(ox + 3, 0), (ox + 3, -11.25), (ox, -8.25), (ox, -3)], "steel ob")
        d.rect(ox + 0.25, -(stem_v + 1.25), ox + 2.75, -(stem_v - 1.25), "coral ob")
        if post:
            d.rect(ox, -3.0, ox + 3, 0, "hid")
        d.line(ox - 6, 0, ox + 5, 0, "thin")
        d.text(ox - 1, 1.3, "front edge, the nose", "sm", "middle")
        d.text(ox - 2.5, -1.5, "F1", "sm", "middle")
        d.text(ox + 1.5, -9.9, "F2", "sm", "middle")
        d.line(ox + 2.75, -stem_v, ox + 5.2, -stem_v, "thin")
        d.dim((ox + 5, 0), (ox + 5, -stem_v), 0, fr(stem_v))
        d.dim((ox + 0.25, -(stem_v + 1.25)), (ox + 2.75, -(stem_v + 1.25)), 1.0, "2-1/2")
    corner(0, 5.625)
    corner(19, 1.5, post=True)
    d.text(-1, -13.4, "Treads 1 and 4: centred on F2", "sm", "middle")
    d.text(18, -13.4, "Landing: in line with the nose", "sm", "middle")
    d.tag(20.5, -2.6, 27, -5, "1", "Post, dashed: front face flush with the nose")
    d.tag(19.4, -1.0, 27, -7.5, "2", "Stem sits over the F1/F2 miter:|grind the miter weld flush first")
    return d.svg("P1 placement on the F2 end members, plan, right end of the tread")


# ------------------------------------------------------------------ index and assembly
parts = [
    ("M4", "1", "Base plate"), ("M6", "1", "Wall plate"),
    ("M1", "1", "Mono stringer"), ("M2a", "6", "Stubs, treads 2 to landing"), ("M2b", "1", "Stub, tread 1"),
    ("M7", "7", "Tread frame assembly"),
    ("F1", "14", "Tread frame front and back members"), ("F2", "14", "Tread frame end members"),
    ("F3", "14", "Tread frame joists"), ("M8", "14 + 7", "Collars and M3 plate"),
    ("P1", "6", "Guard stems"), ("W1", "14", "Ash planks"),
]
idx = table(["Mark", "Qty", "Part", "Page"], [(m, q, p, f'<a href="#sU-{m}">U-{m}</a>') for m, q, p in parts])
u0 = idx + fig(g['side_elev'](), "The assembled flight.") + fig(g['tread_section'](), "A tread, front elevation.")
pages = [sheet("U-00", "Upper stairs, index", u0)]

pages.append(page("M4", "Base plate", "1",
    [("PL 1/2", "A36", "12 × 30", "1 pc")],
    [("A2", "4 sets", "Nut, 1-1/4 OD hardened washer and acorn cap on the existing 1/2 pier rods"), ("—", "1", "Self-adhered flashing under the plate")],
    [(g['base_plate'](), "Rod holes drilled through M4 onto the rods as set."),
     (g['base_detail'](), "Where the stringer's level cut lands on M4."),
     (base_field(), "The two angles to measure on M4 as set on the pier. M4 is not shimmed.")],
    [("Size", "12 × 30 ± 1/16"), ("Rod holes", "9/16, on the rods as set")],
    "Set M4 first and measure it before M1 is cut. M4 is not shimmed: every measured angle goes into the M1 level cut, however small. Send the recorded values; U-M1 updates to the as-built angles.",
    fieldt([
        ("Total rise, M4 top to top of wall", fr(g['TOTAL_RISE'] - 0.5), "Laser or water level at the stringer centreline"),
        ("Run, first riser line to wall face", fr(g['X_WALL']), "Tape along the stair centreline string"),
        ("M4 pitch along the stair", "0.0°", "Digital angle gauge on M4, along its length"),
        ("M4 cross slope across the stair", "0.0°", "Digital angle gauge on M4, across its width"),
        ("Rod positions from the first riser line", "3/4 and 5-1/4, 5-1/4 apart", "Tape from the riser line"),
    ]) + effects([
        ("Total rise or run", "Riser height, stringer slope, both cut angles, M1 length and every stub mark"),
        ("Pitch", "The level cut angle is the design angle plus the measured pitch"),
        ("Cross slope", "The level cut becomes compound: a bevel across the 4 in width equal to the measured cross slope"),
    ])))

pages.append(page("M6", "Wall plate", "1",
    [("PL 1/2", "A36", "12 × 16", "1 pc")],
    [("A1", "6", "1/2 type 316 threaded rod anchors in SET-3G, 9/16 hole, 3-1/2 to 4-1/2 embed, nut and washer")],
    [(g['wall_face'](), "Anchor pattern. Scan the wall and set the pattern between the verticals."),
     (g['wall_detail'](), "Where the stringer's plumb cut meets M6."),
     (wall_field(), "The two angles to measure on the wall face where M6 goes.")],
    [("Size", "12 × 16 ± 1/16"), ("Hole pattern", "± 1/16")],
    "Measure the wall before M1 is cut. M6 welds to the plumb cut, so every measured angle goes into that cut, however small.",
    fieldt([
        ("Wall face lean at M6, positive toward the stair", "0.0°", "Digital angle gauge on a straightedge held to the face"),
        ("Wall face angle to the stair centreline, in plan", "90.0°", "Framing square off the stair centreline string"),
        ("Top of wall to top of M6", fr(g['TOTAL_RISE'] - g['WP_TOP']), "Tape down the face"),
        ("Wall stem thickness at M6", "6", "Tape across the wall top"),
    ]) + effects([
        ("Lean", "The plumb cut angle is the design angle plus the measured lean"),
        ("Plan angle off 90°", "The plumb cut becomes compound: a bevel across the 4 in width equal to the measured error"),
        ("Stem thinner than 6", "Anchor embedment and edge distance change; call before drilling"),
    ])))

pages.append(page("M1", "Mono stringer", "1",
    [("HSS 8×4×1/4", "A500 Gr C", f"{fr(LP)} long point", f"1 pc, about {fr(LP + 2)}")], [],
    [(g['stringer_cut'](), "Level cut at the bottom, plumb cut at the top. Stub centrelines along the top face from the long point. A 3/16 hole under each stub, centred 1-3/8 downhill of its centreline so its edge is flush with the inside of the stub's downhill wall; drill before the stubs go on. A 3/16 weep notch in the bottom edge at the lowest corner on M4, as set, left open. No other vents.")],
    [("Long point, top face", f"{fr(LP)} ± 1/16"), ("Short point, bottom face", f"{fr(SP)} ± 1/16"),
     ("Each stub centreline from the long point", "per detail ± 1/16"), ("3/16 hole under each stub, 1-3/8 downhill of its centreline", "6"), ("3/16 weep notch at the lowest corner on M4", "1, cut after the field measurements")],
    f"Cut angles shown are the design values. Before cutting, apply the field measurements recorded on U-M4 and U-M6. Tape the stub holes and the weep notch while blasting; pull the tape before coating. Total rise is taken as {fr(g['TOTAL_RISE'])} {HOLD}."))

pages.append(page("M2a", "Stubs", "6",
    [("HSS 6×4×1/4", "A500 Gr C", f"{fr(SL_)} long face", "about 48 in")],
    [("H1", "2 per stub", "3/8 through bolts; 13/32 holes drilled at dry fit through the collars and stub together")],
    [(g['stub'](), f"One {DEG:.2f}° cut at the stringer end, square on top, long face downhill. No drain; the stub drains through the 3/16 hole in M1.")],
    [("Long face", f"{fr(SL_)} ± 1/32 {HOLD}"), ("Short face", f"{fr(SS_)} ± 1/32 {HOLD}"), ("Cut angle", f"{DEG:.2f}° {HOLD}"), ("Top square both ways", "within 1/32")],
    f"{HOLD} Triple-check the {DEG:.2f}° cut before cutting any stub. It equals the stringer's slope, which comes from the total rise and run recorded on U-M4 and U-M6 once the plates are set and checked. If either changes, the angle and both face lengths change with it, and this page updates."))

pages.append(page("M2b", "Stub, tread 1", "1",
    [("HSS 6×4×1/4", "A500 Gr C", "4-3/16", "4-3/16 in")],
    [("H1", "2", "3/8 through bolts; 13/32 holes drilled at dry fit through the collars and stub together")],
    [(bar(4.0, 4.125, [(0.45, 0.375, 0.094, "void ob")], [(0.45, 0.375, "3/16 weep hole at the lowest corner, 3/8 above M4"), (2, 4.0, "Open top, square cut")], "M2b, side face", 48),
      "Square both ends. Stands on M4, centred on tread 1. The weep hole goes in whichever side wall sits lowest on M4 as set, centred 3/8 up so it clears the 1/4 fillet.")],
    [("Length", "4-3/16 ± 1/32"), ("Ends square", "within 1/32"), ("Weep hole", "3/16, at the lowest corner, 3/8 above M4")]))

pages.append(page("M7", "Tread frame assembly", "7",
    [("See F1, F2, F3, M8, M3, P1", "", "", "")], [],
    [(g['tread_frame_plan'](), "Seven identical frames. Treads 1 and 4 carry P1 stems at mid-length; the landing tread carries them at its front end, for the post at the nosing."),
     (g['tread_frame_section'](), "Section at the stub."),
     (g['tread_centre_detail'](), "How the frame drops over its stub.")],
    [("Diagonals", "equal within 1/16"), ("Flat", "within 1/16 over 48"), ("Clear between collars", "4-1/8 ± 1/32"),
     ("M3 flush with the frame top", "within 1/32"), ("P1 stem centre from frame centreline", "22-1/2 ± 1/16")]))

pages.append(page("F1", "Front and back members", "14, 2 per frame",
    [("HSS 2-1/2×1-1/2×3/16", "A500 Gr C", "48 long point", "about 56 ft")],
    [("H3", "4 per member", "#10 × 2-3/4 type 316 wood screws, up through the 7/32 holes into the plank")],
    [(mitred(48, 3, taps=[(6, 1.5), (18, 1.5), (30, 1.5), (42, 1.5)], drains=[(1.5, 0.9), (46.5, 0.9)], title="F1, plan, laid flat"), "Laid flat, 3 in wide. Four 7/32 holes on the centreline, 6 and 18 either side of centre, drilled through both walls: plank screws and coating vents. On one member of each pair, a 3/16 drain near each end on the underside."),
     (miter_end(3, 1.5, "F1 end, enlarged"), "Both ends mitred 45° in plan, mirror images, long point on the outside edge.")],
    [("Long point", "48 ± 1/32"), ("Short point", "42 ± 1/32"), ("Miters", "45°, square to the face"), ("Screw holes, 6 and 18 from centre", "7/32, ± 1/16")]))

pages.append(page("F2", "End members", "14, 2 per frame",
    [("HSS 2-1/2×1-1/2×3/16 (plain treads), HSS 3×1-1/2×3/16 (post treads)", "A500 Gr C", "11-1/4 long point", "about 13 ft")],
    [("H3", "2 per member", "#10 × 2-3/4 type 316 wood screws, up through the 7/32 holes into the plank ends")],
    [(mitred(11.25, 3, taps=[(2.75, 1.5), (8.4375, 1.5)], stem=(5.625, 1.5), title="F2, plan, laid flat"),
      "Two 7/32 holes on the centreline at the plank centres, through both walls: plank screws and coating vents. Treads 1 and 4: the P1 stem welds at mid-length (dashed), between the holes. Landing tread: the stem sits at the front end, centred 1-1/2 from the front edge, so the front hole is omitted."),
     (miter_end(3, 1.5, "F2 end, enlarged"), "Both ends mitred 45° in plan, mirror images, long point on the outside edge.")],
    [("Long point", "11-1/4 ± 1/32"), ("Short point", "6-1/4 ± 1/32"), ("Screw holes", "7/32, ± 1/16")]))

pages.append(page("F3", "Joists", "14, 2 per frame",
    [("HSS 1-1/2×1-1/2×1/8", "A500 Gr C", "6-1/4", "about 88 in")],
    [("H3", "2 per joist", "#10 × 2-3/4 type 316 wood screws, one into each plank")],
    [(bar(5.25, 1.5, [(1.25, 0.75, 0.11, "void ob"), (4.0, 0.75, 0.11, "void ob")], [(1.25, 0.75, "7/32 holes through both walls, 1-1/4 from each end")], "F3, top face", 48),
      "Square both ends. Fits between the front and back members at ±12-1/2 from the frame centreline. The two holes are the plank screws and the joist's coating vents.")],
    [("Length", "6-1/4 ± 1/32"), ("Ends square", "within 1/32"), ("Screw holes", "7/32, 1-1/4 from each end ± 1/16")]))

pages.append(page("M8", "Collars and M3 plate", "Per frame: 2 collars and 1 plate. For the flight: 14 collars, 7 plates",
    [("Flat bar 3/8 × 1-1/2", "A36", "6-1/4, M8 collars", "about 88 in"),
     ("Flat bar 3/8 × 4", "A36", "6-1/4, M3 plate", "about 44 in")],
    [("H1", "2 per frame", "3/8-16 × 5-1/2 through bolts with nylocks, through both collars and the stub"),
     ("H2", "1 per frame", "1/16 solid neoprene pad, 6 × 4, self-adhesive, on the stub top under the plate")],
    [(g['saddles'](), "Collars and plate from below. The collars run full frame depth between the front and back members; the plate sits between them on 1/16 shims, flush with the frame top, and is welded from the top, full depth, ground flush. That weld is the water seal over the open stub."),
     (bar(5.25, 1.5, [(1.875, 0.5, 0.2, "hidc"), (3.375, 0.5, 0.2, "hidc")],
          [(1.875, 0.5, "13/32 through-bolt holes, drilled at dry fit")], "M8 collar, face", 48),
      "Both collars identical. The two holes are drilled at dry fit through both collars and the stub together, 4 apart, centred on the collar, 1/2 up. Slotted 13/32 × 9/16 vertically in the collars; round 13/32 in the stub.")],
    [("Collar length", "6-1/4 ± 1/32"), ("Plate length", "6-1/4 ± 1/32"),
     ("Clear between collars", "4-1/8 ± 1/32"), ("Plate flush with the frame top", "within 1/32"),
     ("Plate drains, outside the stub footprint", "2 at 3/16"),
     ("Through-bolt holes, after dry fit", "13/32 round in the stub, 13/32 × 9/16 vertical slots in the collars, 4 apart")]))

pages.append(page("P1", "Guard stems", "6: both F2 end members of treads 1, 4 and the landing",
    [("HSS 2-1/2×2-1/2×3/16", "A500 Gr C", "7", "42 in")],
    [("G", "2 per stem", "3/8 through bolts for the post, in the railing sections")],
    [(p1_placement(), "Dimensions are from the front edge of the tread to the stem centre. Across the tread, every stem is centred on the 3 in end tube, 1/4 in from each side, 22-1/2 from the frame centreline. The left end is the mirror image."),
     (bar(2.5, 7, [(1.25, 2.5, 0.22, "void ob"), (1.25, 5.75, 0.22, "void ob"), (1.25, 0.4, 0.09, "void ob")],
          [(1.25, 5.75, "7/16 holes, both faces, at 2-1/2 and 5-3/4"), (1.25, 0.4, "3/16 drain just above the weld")], "P1, face", 40),
      "Square both ends. 1/4 fillet all around to the top of the frame.")],
    [("Length", "7 ± 1/32"), ("Holes", "± 1/32"),
     ("Treads 1 and 4: stem centre from the front edge", "5-5/8 ± 1/16"),
     ("Landing: stem centre from the front edge", "1-1/2 ± 1/16"),
     ("Stem centre from the frame centreline, all six", "22-1/2 ± 1/16"),
     ("Plumb when welded", "within 1/32 over 7")],
    "Placement by tread: tread 1, both ends, centred; tread 4, both ends, centred; landing, both ends, in line with the nose. Tread frames 2, 3, 5 and 6 get no stems."))

pages.append(page("W1", "Ash planks", "14, 2 per tread",
    [("Ash, thermally modified", "8/4 rough, surfaced four sides", "48 × 5-1/2 × 1-3/4", "14 pcs")],
    [("H3", "8 per plank", "#10 × 2-3/4 type 316 wood screws, up through the frame, 1-1/4 into the ash, 1/8 pilot")],
    [(plank(), "Eight screws per plank: four along its front or back member, one at each end tube, one at each joist. Landing front plank: six, since its end holes sit under the posts. 1/8 eased edges, ends sealed, finish all faces before install. Landing tread: only the front plank is notched, at its front corners, 3-1/8 along the plank and 3-1/16 deep.")],
    [("Length", "48 ± 1/16"), ("Width", "5-1/2 ± 1/32"), ("Thickness", "1-3/4 ± 1/32")]))

html_sheets = pages

nav = "".join(f'<a href="#s{n}"><b>{n}</b>{t}</a>' for n, t in SHEETS)
css = open('css.txt').read() + """
.hidp{stroke:var(--mark);stroke-width:1.2;stroke-dasharray:5 3;fill:none}
.coral{fill:var(--steeld)}
.redc{fill:none;stroke:var(--hold);stroke-width:1.6}
ol.steps{list-style:none;counter-reset:s;padding:0;margin:8px 0}
ol.steps li{counter-increment:s;display:flex;gap:10px;align-items:flex-start;padding:5px 0;border-bottom:1px solid var(--line)}
ol.steps li::before{content:counter(s);font:600 13px 'Archivo Narrow',sans-serif;color:var(--mute);min-width:18px}
.box{flex:none;width:14px;height:14px;border:1.5px solid var(--ink2);border-radius:2px;margin-top:2px}
.blank{display:inline-block;min-width:90px;border-bottom:1px solid var(--ink2);height:1em}
.hold{font:700 11px 'Archivo Narrow',sans-serif;color:var(--hold);border:1px solid var(--hold);border-radius:3px;padding:0 4px}
.note{color:var(--mute);font-size:14px}
.qty{font-size:15px;margin:4px 0 8px}
.holdf{fill:var(--hold);opacity:.4}
@media print{html,body,main{background:#fff !important;padding:0 !important;margin:0 !important}nav,header.cover{display:none}article.sheet{break-before:page;margin:0;border:none;box-shadow:none;max-width:none !important;width:100% !important}figure,table,ol.steps li{break-inside:avoid}h3{break-after:avoid}}
"""
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1, viewport-fit=cover">
<title>Shop guide – {SECTION_NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Shop guide: {SECTION_NAME}</h1>
<p>Parts, materials, hardware and fabrication detail, one page per part. Numbers come from the same model as the drawing set, rev Q, 23 September 2026. Section {SECTION_NO} of 9. Page numbers carry the section prefix {SECTION_CODE}.</p></div>
<div class="stamp">Build to the<br>drawing set rev Q</div></header>
<nav aria-label="Sheets">{nav}</nav>
<main>{''.join(html_sheets)}</main></body></html>"""
open(f'out/{OUT}.html', 'w').write(html)
json.dump([n for n, _ in SHEETS], open('shop_ids.json', 'w'))
print("ok", len(SHEETS))


