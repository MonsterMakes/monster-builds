import math
from fractions import Fraction

exec(open('head.py').read())

PW, PH, PLT = 3.0, 3.0, 0.25          # post, top plate thickness
RW, RH, RT = 3.0, 2.0, 0.125          # rail width, height, wall
SB_T, SB_W = 0.5, 2.25                # spline bar
STEM, STEM_T = 2.5, 0.1875


def fig(svg, cap, cls=""):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


SHEETS = []


def sheet(num, title, body, scale="Not to scale; dimensions govern"):
    SHEETS.append((num, title))
    return (f'<article class="sheet" id="s{num}">'
            f'<header class="tb"><div class="num">{num}</div><div class="ttl"><h2>{title}</h2><p>{scale}</p></div></header>'
            f'<div class="body">{body}</div></article>')


# ================================================================= R-501
def inline_post():
    d = D(-3, 62, -13, 6, 12, "ip")
    # panel A: across the rail
    d.rect(1.5, 0, 4.5, RH, "steel ob")
    d.rect(1.5 + RT, RT, 4.5 - RT, RH - RT, "void")
    d.rect(1.5, -PLT, 4.5, 0, "coral ob")
    d.rect(1.5, -12, 4.5, -PLT, "steel ob")
    d.rect(1.5 + 0.1875, -12, 4.5 - 0.1875, -PLT, "void")
    d.line(3, -0.6, 3, 1.0, "lag")
    d.text(3, 4.6, "across the rail", "sm", "middle")
    # panel B: along the rail
    d.rect(13, 0, 31, RH, "steel ob")
    d.rect(13, RT, 31, RH - RT, "void")
    d.rect(17.5, -PLT, 26.5, 0, "coral ob")
    d.rect(20.5, -12, 23.5, -PLT, "steel ob")
    d.rect(20.5 + 0.1875, -12, 23.5 - 0.1875, -PLT, "void")
    for u in (19, 25):
        d.line(u, -0.6, u, 1.0, "lag")
    d.text(22, 4.6, "along the rail", "sm", "middle")
    d.dim((17.5, -PLT), (26.5, -PLT), -1.4, '9" plate, 6" at end posts')
    d.dim((19, -PLT), (25, -PLT), -3.6, '6"')
    d.dim((1.5, RH), (4.5, RH), 1.2, '3"')
    d.dim((13, 0), (13, RH), 1.2, '2"')
    d.tag(4.5, 1.2, 34, 4.6, "1", "HSS 2x3x1/8 rail, laid flat")
    d.tag(4.5, -0.12, 34, 2.2, "2", "PL 1/4 x 3 top plate, welded to the post")
    d.tag(3, -0.8, 34, -2, "3", '(2) 1/4-20 pancake head, up through the plate,|tapped into the rail bottom wall')
    d.tag(26.5, -0.12, 34, -7, "4", "4 screws at the two stair end posts", side="l")
    return d.svg("Inline post")


def splice():
    d = D(-2, 56, -13, 6, 13, "sp")
    d.rect(0, 0, 16, RH, "steel ob")
    d.rect(16, 0, 32, RH, "steel ob")
    d.rect(0, RT, 32, RH - RT, "void")
    d.rect(13, RT, 19, RT + SB_T, "coral ob")
    d.rect(11.5, -PLT, 20.5, 0, "coral ob")
    d.rect(14.5, -12, 17.5, -PLT, "steel ob")
    d.rect(14.5 + 0.1875, -12, 17.5 - 0.1875, -PLT, "void")
    for u in (13.5, 14.5, 17.5, 18.5):
        d.line(u, -0.6, u, RT + SB_T - 0.1, "lag")
    d.dim((13, RH), (19, RH), 1.2, '6" spline over a post, 12" mid-span')
    d.dim((13.5, -PLT), (18.5, -PLT), -1.4, '1-1/2 and 2-1/2 each side of the joint')
    d.tag(16, 1.6, 36, 4.6, "1", "Rail ends cut square and butted tight")
    d.tag(17, RT + 0.25, 36, 2.2, "2", "PL 1/2 x 2-1/4 spline, chamfered 5/16 x 45|removable, cold galvanized")
    d.tag(14.5, -0.9, 36, -5.5, "3", "(4) screws tapped into the spline", side="l")
    return d.svg("Splice")


def flat_corner():
    d = D(-16, 30, -2.5, 16, 14, "fc")
    d.poly([(-14, 0), (1.5, 0), (-1.5, 3), (-14, 3)], "steel ob")
    d.poly([(1.5, 0), (1.5, 14), (-1.5, 14), (-1.5, 3)], "steel ob")
    d.rect(-1.5, 0, 1.5, 3, "hid")
    d.pline([(-5, 0.375), (1.125, 0.375), (1.125, 8), (-1.125, 8), (-1.125, 2.625), (-5, 2.625), (-5, 0.375)], "hidp")
    for p in ((-4, 1.5), (-2, 1.5), (0, 4), (0, 6)):
        d.circle(p[0], p[1], 0.19, "coral ob")
    d.circle(1.5, 0, 0.3, "redc")
    d.circle(-1.5, 3, 0.3, "redc")
    d.dim((-5, 2.625), (1.125, 2.625), 1.0, '5" legs')
    d.tag(1.5, 0, 8, -1.2, "1", "Miter runs outside corner to inside corner")
    d.tag(0, 5, 8, 12, "2", "L spline, two 1/2 x 2-1/4 bars|mitered, welded and ground flush")
    d.tag(-3, 1.5, 8, 6, "3", "(2) screws per leg, up through the rail bottom")
    return d.svg("Flat corner")


# ================================================================= R-502
def compound_corner():
    d = D(-16, 44, -2.5, 17, 11, "cc")
    d.poly([(-14, 0), (1.05, 0), (-1.05, 3), (-14, 3)], "steel ob")
    d.poly([(1.05, 0), (5.84, 13.16), (3.74, 16.16), (-1.05, 3)], "steel ob")
    d.rect(-1.5, 0, 1.5, 3, "hid")
    d.poly([(-5, 0.375), (0.9, 0.375), (1.058, 1.115), (2.768, 5.815), (0.652, 6.585), (-1.058, 1.885), (-1.1, 2.625), (-5, 2.625)], "hidp")
    for p in ((-2, 1.5), (-4.5, 1.5), (0.684, 3.38), (1.539, 5.73)):
        d.circle(p[0], p[1], 0.19, "coral ob")
    d.circle(1.05, 0, 0.3, "redc")
    d.circle(-1.05, 3, 0.3, "redc")
    d.add(f'<path d="M {d.X(-6):.1f} {d.Y(1.5):.1f} A {(6*d.S):.1f} {(6*d.S):.1f} 0 0 0 {d.X(-6*0.342):.1f} {d.Y(1.5+6*0.940):.1f}" class="dl" fill="none"/>')
    d.text(-7.5, 4.5, "110", "dt", "middle")
    d.tag(0, 1.5, 8, -1.4, "1", "Both rails mitred 35°, blade tilted about 4°, closed face outboard")
    d.tag(1.9, 4.5, 8, 5, "2", "Compound L spline inside both rails (hidden)")
    d.tag(-4.5, 1.5, 8, 8.5, "3", "(2) screws per leg, up through the rail bottom")
    d.tag(-1.2, 0.4, 8, 12, "4", "Corner post under the miter")
    return d.svg("Compound corner, 110 degrees, plan")


def compound_spline():
    d = D(-2, 40, -2.5, 4.5, 20, "cs")
    d.rect(0, 0, 5, 0.5, "steel ob")
    import math as _m
    t = _m.radians(4.5)
    x1, y1 = 5 + 5 * _m.cos(t), 5 * _m.sin(t)
    d.poly([(5, 0), (x1, y1), (x1 - 0.5 * _m.sin(t), y1 + 0.5 * _m.cos(t)), (5, 0.5)], "steel ob")
    d.line(5, -0.6, 5, 1.2, "cl")
    for x in (2.5, 0.5):
        d.circle(x, 0.25, 0.12, "nut")
    for s in (2.0, 4.5):
        d.circle(5 + s * _m.cos(t), s * _m.sin(t) + 0.25, 0.12, "nut")
    d.line(5, 0, 11, 0, "thin")
    d.dim((0, 0), (5, 0), -1.0, '5 level leg')
    d.dim((5, -0.4), (x1, y1 - 0.4), -1.0, '5 raked leg')
    d.text(8.2, 1.3, "4.5°", "sm", "middle")
    d.tag(5, 0.3, 15, 3.4, "1", "1/2 x 2-1/4 bar, same stock as every spline")
    d.tag(7.5, 0.45, 15, 1.8, "2", "Legs welded at 110° in plan, raked leg up 4.5°")
    d.tag(2.5, 0.25, 15, 0.2, "3", "1/4-20 tapped at 2 and 4-1/2 from the corner")
    d.tag(9.5, 0.6, 15, -1.4, "4", "Build to the angle measured at dry fit")
    return d.svg("Compound corner spline, elevation")


def transition():
    d = D(52, 136, 28, 92, 7.2, "tr")
    d.rect(X_WALL, 30, X_WALL + 12, TOTAL_RISE, "CC ob")
    d.line(X_WALL + 12, TOTAL_RISE, 96, TOTAL_RISE, "grade")
    clip = 56
    d.poly([(clip, s_top(clip)), (X_END, YT), (X_END, YB), (clip, s_top(clip) - DV)], "steel ob")
    d.line(clip, s_top(clip) + 0.8, clip, s_top(clip) - DV - 0.8, "brk")
    for n in (6, 7):
        x0, top = T * (n - 1), R * n
        d.rect(x0, top - WOOD, x0 + T, top, "WD ob")
    d.add(f'<rect x="0" y="0" width="{d.X(clip):.1f}" height="{d.H:.0f}" class="paper"/>')
    GH = TOTAL_RISE + 36
    d.poly([(52, GH - (RUN - 52) * SL - RH), (RUN, GH - RH), (RUN, GH), (52, GH - (RUN - 52) * SL)], "coral ob")
    d.rect(RUN, GH - RH, 92, GH, "coral ob")
    for c, b in ((69.0, TOTAL_RISE + 0.375), (81.75, TOTAL_RISE + 0.375)):
        d.rect(c - 1.5, b, c + 1.5, GH - RH - PLT, "steel ob")
    d.pline([(RUN - 4.27, GH - RH - 0.6 - 2.61), (RUN, GH - RH - 0.6), (74, GH - RH - 0.6)], "hidp")
    d.dim((69.0, 44), (81.75, 44), -1.6, fr(12.75) + " post centres")
    d.dim((92, TOTAL_RISE), (92, GH), -1.6, '36')
    d.tag(RUN, GH - RH, 96, 58, "1", "Bend at the landing nosing, shop welded")
    d.tag(74, GH - RH - 0.6, 96, 54, "2", "Bent leg lands over the terminal post")
    d.tag(81.75, 50, 96, 44, "3", "Wall post, centred on the 6 in stem")
    return d.svg("Stair to level transition")


def raked_run():
    RISE, PLAN, NB5 = 15.5, 198.5, 5
    ang = math.degrees(math.atan(RISE / PLAN))
    d = D(-30, 380, -22, 64, 2.1, "rr")
    sl = RISE / PLAN
    d.pline([(-24, 0), (0, 0), (PLAN, RISE), (230, RISE)], "grade")
    posts = [PLAN / NB5 * i for i in range(NB5 + 1)]
    for i, x in enumerate(posts):
        g = x * sl
        d.rect(x - 1.5, g, x + 1.5, g + 36 - 2.25, "steel ob")
        d.rect(x - 4, g - 6, x + 4, g, "CC ob")
    d.poly([(-20, 36), (0, 36), (PLAN, 36 + RISE), (225, 36 + RISE), (225, 34 + RISE), (PLAN, 34 + RISE), (0, 34), (-20, 34)], "coral ob")
    for k in range(10):
        h = 2.6875 + 3.125 * k
        d.line(0, h, PLAN, RISE + h, "cable")
    d.dim((0, -8), (PLAN, -8), -3, fr(PLAN) + " plan, 5 bays at 39-11/16")
    d.dim((PLAN + 10, 0), (PLAN + 10, RISE), 0, fr(RISE) + " rise")
    d.text(PLAN / 2, 50, f"{ang:.1f}° rake", "sm", "middle")
    d.tag(posts[1], posts[1] * sl + 33.75, 236, 60, "1", "Top plates cut at 4.5°; posts plumb, one length")
    d.tag(posts[2], posts[2] * sl + 18, 236, 46, "2", "Intermediate holes square 3/8; ends at the rake")
    d.tag(posts[3], posts[3] * sl + 35, 236, 32, "3", "Two shop-welded segments, splice over post 3")
    d.tag(0, 35, 236, 18, "4", "110° compound corner at the low end")
    d.tag(PLAN, RISE + 35, 236, 4, "5", "Gate jamb at the high end")
    return d.svg("Raked run, 16 ft 6 in along the planter")


# ================================================================= R-503
def wall_spigot():
    d = D(-8, 44, -9, 22, 11, "ws")
    d.rect(-6, -9, 6, 0, "CC ob")
    d.rect(-3, 0, 3, 0.375, "coral ob")
    d.rect(-1.25, 0.375, 1.25, 10.375, "coral ob")
    d.rect(-1.5, 0.375, 1.5, 20, "steel ob")
    d.rect(-1.5 + 0.1875, 0.375, 1.5 - 0.1875, 20, "void")
    d.rect(-1.25, 0.375, 1.25, 10.375, "hid")
    d.line(0, -6, 0, 1.6, "rod")
    for b in (4.625, 7.75):
        d.line(-2, b, 2, b, "lag")
    for k in range(6):
        h = 0.375 + 2.6875 + 3.125 * k
        d.circle(0, h, 0.22 if h < 10.375 else 0.19, "void ob")
    d.circle(0, 0.6, 0.12, "coral ob")
    d.dim((3.6, 0.375), (3.6, 10.375), -1.2, '10 stem')
    d.dim((-3.6, 0.375), (-3.6, 4.625), 1.2, '4-1/4')
    d.dim((-5.4, 0.375), (-5.4, 7.75), 1.2, '7-3/8')
    d.dim((5.6, 0.375), (5.6, 3.0625), 1.2, '2-11/16')
    d.dim((-6, 0), (6, 0), -2.4, '6 x 6 x 3/8 plate')
    d.tag(0, -4, 8, -6, "1", '1/2 rod, 6 embed, on the wall centreline')
    d.tag(2, 7.375, 8, 18, "2", "(2) 3/8 through bolts, post and stem drilled together")
    d.tag(0, 12.4375, 8, 12, "3", "Cable holes at 3-1/8, 7/16 in the post.|The lowest three pass through the stem:|drill those 9/16 in the stem so the cable clears")
    d.text(-7.6, 21, "All post dimensions from the top of the plate.", "sm", "start")
    return d.svg("Wall spigot")


def handrail():
    d = D(-9, 40, -2, 11, 13, "hr")
    d.rect(-1.5, -2, 1.5, 7.5, "steel ob")
    d.rect(-1.5 + 0.1875, -2, 1.5 - 0.1875, 7.5, "void")
    d.rect(-1.5, 7.5, 1.5, 7.75, "coral ob")
    d.rect(-1.5, 7.75, 1.5, 9.75, "coral ob")
    d.rect(-1.75, 0.5, -1.5, 5.5, "coral ob")
    d.poly([(-1.75, 3.2), (-5.5, 3.2), (-5.5, 4.7), (-1.75, 4.7)], "coral ob")
    d.rect(-6.75, 3.15, -5.5, 4.65, "steel ob")
    for b in (1.5, 4.5):
        d.line(-2.2, b, 0, b, "lag")
    d.dim((-6.1, 6), (0, 6), 1.2, '3-1/2 projection')
    d.tag(-6.1, 3.9, 6, 9.5, "1", "HSS 1-1/2 square handrail")
    d.tag(-1.6, 1.5, 6, 1.5, "2", "(2) 1/4-20 into the tapped post face, 4 in centres")
    d.tag(1.5, 8.75, 6, 6, "3", "2x3 cap rail above, 36 to its top")
    return d.svg("Handrail bracket")


# ================================================================= R-504
def gate5():
    d = D(-8, 128, -10, 48, 5.6, "g5")
    d.line(-8, 0, 74, 0, "grade")
    d.rect(-3, 0, 0, 36, "steel ob")
    d.rect(63, 0, 66, 36, "steel ob")
    d.rect(0.5, 34, 62.5, 36, "coral ob")
    d.rect(0.5, 2, 3.5, 34, "coral ob")
    d.rect(59.5, 2, 62.5, 34, "coral ob")
    d.rect(0.5, 2, 62.5, 5, "coral ob")
    for i in range(10):
        h = 3.0625 + 3.125 * i
        if h < 33:
            d.line(3.5, h, 59.5, h, "cable")
    for y in (6, 18, 30):
        d.rect(-1, y, 1.5, y + 1.5, "nut")
    d.line(61, 2, 61, -3, "rod")
    d.dim((0.5, -1), (62.5, -1), -2.2, '59 leaf, 60 clear, posts at 63 centres')
    d.dim((70, 0), (70, 36), -1.6, '36')
    d.tag(30, 35, 76, 42, "1", "2x3 top rail, matching the fence")
    d.tag(2, 20, 76, 36, "2", "1x3 stiles and bottom rail, 3 in in the plane")
    d.tag(61, -2, 76, -5, "3", "Drop rod into a ground sleeve")
    return d.svg("Walk path gate, 5 ft")


def gate42():
    d = D(-8, 112, -10, 48, 6.2, "g4")
    d.line(-8, 0, 56, 0, "grade")
    d.rect(-3, 0, 0, 36, "steel ob")
    d.rect(45, 0, 48, 36, "steel ob")
    d.rect(0.5, 34, 44.5, 36, "coral ob")
    d.rect(0.5, 2, 3.5, 34, "coral ob")
    d.rect(41.5, 2, 44.5, 34, "coral ob")
    d.rect(0.5, 2, 44.5, 5, "coral ob")
    for i in range(10):
        h = 3.0625 + 3.125 * i
        if h < 33:
            d.line(3.5, h, 41.5, h, "cable")
    for y in (6, 18, 30):
        d.rect(-1, y, 1.5, y + 1.5, "nut")
    d.dim((0.5, -1), (44.5, -1), -2.2, '41 leaf, 42 clear')
    d.tag(22, 35, 60, 42, "1", "Guard rules apply: this gate closes a gap in a guard")
    d.tag(-1, 30, 60, 30, "2", "Hinges left ascending; swings away from the stair")
    return d.svg("Stairwell gate, 42 in")


def top_plates():
    d = D(-3, 58, -5, 7, 13, "tp")
    d.rect(0, 0, 9, 3, "steel ob")
    for x in (1.5, 7.5):
        d.circle(x, 1.5, 0.14, "void ob")
    d.rect(15, 0, 21, 3, "steel ob")
    for x in (16.5, 19.5):
        d.circle(x, 1.5, 0.14, "void ob")
    d.dim((0, 3), (9, 3), 1.2, '9" inline')
    d.dim((1.5, 0), (7.5, 0), -1.2, '6')
    d.dim((15, 3), (21, 3), 1.2, '6" end')
    d.dim((16.5, 0), (19.5, 0), -1.2, '3')
    d.dim((21, 0), (21, 3), -1.2, '3')
    d.tag(7.5, 1.5, 27, 5, "1", "PL 1/4 x 3, welded to the post top")
    d.tag(19.5, 1.5, 27, 1.5, "2", "(2) 9/32 holes; pancake screws up into the rail")
    d.tag(21, 0.5, 27, -2, "3", "Cut at the rake on stair posts, long point uphill")
    return d.svg("K-1 top plates")


def splines():
    d = D(-3, 62, -5, 6, 12, "sp")
    d.rect(0, 0, 6, 2.25, "steel ob")
    for x in (0.5, 1.5, 4.5, 5.5):
        d.circle(x, 1.125, 0.13, "nut")
    d.line(3, -0.6, 3, 2.85, "cl")
    d.rect(10, 0, 22, 2.25, "steel ob")
    for x in (11, 14, 18, 21):
        d.circle(x, 1.125, 0.13, "nut")
    d.line(16, -0.6, 16, 2.85, "cl")
    d.poly([(26.3125, 0), (27.9375, 0), (28.25, 0.3125), (28.25, 0.5), (26, 0.5), (26, 0.3125)], "steel ob")
    d.dim((0, 2.25), (6, 2.25), 1.2, '6" over a post')
    d.dim((10, 2.25), (22, 2.25), 1.2, '12" mid-span')
    d.dim((0, 0), (0, 2.25), 1.0, '2-1/4')
    d.dim((1.5, 0), (4.5, 0), -1.0, '3')
    d.dim((14, 0), (18, 0), -1.0, '4')
    d.dim((26, 0.5), (28.25, 0.5), 1.0, 'section')
    d.tag(4.5, 1.125, 32, 4, "1", "1/4-20 tapped, 4 per spline, at the joint centreline")
    d.tag(27, 0.1, 32, 1, "2", "PL 1/2 x 2-1/4; 5/16 x 45 chamfer both bottom edges")
    d.tag(20, 0.5, 32, -2, "3", "Cold galvanize after drilling; removable, never welded")
    return d.svg("K-2 straight splines")


def l_spline():
    d = D(-3, 40, -3, 8, 20, "ls")
    d.poly([(0.375, 0), (5, 0), (5, 2.25), (2.25, 2.25), (2.25, 5), (0, 5), (0, 0.375)], "steel ob")
    d.line(0.19, 0.19, 2.25, 2.25, "thin")
    for p in ((2, 1.125), (4.5, 1.125), (1.125, 2), (1.125, 4.5)):
        d.circle(p[0], p[1], 0.13, "nut")
    d.dim((0, 2.25), (5, 2.25), 0, '')
    d.dim((5, 0), (5, 2.25), -1.0, '2-1/4')
    d.dim((0, -0.2), (5, -0.2), -1.0, '5 leg')
    d.dim((-0.2, 0), (-0.2, 5), 1.0, '5 leg')
    d.tag(1.2, 1.2, 10, 6, "1", "Two bars mitred 45, full penetration weld, ground flush all faces")
    d.tag(0.2, 0.2, 10, 3.5, "2", "Outer corner clipped 3/8 to clear the rail miter")
    d.tag(4.5, 1.125, 10, 1, "3", "1/4-20 tapped at 2 and 4-1/2 from the corner")
    return d.svg("Corner L spline")


def small_parts():
    d = D(-3, 60, -4, 6, 13, "smp")
    d.rect(0, 0, 3, 2.25, "steel ob")
    for x in (0.75, 2.25):
        d.circle(x, 1.125, 0.13, "nut")
    d.dim((0, 2.25), (3, 2.25), 1.0, '3')
    d.rect(9, 0, 12, 2, "steel ob")
    d.circle(10.5, 0.3, 0.07, "void ob")
    d.dim((9, 2), (12, 2), 1.0, '3')
    d.dim((12, 0), (12, 2), -1.0, '2')
    d.tag(1.5, 1.8, 18, 4, "1", "K-3 backing bar, 1/2 x 2-1/4 x 3, tapped twice, cold galvanized")
    d.tag(10.5, 0.3, 18, 0.5, "2", "K-4 end cap, 1/8 plate, welded and ground; 1/8 weep at the low edge")
    return d.svg("Backing bar and end cap")


def spigots():
    d = D(-8, 70, -4, 13, 13, "sg")
    # wall spigot elevation
    d.rect(-3, 0, 3, 0.375, "steel ob")
    d.rect(-1.25, 0.375, 1.25, 10.375, "steel ob")
    for b in (4.25, 7.375):
        d.circle(0, b + 0.375, 0.22, "void ob")
    for k in range(3):
        d.circle(0, 0.375 + 2.6875 + 3.125 * k, 0.28, "void ob")
    d.circle(0, 0.9, 0.1, "void ob")
    d.dim((3, 0.375), (3, 10.375), -1.2, '10 stem')
    d.dim((5, 0.375), (5, 3.0625), 1.2, '2-11/16')
    d.dim((5, 3.0625), (5, 6.1875), 1.2, '3-1/8')
    d.dim((-3, 0.375), (-3, 4.625), 1.2, '4-1/4')
    d.dim((-3, 4.625), (-3, 7.75), 1.2, '3-1/8')
    d.dim((-3, 0), (3, 0), -1.2, '6')
    d.text(0, -2.6, "wall spigot", "sm", "middle")
    # hinge spigot plan
    d.rect(10, 1, 22, 6, "steel ob")
    for x in (13, 19):
        d.circle(x, 3.5, 0.28, "void ob")
    d.rect(14.75, 2.25, 17.25, 4.75, "hid")
    d.dim((10, 6), (22, 6), 1.2, '12')
    d.dim((13, 1), (19, 1), -1.2, '6 rod centres')
    d.dim((22, 1), (22, 6), -1.2, '5')
    d.text(16, -2.6, "hinge-post plate, plan", "sm", "middle")
    # tread stem
    d.rect(28, 0, 30.5, 7, "steel ob")
    for b in (2.5, 5.75):
        d.circle(29.25, b, 0.22, "void ob")
    d.circle(29.25, 0.4, 0.09, "void ob")
    d.dim((30.5, 0), (30.5, 7), -1.2, '7')
    d.dim((27.5, 0), (27.5, 2.5), 1.0, '2-1/2')
    d.dim((27.5, 2.5), (27.5, 5.75), 1.0, '3-1/4')
    d.text(29.25, -2.6, "tread stem", "sm", "middle")
    d.tag(0, 9.4, 38, 11, "1", "HSS 2-1/2 sq x 3/16 stems. Bolt holes 7/16 both faces;|cable holes 9/16 in the stem, oversize to the post's 7/16")
    d.tag(1.5, 0.2, 38, 8, "2", "PL 6 x 6 x 3/8, one 9/16 hole for the rod on the wall centreline")
    d.tag(19, 3.5, 38, 5, "3", "Hinge posts: PL 5 x 12 x 3/8, two rods along the wall")
    d.tag(29.25, 0.4, 38, 2, "4", "3/16 drain just above the weld on every stem")
    return d.svg("Spigots and stems")


def bracket():
    d = D(-4, 50, -3, 8, 18, "br")
    d.rect(0, 0, 0.25, 5, "steel ob")
    for y in (0.5, 4.5):
        d.rect(-0.05, y - 0.14, 0.3, y + 0.14, "void ob")
    d.poly([(0.25, 3.2), (3.5, 3.2), (3.5, 4.7), (0.25, 4.7)], "steel ob")
    d.rect(3.5, 3.2, 5.0, 4.7, "steel ob")
    d.dim((0, 5), (4.25, 5), 1.0, '3-1/2 to rail ℄')
    d.dim((0, 0.5), (0, 4.5), 1.2, '4')
    d.dim((0.25, 0), (0.25, 5), -0.8, '5')
    d.tag(0.12, 2.5, 12, 6, "1", "PL 1/4 x 2-1/2 x 5, (2) 9/32 holes slotted 1/16")
    d.tag(2, 4, 12, 3.5, "2", "Arm 3/8 x 1-1/2, welded to the base and the rail")
    d.tag(4.25, 3.95, 12, 1, "3", "1-1/2 square handrail; bracket and rail are one weldment")
    return d.svg("K-8 handrail bracket")


# ================================================================= content
holds = """
<div class="cols">
<section>
<h3>Design basis</h3>
<table class="kv">
<tr><td>Codes</td><td>2018 IRC R312 and R311.7.8; IBC referenced for structural design and special inspection</td></tr>
<tr><td>Guard height</td><td>36" above the walking surface, 36" above the nosing line on flights</td></tr>
<tr><td>Handrail</td><td>Required on flights of 4+ risers. A 2x3 cap rail is not graspable; a separate 1-1/2 square rail is provided</td></tr>
<tr><td>Infill</td><td>10 cables, 4" sphere where the run is a guard</td></tr>
<tr><td>Loads</td><td>200 lb in any direction at the top, 50 plf, plus sustained cable tension of about 200 lb per cable on guard runs</td></tr>
<tr><td>Model</td><td>Every post is propped by the continuous top rail. Base moments are small; base shear is what governs</td></tr>
</table>
</section>
<section>
<h3>Hold points</h3>
<ol class="holds">
<li><b>Cables last.</b> The rail must be installed, spliced over posts with its splines, and anchored at both ends of every run before any cable is tensioned. Tensioning against an unbraced post makes it a cantilever carrying roughly 45,000 in-lb, which no spigot here will hold. Cables come off first for any later work.</li>
<li><b>Master bath run tension.</b> The master bath landing and stair guard run is tensioned to about 100 lb per cable, half the 200 lb used elsewhere. Its spans are about half as long, so it needs half the tension to pass the 4 in sphere, and the lower tension limits the one-sided pull on the master bath stair tread 1.</li>
<li><b>Raked run.</b> The 16 ft 6 in run along the planter climbs 15-1/2 in at about 4.5 degrees, rail parallel to the walk. Posts are plumb and one length with top plates cut at the rake. The survey confirms the exact rise and angle.</li>
<li><b>Guard extent.</b> Guard from the stair opening to the 110 degree corner. Everything past that corner is garden fence: same parts, no code obligation, cable tension reduced to snug.</li>
<li><b>Post schedule is provisional</b> pending the field survey on S-002 of the stair set.</li>
<li><b>Engineer review</b> of the wall spigots at reduced embedment in a 6 in stem, the cable tension load cases, and the stem-to-end-tube weld at the tread posts.</li>
</ol>
</section>
</div>
"""

posts = """
<div class="scroll"><table class="grid">
<thead><tr><th>Type</th><th>Where</th><th>Length</th><th>Base</th><th>Holes</th></tr></thead>
<tbody>
<tr><td>P-A</td><td>Stair posts, treads 1 and 4</td><td>38-15/16</td><td>Stem welded to the tread frame end tube</td><td>10 cable at the rake from 6-3/16 at 3-3/8; bolts at 2-1/2 and 5-3/4; handrail taps at 33 and 37</td></tr>
<tr><td>P-B</td><td>Stair post, landing tread</td><td>35-1/2</td><td>Stem welded to the landing tread frame</td><td>Stair face raked from 3-11/16; level face square from 4-13/16; each offset 3/4 off centre</td></tr>
<tr><td>P-C</td><td>Level posts on the wall</td><td>33-3/8</td><td>Wall spigot, 6x6 plate, 1/2 rod at 6 embed</td><td>10 cable square from 2-11/16 at 3-1/8; bolts at 4-1/4 and 7-3/8</td></tr>
<tr><td>P-D</td><td>Level posts on piers</td><td>33-3/8</td><td>Spigot embedded in the pier, 9 exposed</td><td>As P-C</td></tr>
<tr><td>P-E</td><td>Gate jamb posts</td><td>33-3/8</td><td>As P-C or P-D; hinge posts get a 5x12 plate with two rods</td><td>As P-C, plus hinge and latch fixings</td></tr>
<tr><td>P-F</td><td>Raked run posts</td><td>33-3/8, all equal</td><td>Pier or wall spigot</td><td>Top plate cut at 4.5 deg; intermediate cable holes square at 3/8; end posts drilled at the rake</td></tr>
</tbody>
<tfoot><tr><td colspan="5">Quantities and individual lengths follow the field survey. Post spacing 48 in maximum, measured on the rake.</td></tr></tfoot>
</table></div>
"""

parts = """
<div class="scroll"><table class="grid">
<thead><tr><th>Mark</th><th>Item</th><th>Spec</th></tr></thead>
<tbody>
<tr><td>K-1</td><td>Top plate</td><td>PL 1/4 x 3; 9 in at inline posts, 6 in at end posts; cut at the rake where the rail rakes, long point uphill</td></tr>
<tr><td>K-2</td><td>Spline</td><td>PL 1/2 x 2-1/4, chamfered 5/16 x 45 both bottom edges; 6 in over a post, 12 in mid-span; cold galvanized; removable</td></tr>
<tr><td>K-2c</td><td>Compound corner spline</td><td>Two 1/2 x 2-1/4 bars, 5 in legs, welded at 110 deg in plan with the raked leg up 4.5 deg, four taps; built to the angle measured at dry fit</td></tr>
<tr><td>K-3</td><td>Backing bar</td><td>3 in of the same stock, tapped, at mitered rail ends</td></tr>
<tr><td>K-4</td><td>End cap</td><td>1/8 in plate welded and ground; rail runs 3 in past the end post; 1/8 in weep at the low end</td></tr>
<tr><td>K-5</td><td>Wall spigot</td><td>PL 6 x 6 x 3/8, 10 in stem of HSS 2-1/2x2-1/2x3/16, one 1/2 in 316 rod at 6 in embed in SET-3G; horseshoe shims at the rod to level, bedded in construction adhesive</td></tr>
<tr><td>K-6</td><td>Tread stem</td><td>HSS 2-1/2 x 2-1/2 x 3/16 x 7, welded to the 3 in end tube of the tread frame; both planks notched at each end around the post; see S-104</td></tr>
<tr><td>K-8</td><td>Handrail bracket</td><td>3/8 x 1-1/2 arm on PL 1/4 x 2-1/2 x 5, holes at 4 in centres slotted 1/16</td></tr>
<tr><td>H-1</td><td>Rail screws</td><td>1/4-20 x 3/4 pancake head, black oxide 304, thread-formed into the rail wall</td></tr>
<tr><td>H-2</td><td>Through bolts</td><td>3/8-16 x 4-1/2 type 316, two per post</td></tr>
<tr><td>H-3</td><td>Cable</td><td>1/8 in 1x19 type 316; Muzata CB04 and CB17 at end posts, CR90 at level intermediates, bare angled holes at stair intermediates, CR60 washers at stair end posts</td></tr>
</tbody></table></div>
"""

cables = """
<div class="scroll"><table class="grid">
<thead><tr><th></th><th>Level runs</th><th>Stair flights</th></tr></thead>
<tbody>
<tr><td>Runs</td><td>10</td><td>10</td></tr>
<tr><td>Spacing, perpendicular</td><td>3-1/8</td><td>2-7/8</td></tr>
<tr><td>Spacing, vertical on a plumb post</td><td>3-1/8</td><td>3-3/8</td></tr>
<tr><td>First hole above the post base</td><td>2-11/16</td><td>6-3/16</td></tr>
<tr><td>Last hole above the post base</td><td>30-13/16</td><td>36-9/16</td></tr>
<tr><td>Drilled</td><td>square</td><td>at 31.43 degrees</td></tr>
<tr><td>Tension</td><td colspan="2">About 200 lb per cable on guard runs; about 100 lb on the master bath run; snug, about 75 lb, on garden fence runs</td></tr>
<tr><td>Check</td><td colspan="2">The lowest stair cable sits 1 in above the nosing line and clears each nosing by 3/4 in. Pull a string line at that height before drilling.</td></tr>
</tbody></table></div>
"""

html_sheets = [
    sheet("R-001", "General notes and hold points", holds),
    sheet("R-501", "Rail connections", fig(inline_post(), "Rail fixed down at every post; four screws at the two stair end posts where the rail carries thrust.", "big") + fig(splice(), "Splices land over a post wherever possible. Mid-span splices use a 12 in spline.", "big") + fig(flat_corner(), "Flat corner, any angle. The spline makes the corner continuous.", "big")),
    sheet("R-502", "Compound corner", fig(compound_corner(), "The 110 degree corner where the run turns and begins to rake. Both changes happen at the corner post, inside the spline.", "big") + fig(compound_spline(), "Compound corner spline. Cold-galvanize after welding, same as every spline.", "big")),
    sheet("R-509", "Raked run", fig(raked_run(), "The walk climbs 15-1/2 in over the run and the rail climbs with it, staying 36 in above the walk. No steps in the rail anywhere on this job.", "big")),
    sheet("R-505", "Stair to level transition", fig(transition(), "Stair to level at the head of the upper flight. The stair rail is one shop-welded piece through the bend.", "big")),
    sheet("R-503", "Bases and handrail", fig(wall_spigot(), "Wall spigot. Cable holes pass through the stem; drill post and stem together.", "big") + fig(handrail(), "Handrail bracket, 34 in above the nosing line, left side ascending.", "big")),
    sheet("R-504", "Gates", fig(gate5(), "Walk path gate. Garden fence, so infill is by choice rather than code.", "big") + fig(gate42(), "Stairwell gate. Closes a gap in a required guard, so guard rules follow it.", "big")),
    sheet("R-506", "Rail parts", fig(top_plates(), "Top plates, all posts.", "big") + fig(splines(), "Straight splines. Screws land at the joint centreline, two each side.", "big")),
    sheet("R-507", "Corner and small parts", fig(l_spline(), "Corner spline for flat corners. Odd-angle corners use the same bar mitred at half the turn.", "big") + fig(small_parts(), "Backing bar and end cap.", "big")),
    sheet("R-508", "Spigots, stems and bracket", fig(spigots(), "Wall spigot, hinge-post plate and the tread stem.", "big") + fig(bracket(), "Handrail bracket, left side ascending.", "big")),
    sheet("R-601", "Schedules", "<h3>Post schedule</h3>" + posts + "<h3>Components and hardware</h3>" + parts + "<h3>Cable schedule</h3>" + cables),
]

nav = "".join(f'<a href="#s{n}"><b>{n}</b>{t}</a>' for n, t in SHEETS)
css = open('css.txt').read() + """
.coral{fill:var(--steeld)}
.hidp{stroke:var(--mark);stroke-width:1.2;stroke-dasharray:5 3;fill:none}
.redc{fill:none;stroke:var(--hold);stroke-width:1.6}
.cable{stroke:#1D9E75;stroke-width:1.1}
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cable rail — preliminary drawing set, rev A</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Cable rail,<br>guard, fence and gates</h1>
<p>Rev A. Connections, bases, gates and schedules for the 3x3 post and 2x3 rail system. Companion to the mono stringer stair set. Post quantities and individual lengths follow the field survey.</p></div>
<div class="stamp">PRELIMINARY<br>not for construction<br>engineer review required</div></header>
<nav aria-label="Sheets">{nav}</nav>
<main>{''.join(html_sheets)}</main></body></html>"""

open("out/cable-rail-drawings.html", "w").write(html)
print("ok")

import json
open("part_R.html", "w").write("".join(html_sheets))
json.dump(SHEETS, open("part_R.json", "w"))


