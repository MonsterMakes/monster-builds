import math, re
from fractions import Fraction

exec(open('head.py').read())

# ---------------------------------------------------------------- revised geometry
SW = 6.0            # stub depth in the run direction (rev P)
MEM = 2.5           # F1 and F2 member width, plain treads
MEMP = 3.0          # F2 member width, post treads
WALLT = 0.1875      # F1, F2 wall
CH = (11.25 - 2 * MEM) / 2   # half the collar length, notch-free pocket
BSP = 4.0           # through-bolt spacing, across the stair
SH = SW / 2
CM_W, CM_H = 3.0, 2.5    # crossmember, run width x height
POSTS = (1, 4, 7)
TW = 48.0              # tread width
THW = TW / 2
POST_U = THW - 1.5     # post centreline from tread centreline, across the width
TP, BP_L = 3.0, 8.0    # top plate 3x3, bottom plate 3x8
PLT_T = 0.375
LAG_S = 3.0
PL_T = 0.375
SAD_DEPTH = 9.0
STUB_LONG = STUB_CL + SH * SL
STUB_SHORT = STUB_CL - SH * SL
X_NOSE = T * N + CM_W / 2       # landing crossmember centre, 69.0
BAR_T = 0.25                    # bearing bar at tread 1
WP_TOP = WP_C + 6
WP_BOT = WP_TOP - 16
AN_X = 4.5
AN_Y = (WP_TOP - 4, WP_TOP - 9, WP_TOP - 14)
POST_OUT = 25.5                 # post centreline from tread centreline
CM_LEN = 2 * (POST_OUT + 1.25)  # 53.5
STUB_UP = 10.0                  # post stub above crossmember top


def sad_top(n):
    return R * n - 1.75 - PL          # underside of the centre plate


def sad_bot(n):
    return sad_top(n) - PAD           # top of the stub


def cm_bot(n):
    return sad_top(n)


def cm_c(n):
    return 69.0 if n == NB else xc(n)


def st_top(n):
    return sad_bot(n)


def plates(n):
    return [(xc(n) - 4, xc(n) + 4)]


def sad_span(n):
    return (xc(n) - CH, xc(n) + CH)


def draw_wall(d):
    d.rect(X_WALL, -14, X_WALL + 12, TOTAL_RISE, "CC ob")
    d.line(X_WALL + 12, TOTAL_RISE, X_WALL + 16, TOTAL_RISE, "grade")


def draw_tread(d, n, stubs=True):
    x0, top = T * (n - 1), R * n
    fb = top - WOOD
    d.rect(x0, fb, x0 + T, top - 1.75, "steel ob")
    d.rect(x0, top - 1.75, x0 + 5.5, top, "WD ob")
    d.rect(x0 + 5.6875, top - 1.75, x0 + T, top, "WD ob")
    d.rect(xc(n) - CH, top - 1.75 - PL, xc(n) + CH, top - 1.75, "hid")
    d.rect(xc(n) - CH, fb, xc(n) + CH, top - 1.75 - PL, "hid")
    if not stubs:
        return
    if n == 1:
        d.rect(xc(n) - SH, BP_TOP, xc(n) + SH, fb, "steel ob")
        d.rect(xc(n) - SH, fb, xc(n) + SH, sad_bot(n), "hid")
        return
    c = xc(n)
    d.poly([(c - SH, fb), (c + SH, fb), (c + SH, s_top(c + SH)), (c - SH, s_top(c - SH))], "steel ob")
    d.rect(c - SH, fb, c + SH, sad_bot(n), "hid")


def draw_stringer(d):
    d.poly([(XT, BP_TOP), (X_END, YT), (X_END, YB), (XB, BP_TOP)], "steel ob")


def draw_base(d):
    d.rect(-1.5, BP_BOT, 28.5, BP_TOP, "steel ob")
    for rx in RODS_X:
        d.line(rx, -6, rx, BP_TOP + 1.0, "rod")
        d.rect(rx - 1, BP_TOP, rx + 1, BP_TOP + 0.25, "steel ob")
        d.rect(rx - 0.55, BP_TOP + 0.25, rx + 0.55, BP_TOP + 0.85, "nut")


def draw_wallplate(d):
    d.rect(X_END, WP_BOT, X_WALL, WP_TOP, "steel ob")
    for yy in AN_Y:
        d.line(X_WALL - 0.9, yy, X_WALL + 5.5, yy, "rod")


# ================================================================= S-101
def side_elev():
    d = D(-17, 120, -15, 72, 8.0, "se")
    d.line(-17, 0, X_WALL, 0, "grade")
    d.rect(-17, -2.2, X_WALL, 0, "GR none")
    d.rect(4, -13, 30, -0.02, "hid")
    d.text(17, -11.6, "existing pier below pavers", "sm", "middle")
    draw_wall(d)
    draw_base(d)
    draw_stringer(d)
    for n in range(1, NB + 1):
        draw_tread(d, n)
    draw_wallplate(d)
    for n in POSTS:
        c = cm_c(n)
        d.rect(c - 1.5, R * n - 1.75, c + 1.5, R * n + 22, "hid")
    d.line(-3, -3 * SL + R, X_WALL + 3, (X_WALL + 3) * SL + R, "cl")
    d.text(26, 26 * SL + R, "nosing line", "sm", "middle", dy=-6, rot=-DEG)
    for i in range(7):
        d.dim((-4, R * (i + 1)), (-4, R * i), -2.5, fr(R))
    d.dim((-4, TOTAL_RISE), (-4, 0), -10, fr(TOTAL_RISE) + " total rise")
    for i in range(NB):
        d.dim((T * i, R * (i + 1)), (T * (i + 1), R * (i + 1)), 57 - R * (i + 1), fr(T) if i < N else "landing")
    d.dim((0, R), (RUN, R), 61.5 - R, fr(RUN) + " run, nosing to landing nosing")
    d.dim((0, R), (X_WALL, R), 65.5 - R, fr(X_WALL) + " first riser to wall face")
    r = 80
    cx, cy = d.X(T * 3), d.Y(R * 4)
    d.add(f'<path d="M {cx+r:.1f} {cy:.1f} A {r} {r} 0 0 0 {cx+r*COS:.1f} {cy-r*SIN:.1f}" class="dl" fill="none"/>')
    d.text(T * 3, R * 4, f"{DEG:.2f}°", "dt", "start", dx=r + 5, dy=-10)
    px = 45
    d.dim((px, s_top(px)), (px + 8 * SIN, s_top(px) - 8 * COS), 4, '8"')
    d.text(X_WALL + 13, TOTAL_RISE, f"T.O. wall = landing tread +{fr(TOTAL_RISE)}", "sm", "start", dy=14)
    d.text(-16.5, 0, "finish grade ±0, M4 bears direct", "sm", "start", dy=-5)
    d.tag(xc(2) - 2, R * 2 - 1.6, 2, 22, "W1", 'tread frame + ash planks (×7)')
    d.tag(xc(5) + 1, s_top(xc(5) + 1) + 1.2, 2, 34, "M2", "HSS 6×4×1/4 stub (×6)|6\" at ℄, all identical")
    d.tag(xc(3) + 1.5, R * 3 - 3.6, 2, 28, "M8", "stub between two collars under each tread (×7)")
    d.tag(xc(4), R * 4 + 10, 2, 47, "G", "guard posts centred on treads 1 and 4;|landing post in line with the nose, see S-104")
    d.tag(55, s_top(55) - 4.6, 42, 6, "M1", "HSS 8×4×1/4 mono stringer|long point " + fr(LONG_PT))
    d.tag(20, BP_TOP - 0.2, 36, -4, "M4", "base PL 1/2×12×30 on grade")
    d.tag(xc(1), 1.6, 36, -8, "M2b", "tread 1 stub on M4, 6 in the run")
    d.tag(RODS_X[1], -4, 36, -11.5, "A2", "existing all-thread (4), measured")
    d.tag(X_WALL - 0.25, WP_BOT + 1.5, 96, 22, "M6", "wall PL 1/2×12×16")
    d.tag(X_WALL + 4, AN_Y[0], 96, 38, "A1", '1/2" adhesive anchors (6)')
    return d.svg("Side elevation")


# ================================================================= S-102
def plan():
    d = D(-14, 98, -44, 40, 7.8, "pl")
    d.rect(X_WALL, -30, X_WALL + 12, 30, "CC ob")
    d.rect(-1.5, -6, 28.5, 6, "hid")
    for rx in RODS_X:
        for u in (-RODS_U, RODS_U):
            d.circle(rx, u, 0.5, "hidc")
    d.rect(XT, -2, X_END, 2, "hid")
    for n in range(1, NB + 1):
        a, b = sad_span(n)
        d.rect(a, -4, b, 4, "hid")
        if n != 1:
            d.rect(xc(n) - SH, -2, xc(n) + SH, 2, "hid")
    d.rect(X_END, -6, X_WALL, 6, "hid")
    for n in range(1, NB + 1):
        x0 = T * (n - 1)
        d.rect(x0, -THW, x0 + T, THW, "wdplan ob")
        for a, b in ((-THW, -THW + 3), (THW - 3, THW)):
            d.rect(x0, a, x0 + T, b, "hid")
        d.text(x0 + T / 2, THW - 4.5, f"{n}" if n <= N else "L", "tn", "middle")
    for n in POSTS:
        for u in (-POST_U, POST_U):
            d.rect(cm_c(n) - 1.5, u - 1.5, cm_c(n) + 1.5, u + 1.5, "steel ob")
    d.line(-10, 0, X_WALL + 14, 0, "cl")
    d.add(f'<line x1="{d.X(6):.1f}" y1="{d.Y(-THW+5):.1f}" x2="{d.X(58):.1f}" y2="{d.Y(-THW+5):.1f}" class="arw"/>')
    d.poly([(58, -THW + 6.2), (61, -THW + 5), (58, -THW + 3.8)], "arwh")
    d.text(32, -THW + 5, "UP, 7 risers", "sm", "middle", dy=-6)
    d.dim((0, -THW), (0, THW), 6.5, fr(TW) + " tread")
    d.dim((xc(2) - CH, THW), (xc(2) + CH, THW), 2.4, '6-1/4 plate and collars')
    d.dim((xc(4), THW), (xc(4), POST_U), -2.4, fr(THW - POST_U))
    d.dim((xc(2), -THW), (xc(2), -THW + 3), -2.4, '3" end tube')
    for i in range(NB):
        d.dim((T * i, -THW), (T * (i + 1), -THW), -3.2, fr(T))
    d.dim((0, -THW), (RUN, -THW), -7.2, fr(RUN) + " run")
    d.dim((0, -THW), (X_WALL, -THW), -11, fr(X_WALL) + " to wall face")
    d.text(X_WALL + 6, 28, "retaining wall", "sm", "middle")
    d.text(xc(3), 9, "plate and collars", "sm", "middle")
    d.text(30, -THW + 12, "base PL and rods below", "sm", "start")
    d.text(xc(2), THW + 9, "guard posts at treads 1, 4 and the landing", "sm", "middle")
    return d.svg("Plan")


# ================================================================= S-103
def setout():
    d = D(-8, 136, -34, 62, 7.3, "so")
    d.line(-8, 0, X_WALL, 0, "grade")
    d.rect(-8, -2.2, X_WALL, 0, "GR none")
    draw_wall(d)
    draw_base(d)
    draw_stringer(d)
    draw_wallplate(d)
    for n in range(1, NB + 1):
        d.rect(T * (n - 1), R * n - WOOD, T * n, R * n, "hid")
    d.line(-3, -3 * SL + R, X_WALL + 3, (X_WALL + 3) * SL + R, "cl")
    d.line(X_WALL, TOTAL_RISE, X_WALL + 34, TOTAL_RISE, "thin")
    d.line(X_WALL, -30, X_WALL, 0, "thin")
    d.text(X_WALL + 1, TOTAL_RISE, "datum: top of wall", "sm", "start", dy=-8)
    d.text(X_WALL, -31, "datum: wall face", "sm", "middle")
    # vertical chain, right of the wall
    xv = X_WALL + 20
    for y in (WP_TOP, AN_Y[0], AN_Y[1], AN_Y[2], WP_BOT):
        d.line(X_WALL + 12, y, xv, y, "thin")
    d.dim((xv, TOTAL_RISE), (xv, WP_TOP), 2.0, fr(TOTAL_RISE - WP_TOP) + " wall PL top")
    d.dim((xv, TOTAL_RISE), (xv, AN_Y[0]), 6.5, fr(TOTAL_RISE - AN_Y[0]) + " anchor row 1")
    d.dim((xv, TOTAL_RISE), (xv, AN_Y[1]), 11.0, fr(TOTAL_RISE - AN_Y[1]) + " anchor row 2")
    d.dim((xv, TOTAL_RISE), (xv, AN_Y[2]), 15.5, fr(TOTAL_RISE - AN_Y[2]) + " anchor row 3")
    d.dim((xv, TOTAL_RISE), (xv, WP_BOT), 20.0, fr(TOTAL_RISE - WP_BOT) + " wall PL bottom")
    d.line(X_END, YT, 69, YT, "thin")
    d.line(X_END, YB, 69, YB, "thin")
    d.line(X_WALL, TOTAL_RISE, 62, TOTAL_RISE, "thin")
    d.dim((70, TOTAL_RISE), (70, YT), -2.0, fr(TOTAL_RISE - YT) + " to stringer top")
    d.dim((66, TOTAL_RISE), (66, YB), -2.0, fr(TOTAL_RISE - YB) + " to stringer bottom")
    # horizontal chain, below grade
    for x, off, lab in ((28.5, -4.5, "base PL, uphill end"), (XB, -8.5, "stringer bottom toe"),
                        (XT, -12.5, "stringer top toe"), (0.5, -16.5, "base PL, downhill end"),
                        (0.0, -20.5, "first riser")):
        d.line(x, 0.2, x, off + 1.2, "thin")
        d.dim((X_WALL, off), (x, off), 0, fr(X_WALL - x) + "  " + lab)
    d.text(-6, TOTAL_RISE + 8, "Treads shown dashed for reference only", "sm", "start")
    return d.svg("Setting out")


# ================================================================= S-106
CH0, CHS, NCB = 6.1875, 3.375, 10          # stair post: first hole, spacing, count
TH0, THS = 3.6875, 3.375                    # top post, stair face
TL0, TLS = 4.8125, 3.125                    # top post, level face
HR = (33.0, 37.0)                           # handrail bracket taps, stair posts
BOLTS = (2.5, 5.75)                         # through bolts, stair posts
POST_LEN = 38.9375


def drilling():
    d = D(-6, 34, -5, 41, 11.0, "dr")
    def post(u, top, holes, taps, lab):
        d.rect(u - 1.5, 0, u + 1.5, top, "steel ob")
        d.rect(u - 1.5, top, u + 1.5, top + 0.25, "steel ob")
        d.rect(u - 1.5, -0.375, u + 1.5, 0, "steel ob")
        for h in holes:
            d.circle(u, h, 0.28, "void ob")
        for t in taps:
            d.circle(u - 0.9, t, 0.22, "nut")
        for b in BOLTS:
            d.line(u - 1.5, b, u + 1.5, b, "lag")
        d.text(u, -3.2, lab, "sm", "middle")
    sp = [CH0 + CHS * i for i in range(NCB)]
    tp = [TH0 + THS * i for i in range(NCB)]
    tl = [TL0 + TLS * i for i in range(NCB)]
    post(2, POST_LEN, sp, HR, "treads 1 and 4")
    post(16, 35.5, tp, (30.75, 34.75), "landing, stair face")
    post(28, 35.5, tl, (), "landing, level face")
    for h in sp:
        d.line(3.5, h, 5.2, h, "thin")
    d.dim((5.2, 0), (5.2, POST_LEN), 0, "see table")
    d.text(2, POST_LEN + 2.5, fr(POST_LEN), "sm", "middle")
    d.text(16, 36.9, "35-1/2", "sm", "middle")
    d.text(28, 36.9, "35-1/2", "sm", "middle")
    return d.svg("Guard post drilling schedule")

# ================================================================= S-501
def base_detail():
    d = D(-13, 66, -10, 15, 13.2, "bd")
    d.line(-13, 0, 66, 0, "grade")
    d.rect(-13, -1.4, 66, 0, "GR none")
    d.rect(-5, -9, 22, -0.02, "hid")
    draw_base(d)
    clip = 33
    d.poly([(XT, BP_TOP), (clip, s_top(clip)), (clip, s_top(clip) - DV), (XB, BP_TOP)], "steel ob")
    d.line(clip, s_top(clip) + 0.7, clip, s_top(clip) - DV - 0.7, "brk")
    for n in (1, 2):
        draw_tread(d, n)
    d.dim((-2, R), (-2, 0), -3, fr(R) + " riser")
    d.dim((-1.5, BP_TOP), (-1.5, 0), -1.3, fr(BP_TOP))
    d.dim((sad_span(1)[1] + 0.8, BP_TOP), (sad_span(1)[1] + 0.8, sad_bot(1)), -0.8, fr(sad_bot(1) - BP_TOP))
    d.dim((-1.5, BP_BOT), (28.5, BP_BOT), -4.0, '30" base PL')
    d.dim((XT, BP_TOP), (XB, BP_TOP), -2.2, fr(DV / SL) + " level cut")
    d.dim((xc(1) + SH, BP_TOP), (XT, BP_TOP), -6.0, fr(XT - xc(1) - SH) + " stub to stringer toe")
    d.dim((RODS_X[0], -2.5), (RODS_X[1], -2.5), -1.2, fr(RODS_X[1] - RODS_X[0]) + " rod spacing")
    d.tag(xc(1), 1.6, 35, 11.5, "M2b", 'HSS 6×4×1/4 stub, square cut, welded to M4,|notched at dry fit for the M1 toe')
    d.tag(RODS_X[1], BP_TOP + 0.6, 35, -4.5, "A2", '1/2 rods at 3/4 and 5-1/4 from the first riser|5-1/4 apart across, 1-1/4 round washers')
    d.tag(XT + 0.3, BP_TOP + 0.15, 35, 5.2, "V", '3/16" weep notch at the lowest|corner of M1 on M4, left open')
    d.circle(xc(1) + SH - 0.4, BP_TOP + 0.375, 0.094, "void ob")
    d.tag(xc(1) + SH - 0.4, BP_TOP + 0.375, 35, 2.6, "W", '3/16" weep hole in M2b at its lowest|corner, 3/8" above M4, clear of the fillet')
    d.tag(2, 0.25, 35, 7.5, "F", "self-adhered flashing under M4")
    d.text(-12, 13.2, f"level cut {90-DEG:.2f}\u00b0 off square", "dt", "start")
    d.text(-12, 13.2, "HOLD: verify to the pier as set", "sm", "start", dy=13)
    return d.svg("Base connection")


def wall_detail():
    d = D(49, 96, 20, 54, 13, "wd")
    d.rect(X_WALL, 20, X_WALL + 12, TOTAL_RISE, "CC ob")
    d.line(X_WALL + 12, TOTAL_RISE, 96, TOTAL_RISE, "grade")
    clip = 60
    d.poly([(clip, s_top(clip)), (X_END, YT), (X_END, YB), (clip, s_top(clip) - DV)], "steel ob")
    d.line(clip, s_top(clip) + 0.8, clip, s_top(clip) - DV - 0.8, "brk")
    for n in (6, 7):
        draw_tread(d, n)
    d.add(f'<rect x="0" y="0" width="{d.X(clip):.1f}" height="{d.H:.0f}" class="paper"/>')
    draw_wallplate(d)
    for yy in AN_Y:
        d.rect(X_WALL - 0.85, yy - 0.5, X_WALL - 0.5, yy + 0.5, "nut")
    d.circle(X_END - 3, s_top(X_END - 3) - DV + 0.9, 0.19, "void ob")
    d.dim((X_WALL + 12, TOTAL_RISE), (X_WALL + 12, AN_Y[0]), -1.6, fr(TOTAL_RISE - AN_Y[0]))
    d.dim((X_WALL + 12, AN_Y[0]), (X_WALL + 12, AN_Y[2]), -1.6, '10"')
    d.dim((X_END, YB), (X_END, YT), 1.4, fr(DV) + " plumb cut")
    d.dim((X_END, R * 7 - WOOD), (X_END, WP_TOP), 3.0, fr(R * 7 - WOOD - WP_TOP) + " clear")
    d.tag(X_WALL - 0.25, WP_BOT + 1.5, 66, 24, "M6", '1/2×12×16 wall PL')
    d.tag(xc(7), R * 7 + 0.2, 66, 27.5, "G", "guard post stem on the landing tread frame")
    d.tag(X_WALL + 4, AN_Y[1], 72, 52, "A1", '1/2" SS all-thread in SET-3G, 9/16 hole|3-1/2 to 4-1/2 embed, locate between bars', side="l")
    d.text(50, 47.5, f"plumb cut {DEG:.2f}\u00b0 off square", "dt", "start")
    d.text(50, 47.5, "HOLD: verify to the wall as built", "sm", "start", dy=13)
    d.text(X_WALL + 6, TOTAL_RISE, "T.O. wall", "sm", "middle", dy=-6)
    return d.svg("Wall connection")


def wall_face():
    d = D(-12, 12, WP_BOT - 3, WP_TOP + 3, 14, "wf")
    d.rect(-12, WP_BOT - 3, 12, WP_TOP + 3, "CC none")
    d.rect(-6, WP_BOT, 6, WP_TOP, "steel ob")
    d.rect(-2, YB, 2, YT, "STH ob")
    for u in (-AN_X, AN_X):
        for yy in AN_Y:
            d.circle(u, yy, 0.5, "nut")
            d.circle(u, yy, 0.28, "rodc")
    d.dim((-6, WP_TOP), (6, WP_TOP), 1.4, '12"')
    d.dim((-AN_X, WP_BOT), (AN_X, WP_BOT), -1.4, '9" anchors')
    d.dim((6, AN_Y[0]), (6, AN_Y[1]), 1.4, '5"')
    d.dim((-6, WP_BOT), (-6, WP_TOP), 1.4, '16"')
    d.text(0, (YT + YB) / 2, "tube", "sm", "middle", dy=4)
    return d.svg("Wall plate face")


# ================================================================= S-502
def stringer_cut():
    d = D(-5, 88, -9.5, 19.5, 11, "sc")
    off_b = 8 / math.tan(ANG)
    off_t = 8 * math.tan(ANG)
    L = LONG_PT
    d.poly([(0, 8), (L, 8), (L - off_t, 0), (off_b, 0)], "steel ob")
    marks = [(xc(n) - XT) / COS for n in range(2, NB + 1)]
    half = SH / COS
    hole = half - 0.4375          # just inside the stub's downhill wall
    faces = [m - half for m in marks]
    for s in marks:
        d.line(s - half, 8, s - half, 12.5, "cl")
        d.rect(s - half, 8, s + half, 8.35, "hid")
        d.circle(s - hole, 8, 0.12, "void ob")
    d.dim((0, 8), (L, 8), 9.5, fr(LONG_PT) + " long point (top face)")
    d.dim((off_b, 0), (L - off_t, 0), -3.5, fr(SHORT_PT) + " short point (bottom face)")
    d.dim((0, 8), (faces[0], 8), 4.5, fr(faces[0]))
    for a, b in zip(faces, faces[1:]):
        d.dim((a, 8), (b, 8), 4.5, fr(b - a))
    d.text(off_b / 2 - 2, 4, "LEVEL cut", "sm", "middle", rot=DEG)
    d.text(L - off_t / 2 + 2.3, 4, "PLUMB cut", "sm", "middle", rot=-(90 - DEG))
    d.note(0, -6.3, f"Bottom: level cut, {90-DEG:.2f}° off square.|Top: plumb cut, {DEG:.2f}° off square.", "nt")
    d.note(44, -6.3, 'Marks are the downhill face of each stub, measured along the top face|from the long point. 3/16" hole just inside each stub\'s downhill wall.', "nt")
    return d.svg("Stringer cut and layout")


def stub():
    d = D(-10.5, 10.5, -1.5, 9.2, 22, "sb")
    d.poly([(-SH, 0), (SH, 2 * SH * SL), (SH, STUB_LONG), (-SH, STUB_LONG)], "steel ob")
    d.line(-SH, 0, SH + 2.5, 0, "thin")
    r = 55
    d.add(f'<path d="M {d.X(-SH)+r:.1f} {d.Y(0):.1f} A {r} {r} 0 0 0 {d.X(-SH)+r*COS:.1f} {d.Y(0)-r*SIN:.1f}" class="dl" fill="none"/>')
    d.text(-SH, 0, f"{DEG:.2f}°", "dt", "start", dx=r + 5, dy=-4)
    d.dim((-SH, STUB_LONG), (-SH, 0), -1.3, fr(STUB_LONG) + " long")
    d.dim((SH, 2 * SH * SL), (SH, STUB_LONG), -1.3, fr(STUB_SHORT) + " short")
    d.dim((-SH, STUB_LONG), (SH, STUB_LONG), 1.0, fr(2 * SH))
    d.text(-SH - 3.9, 3, "downhill", "sm", "middle")
    d.text(SH + 4.1, 5, "uphill", "sm", "middle")
    return d.svg("Stub cut")


def sphere():
    d = D(35, 58.5, 18.5, 37.5, 19, "sph")
    d.poly([(35, s_top(35)), (58.5, s_top(58.5)), (58.5, s_top(58.5) - DV), (35, s_top(35) - DV)], "steel ob")
    for n in (4, 5):
        draw_tread(d, n)
    cx = 45 - math.sqrt(4 - (R * 5 - WOOD - R * 4 - 2) ** 2)
    d.circle(cx, R * 4 + 2, 2, "sphere")
    d.text(cx, R * 4 + 2, '4" Ø', "dt", "middle", dy=4)
    d.dim((45, R * 4), (45, R * 5 - WOOD), -1.0, fr(R - WOOD) + " clear")
    d.dim((56.25, R * 5 - WOOD), (56.25, R * 5), -1.2, fr(WOOD))
    d.text(cx - 1.5, R * 4 - 1.6, "blocked by tread above", "sph_t", "middle")
    return d.svg("Four inch sphere check")


# ================================================================= content
# ----------------------------------------------------------------- S-505 tread frame
def tread_frame_plan():
    d = D(-28, 72, -11.5, 17.5, 11, "tfp")
    W2, Dp = 24.0, 11.25
    d.poly([(-W2, 0), (W2, 0), (W2 - MEM, MEM), (-W2 + MEM, MEM)], "steel ob")
    d.poly([(-W2, Dp), (W2, Dp), (W2 - MEM, Dp - MEM), (-W2 + MEM, Dp - MEM)], "steel ob")
    d.poly([(-W2, 0), (-W2 + MEM, MEM), (-W2 + MEM, Dp - MEM), (-W2, Dp)], "steel ob")
    d.poly([(W2, 0), (W2 - MEM, MEM), (W2 - MEM, Dp - MEM), (W2, Dp)], "steel ob")
    for u in (-12.5, 12.5):
        d.rect(u - 0.75, MEM, u + 0.75, Dp - MEM, "steel ob")
    for s in (-1, 1):
        d.rect(s * 2.0625, MEM, s * 2.4375, Dp - MEM, "steel ob")
    d.rect(-2, MEM, 2, Dp - MEM, "steel ob")
    d.rect(-2, Dp / 2 - SH, 2, Dp / 2 + SH, "hidc")
    for u in (-18, -6, 6, 18):
        for v in (1.5, Dp - 1.5):
            d.circle(u, v, 0.14, "redc")
    for u in (-22.5, 22.5):
        for v in (2.75, 8.4375):
            d.circle(u, v, 0.14, "redc")
    for u in (-12.5, 12.5):
        for v in (4.25, 7.0):
            d.circle(u, v, 0.14, "redc")
    for u in (-W2 + 1.5, W2 - 1.5):
        d.circle(u, 0.9, 0.15, "void ob")
    d.rect(21.25, 4.375, 23.75, 6.875, "hid")
    d.line(-28, Dp / 2, 28, Dp / 2, "cl")
    d.line(0, -3, 0, Dp + 3, "cl")
    d.dim((-W2, Dp), (W2, Dp), 3.2, '48" overall')
    d.dim((0, Dp), (2.4375, Dp), 1.4, '2-7/16')
    d.dim((2.4375, Dp), (12.5, Dp), 1.4, '10-1/16')
    d.dim((12.5, Dp), (21, Dp), 1.4, '8-1/2')
    d.dim((W2, 0), (W2, Dp), -2.6, fr(Dp))
    d.dim((W2, 0), (W2, 3), -1.2, '3')
    d.dim((-2, 0), (2, 0), -1.6, '4 plate')
    d.dim((0, 0), (6, 0), -3.6, '6')
    d.dim((6, 0), (18, 0), -3.6, '12')
    d.tag(-10, 1.5, 30, -6.2, "1", "HSS 2-1/2×1-1/2×3/16 laid flat, mitred corners.|Post treads: 3×1-1/2×3/16 end members, unequal miter")
    d.tag(12.5, 5.5, 30, -2.0, "2", "HSS 1-1/2×1-1/2×1/8 joists at ±12-1/2")
    d.tag(0.5, 7.9, 30, 1.0, "3", "M3 plate, 3/8 × 4 × 6-1/4 bar, between the collars")
    d.tag(2.25, 4.0, 30, 4.0, "4", "M8 collars, 3/8 × 1-1/2 × 6-1/4 bar, 1/16 weld gap to the plate")
    d.tag(0, Dp / 2 + 2.1, 30, 7.6, "5", "M3 caps the stub; the frame drains at the two|underside corners, the stub drains into the stringer")
    d.tag(-W2 + 1.5, 0.9, 30, -9.0, "6", "3/16 frame drain at two corners, underside")
    d.tag(22.5, 5.625, 30, 11.6, "7", "Post treads only: 2-1/2 stem, 7 tall")
    d.tag(18, Dp - 1.5, 30, 14.6, "8", "7/32 holes through both walls: plank screws and coating vents")
    return d.svg("M7 tread frame, plan from above")


def tread_frame_section():
    d = D(-28, 72, -8, 6.5, 11, "tfs")
    for a2, b2 in ((-24, -24 + MEMP), (24 - MEMP, 24)):
        d.rect(a2, 0, b2, 1.5, "steel ob")
        d.rect(a2 + WALLT, WALLT, b2 - WALLT, 1.5 - WALLT, "void")
    for u in (-12.5, 12.5):
        d.rect(u - 0.75, 0, u + 0.75, 1.5, "steel ob")
        d.rect(u - 0.625, 0.125, u + 0.625, 1.375, "void")
    for s in (-1, 1):
        d.rect(s * 2.0625, 0, s * 2.4375, 1.5, "steel ob")
    d.rect(-2, 1.125, 2, 1.5, "steel ob")
    d.rect(-2, -3.5, 2, 1.0, "hid")
    d.rect(-2, 1.0, 2, 1.125, "pad")
    d.line(-2.9, 0.5, 2.9, 0.5, "rod")
    d.rect(21.25, 1.5, 23.75, 4.5, "steel ob")
    d.line(-28, 0, 28, 0, "thin")
    d.dim((24, 0), (24, 1.5), -1.2, '1-1/2')
    d.dim((-2.4375, -3.5), (2.4375, -3.5), -1.0, '4-7/8 over the collars')
    d.tag(2.25, 0.9, 30, 3.5, "4", "Collars, full frame depth; plate welded between, flush")
    d.tag(2.9, 0.5, 30, 1, "8", "(2) 3/8 through bolts, 4 apart, both collars and the stub")
    d.tag(0, -2, 30, -2, "9", "Stub rises 1 in between the collars, 1/16 neoprene pad on top")
    d.tag(22.5, 3.5, 30, -5.5, "7", "Stem to the end tube, 1/4 fillet all around")
    return d.svg("M7 section across, at the stub")


# ----------------------------------------------------------------- S-506 base plate
def base_plate():
    XB = (BP_TOP - C + DV) / SL
    d = D(-14, 52, -4, 32, 12, "bpp")
    d.rect(-6, -1.5, 6, 28.5, "steel ob")
    for v in RODS_X:
        for u in (-RODS_U, RODS_U):
            d.circle(u, v, 0.28, "void ob")
    d.rect(-2, xc(1) - SH, 2, xc(1) + SH, "hid")
    d.rect(-2, XT, 2, XB, "hid")
    d.line(-8, 0, 8, 0, "thin")
    d.text(-8, 0, "first riser", "sm", "end", dx=-4, dy=4)
    d.line(0, -3, 0, 30, "cl")
    d.dim((6, -1.5), (6, 28.5), -2.6, '30"')
    d.dim((6, 0), (6, RODS_X[0]), -1.2, fr(RODS_X[0]))
    d.dim((6, RODS_X[0]), (6, RODS_X[1]), -1.2, fr(RODS_X[1] - RODS_X[0]))
    d.dim((-RODS_U, -1.5), (RODS_U, -1.5), -1.4, fr(2 * RODS_U))
    d.dim((-6, -1.5), (6, -1.5), -3.0, '12"')
    d.dim((-6, xc(1) - SH), (-6, xc(1) + SH), 1.4, '6')
    d.dim((-6, XT), (-6, XB), 1.4, fr(XB - XT) + ' level cut')
    d.dim((-9, 0), (-9, XT), 0, fr(XT))
    d.tag(RODS_U, RODS_X[1], 14, 4, "1", "(4) 9/16 holes, drilled at dry fit to the rods as set")
    d.tag(0, xc(1), 14, 9, "2", "M2b stub footprint, 4 across x 6 in the run;|notched at dry fit where the M1 toe lands")
    d.tag(0, (XT + XB) / 2, 14, 16, "3", "M1 level cut footprint, 4 wide")
    d.tag(4, 26, 14, 24, "4", "PL 1/2 x 12 x 30; self-adhered flashing underneath")
    return d.svg("M4 base plate, plan from above")


def _centre(d, y0=0.0):
    # hidden centre connection: two full-depth collars, plate between, stub, pad, bolts
    for s in (-1, 1):
        d.rect(s * 2.0625, y0, s * 2.4375, y0 + 1.5, "hid")
    d.rect(-2.0, y0 + 1.125, 2.0, y0 + 1.5, "hid")
    d.rect(-2, y0, 2, y0 + 1.0, "hid")
    d.rect(-2, y0 + 1.0, 2, y0 + 1.125, "pad")
    d.line(-2.9, y0 + 0.5, 2.9, y0 + 0.5, "hidp")


def tread_centre_detail():
    d = D(-9, 30, -6.5, 5, 30, "tcd")
    d.rect(-9, 0, 9, 1.5, "steel ob")
    d.rect(-9, 1.5, 9, 3.25, "WD ob")
    _centre(d)
    d.rect(-2, -6.5, 2, 0, "steel ob")
    d.line(0, -6.5, 0, 4.5, "cl")
    d.dim((-2.4375, 0), (2.4375, 0), -1.2, '4-7/8 over the collars')
    d.dim((-2, -3), (2, -3), 0, '4 stub across')
    d.dim((-2.0625, 0.3), (-2, 0.3), 0.8, '1/16')
    d.dim((-4, 1.125), (-4, 1.5), 1.0, '3/8')
    d.dim((-5.2, 0), (-5.2, 1.0), 0.8, '1 in')
    d.dim((9, 0), (9, 1.5), -1.0, '1-1/2')
    d.dim((9, 1.5), (9, 3.25), -1.0, '1-3/4')
    d.tag(1.0, 1.3, 12, 4.2, "M3", "Plate, 3/8 × 4 bar, flush with the frame top")
    d.tag(2.25, 0.3, 12, 2.4, "M8", "Collars, 3/8 × 1-1/2 bar, full frame depth")
    d.tag(2.7, 0.5, 12, 0.6, "H1", "Through bolts, 4 apart, both collars and the stub")
    d.tag(0, 1.06, 12, -3.0, "H2", "EPDM pad on the open stub top")
    d.tag(1.9, -4.5, 12, -4.8, "M2", "Stub, 6 in the run; only this shows below the frame")
    return d.svg("Centre connection, front elevation, enlarged")


def tread_section():
    d = D(-30, 64, -16, 7, 11, "ts")
    d.rect(-24, 0, 24, 1.5, "steel ob")
    d.rect(-24, 1.5, 24, 3.25, "WD ob")
    for u in (-12.5, 12.5):
        d.rect(u - 0.75, 0, u + 0.75, 1.5, "hid")
    for a, b in ((-24, -21), (21, 24)):
        d.rect(a, 0, b, 1.5, "hid")
    _centre(d)
    d.rect(-2, -5.0, 2, 0, "steel ob")
    d.rect(-2, -5.0 - DV, 2, -5.0, "steel ob")
    d.line(0, -16, 0, 6.5, "cl")
    d.dim((-24, 3.25), (24, 3.25), 2.2, '48" tread')
    d.dim((0, 3.25), (12.5, 3.25), 1.0, '12-1/2')
    d.dim((24, 0), (24, 1.5), -1.2, '1-1/2')
    d.dim((24, 1.5), (24, 3.25), -2.6, '1-3/4')
    d.dim((-2, -5.0), (-2, 0), 2.6, '5 air')
    d.dim((-2, -5.0 - DV), (2, -5.0 - DV), -1.0, '4')
    d.tag(-16, 2.4, 30, 5.5, "W1", "Ash planks 5-1/2 × 1-3/4, 3/16 reveal")
    d.tag(-18, 0.75, 30, 3, "M7", "HSS 2-1/2×1-1/2×3/16 frame, front member shown solid")
    d.tag(12.5, 0.75, 30, 0.5, "J", "1-1/2 sq joists at ±12-1/2 (hidden)")
    d.tag(1.0, 1.3, 30, -2, "M3", "3/8 × 4 plate between the collars, flush with the frame top (hidden)")
    d.tag(2.25, 0.3, 30, -4.5, "M8", "(2) 3/8 × 1-1/2 collars, 1/16 clear of the stub (hidden)")
    d.tag(2.7, 0.5, 30, -7, "H1", "(2) 3/8 through bolts, both collars and the stub")
    d.tag(0, 1.06, 30, -12, "H2", "1/8 EPDM pad on the open stub top")
    d.tag(1.9, -2.5, -26, -8, "M2", "HSS 6×4×1/4 stub, 6 at ℄, 1 in up inside the frame", side="r")
    d.tag(1.9, -9, -26, -13, "M1", "HSS 8×4×1/4 stringer", side="r")
    return d.svg("Typical tread, front elevation")


def post_section():
    d = D(-30, 66, -12, 16, 11, "ps")
    d.rect(-24, 0, 24, 1.5, "steel ob")
    d.rect(-24, 1.5, 24, 3.25, "WD ob")
    for u in (-12.5, 12.5):
        d.rect(u - 0.75, 0, u + 0.75, 1.5, "hid")
    for a, b in ((-24, -21), (21, 24)):
        d.rect(a, 0, b, 1.5, "hid")
    _centre(d)
    d.rect(-2, -5.0, 2, 0, "steel ob")
    d.rect(-2, -9.0, 2, -5.0, "steel ob")
    for u in (-POST_U, POST_U):
        d.rect(u - 1.5, 3.25, u + 1.5, 13.5, "steel ob")
        d.rect(u - 1.5, 1.5, u + 1.5, 3.25, "hid")
        d.rect(u - 1.25, 1.5, u + 1.25, 8.5, "hid")
        for b in (2.5, 5.75):
            d.line(u - 1.8, 1.5 + b, u + 1.8, 1.5 + b, "lag")
        d.circle(u - 0.9, 1.5 + 0.6, 0.12, "hidc")
    d.line(0, -12, 0, 15, "cl")
    d.dim((0, 13.5), (POST_U, 13.5), 1.4, fr(POST_U) + " to post ℄")
    d.dim((24, 1.5), (24, 8.5), -1.4, '7 stem')
    d.tag(POST_U + 1.5, 11, 30, 14, "G", "3×3×3/16 post, bare tube, sleeved over the stem")
    d.tag(POST_U, 5.0, 30, 11, "P1", "2-1/2 sq stem, 7 tall, welded to the 3 in end tube (hidden)")
    d.tag(POST_U + 1.8, 7.25, 30, 8, "P5", "(2) 3/8 through bolts at 2-1/2 and 5-3/4")
    d.tag(POST_U - 0.9, 2.1, 30, 5, "V", "3/16 drain in the stem, just above the tube")
    d.tag(-18, 0.75, 30, 2, "M7", "Frame front member, solid; both planks notched around the post")
    d.tag(1.9, -3, 30, -2, "M2", "Stub into the collar, as S-103")
    return d.svg("Guard post mounting, front elevation")


def saddles():
    d = D(-9, 30, -5.8, 5.8, 22, "sp")
    d.rect(-2, -CH, 2, CH, "steel ob")
    for s in (-1, 1):
        d.rect(s * 2.0625, -CH, s * 2.4375, CH, "steel ob")
    d.rect(-2, -SH, 2, SH, "hidc")
    for v in (-BSP / 2, BSP / 2):
        d.line(-2.9, v, 2.9, v, "hidp")
    d.line(-8, 0, 8, 0, "cl")
    d.dim((-2, CH), (2, CH), 1.2, '4 plate')
    d.dim((-2.4375, -CH), (2.4375, -CH), -1.2, '4-7/8 over the collars')
    d.dim((2.4375, -CH), (2.4375, CH), -1.4, fr(2 * CH))
    d.dim((-2.0625, CH), (-2, CH), 2.4, '1/16 weld gap')
    d.dim((-2.9, -BSP / 2), (-2.9, BSP / 2), 0.9, fr(BSP) + ' bolts')
    d.tag(0, CH - 0.3, 11, 3.9, "1", "Plate, 3/8 x 4 flat bar x 6-1/4, flush with the frame top")
    d.tag(-2.25, 2.2, 11, 2.2, "2", "(2) collars, 3/8 x 1-1/2 flat bar x 6-1/4, member to member")
    d.tag(2.9, BSP / 2, 11, 0.5, "3", "(2) 3/8 through bolts, 4 apart, left to right")
    d.tag(0.5, -1.2, 11, -3.2, "6", "Stub below, 6 x 4 (hidden)")
    return d.svg("M3 plate and M8 collars, plan from below")


def fig(svg, cap, cls=""):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


SHEETS = []


def sheet(num, title, body, scale="Not to scale; dimensions govern"):
    SHEETS.append((num, title))
    return (f'<article class="sheet" id="s{num}">'
            f'<header class="tb"><div class="num">{num}</div><div class="ttl"><h2>{title}</h2><p>{scale}</p></div></header>'
            f'<div class="body">{body}</div></article>')


w_str = 17.27 * LONG_PT / 12
w_stub = 10.51 * (6 * STUB_CL + 6) / 12
w_sad9 = 0.2836 * 0.5 * 9 * 28
w_sad3 = 0.2836 * 0.5 * 3 * 28
w_cm = 0.0
w_base = 0.2836 * 0.5 * 12 * 28
w_wall = 0.2836 * 0.5 * 12 * 16
w_total = w_str + w_stub + 7 * w_sad9 + w_base + w_wall + 6

gen_notes = f"""
<div class="cols">
<section>
<h3>Design basis</h3>
<table class="kv">
<tr><td>Codes</td><td>2018 IRC R311.7 / R312 and 2018 IBC 1011 / 1015, stricter of the two</td></tr>
<tr><td>Live load</td><td>Stair 100 psf or 300 lb point. Guard 200 lb any direction at the top, plus sustained cable tension</td></tr>
<tr><td>Total rise</td><td>7 risers @ {fr(R)} = {fr(TOTAL_RISE)}, grade to top of wall</td></tr>
<tr><td>Total run</td><td>6 treads @ {fr(T)} = {fr(RUN)} nosing to landing nosing, slope {DEG:.2f}°</td></tr>
<tr><td>Tread</td><td>Steel frame {fr(TW)} × {fr(T)}, two ash planks on top, {fr(WOOD)} total; no nosing; 42" clear between guard posts; landing tread flush with top of wall</td></tr>
<tr><td>Open riser</td><td>{fr(R-WOOD)} clear, passes the 4" sphere</td></tr>
<tr><td>Guard posts</td><td>Treads 1 and 4 centred, landing post at the nosing. {fr(39.55)} and {fr(34.75)} on the rake, both under the 48" limit. Clear width between posts 42"</td></tr>
<tr><td>Steel</td><td>HSS ASTM A500 Gr. C; plate A36; E70XX</td></tr>
<tr><td>Wood</td><td>Thermally modified ash, oiled to hold its colour. The steel frame is the structure; the planks are a surface.</td></tr>
</table>
</section>
<section>
<h3>Hold points</h3>
<ol class="holds">
<li><b>Finish grade and pier.</b> M4 bears directly on grade over the existing pier, on self-adhered flashing. M4 is not shimmed. Measure its pitch along the stair and cross slope across it as set, and cut the M1 level cut to match, as a compound cut where there is cross slope. Measure the wall face the same way for the plumb cut.</li>
<li><b>Rod positions.</b> Measured at 3/4" and 5-1/4" from the first riser face, 5-1/4" apart across, 1/2" diameter. Re-verify before drilling; both rows land near the downhill end of M4, so the plate runs 1-1/2" past the first riser; the 1-1/4" round washers clear the M2b stub walls.</li>
<li><b>Wall anchors.</b> 6" stem with #4 verticals at 12" o.c., 1-3/4" clear at the back face, so bars sit about 4" from the front face. Scan and lay out anchors between bars. Embedment 3-1/2" minimum to 4-1/2" maximum in the 6" stem, 9/16" hole.</li>
<li><b>Guard sequence.</b> The posts are propped by the top rail. The rail must be installed, spliced over posts with its internal splines, and anchored at the wall <em>before</em> any cable is tensioned. Tensioning against an unbraced post makes it a cantilever and overloads the tread mounting.</li>
<li><b>Propped post assumption.</b> The guard posts are propped by the continuous top rail, so the stem welds see about 1,200 in-lb of moment and 1,244 lb of shear at the bottom post, carried into the side walls of the 3 in end tube. The engineer should confirm the stem-to-tube weld and the collar connection for that case.</li>
<li><b>Engineer of record review.</b> A cantilevered mono stringer is not a prescriptive IRC stair. Expect stamped calcs and possibly special inspection of the adhesive anchors.</li>
</ol>
</section>
</div>
<h3>Legend</h3>
<div class="legend">
<span><svg viewBox="0 0 40 18"><rect x="1" y="2" width="38" height="14" class="steel ob"/></svg>Steel</span>
<span><svg viewBox="0 0 40 18"><defs><pattern id="lgw" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" class="wdb"/><path d="M0 3 Q5 1 10 3 M0 8 Q5 6.5 10 8" class="wdl"/></pattern></defs><rect x="1" y="2" width="38" height="14" fill="url(#lgw)" class="ob"/></svg>Ash plank</span>
<span><svg viewBox="0 0 40 18"><rect x="1" y="6" width="38" height="4" class="pad"/></svg>Gasket</span>
<span><svg viewBox="0 0 40 18"><rect x="1" y="2" width="38" height="14" class="hid"/></svg>Hidden</span>
<span><svg viewBox="0 0 40 26"><circle cx="20" cy="13" r="11" class="bub"/><text x="20" y="13" text-anchor="middle" dominant-baseline="central" class="bt">M1</text></svg>Mark</span>
</div>
"""

bom = f"""
<div class="scroll"><table class="grid">
<thead><tr><th>Mark</th><th>Qty</th><th>Description</th><th>Size / cut</th><th>≈ lb ea</th></tr></thead>
<tbody>
<tr><td>M1</td><td>1</td><td>Mono stringer</td><td>HSS 8×4×1/4. Long point {fr(LONG_PT)}, short point {fr(SHORT_PT)}. Level cut bottom, plumb cut top.</td><td>{w_str:.0f}</td></tr>
<tr><td>M2a</td><td>6</td><td>Stubs, treads 2 to 7</td><td>HSS 6×4×1/4, 4" across the tread, 6" in the run direction, open top, rising 1 in into the tread frame collar. {fr(STUB_CL)} at ℄, long {fr(STUB_LONG)}, short {fr(STUB_SHORT)}, single {DEG:.2f}° cut. All six identical.</td><td>4</td></tr>
<tr><td>M3</td><td>7</td><td>Plates</td><td>3/8 × 4 flat bar × 6-1/4, set between the two M8 collars with a 1/16" gap each side, flush with the frame top. (2) 3/16" drains outside the stub footprint. Caps the open stub.</td><td>2</td></tr>
<tr><td>M8</td><td>14</td><td>Collars</td><td>3/8 × 1-1/2 flat bar × 6-1/4, two per tread, full frame depth, welded at both ends to the frame front and back members. Both identical. Through-bolt holes drilled at dry fit through both collars and the stub together: 13/32 round in the stub, 13/32 × 9/16 vertical slots in the collars.</td><td>1</td></tr>
<tr><td>M7</td><td>7</td><td>Tread frames</td><td>Picture frame of HSS 2-1/2×1-1/2×3/16 laid flat, 48 × 11-1/4, mitred corners, with HSS 3×1-1/2×3/16 end members on the three post treads, with HSS 1-1/2×1-1/2×1/8 joists at ±12-1/2 and the two M8 collars with the M3 plate between the front and back members. F1, F2 and F3 drilled 7/32 through both walls for the plank screws: 4 in each front and back member at 6 and 18 either side of centre, 2 in each end member at the plank centres, 2 in each joist 1-1/4 from its ends. The same holes vent the frame for coating. Landing tread: the front hole in each end member is omitted under the post stem. (2) 3/16" drains at the low corners. Post treads get the 2-1/2 stem welded to each 3 in end tube.</td><td>22</td></tr>
<tr><td>M4</td><td>1</td><td>Base plate</td><td>PL 1/2 × 12 × 30, from 1-1/2 downhill of the first riser to 28-1/2 uphill. Bears on grade over self-adhered flashing. (4) 9/16" holes at 3/4 and 5-1/4 from the first riser, 5-1/4 apart across; drill at dry fit to the rods as set.</td><td>{w_base:.0f}</td></tr>
<tr><td>M2b</td><td>1</td><td>Stub, tread 1</td><td>HSS 6×4×1/4 × 4-3/16, square cut both ends, open top, centred on M4, uphill wall notched at dry fit where the M1 level cut toe lands, 1/4 fillet all around, ground smooth. 3/16 weep hole at its lowest corner, 3/8 above M4. Rises 1 in into the tread frame collar. Same section as M2a.</td><td>2</td></tr>
<tr><td>M6</td><td>1</td><td>Wall plate</td><td>PL 1/2 × 12 × 16, (6) 9/16" holes at 9" × 5".</td><td>{w_wall:.0f}</td></tr>
<tr><td>W1</td><td>14</td><td>Tread planks</td><td>Thermally modified ash, 5-1/2 × 1-3/4 × 48, two per tread with a 3/16" reveal. Surfaced four sides, 1/8" eased edges, ends sealed.</td><td>≈14</td></tr>
<tr><td>H1</td><td>14</td><td>Tread through bolts</td><td>3/8-16 × 5-1/2 type 316, two per tread through both collars and the stub, 4 apart, left to right, black oxide stainless with nylon insert nuts and anti-seize. Holes drilled through collars and stub together at dry fit, 4 apart: 13/32 round in the stub, 13/32 × 9/16 vertical slots in the collars so the pad thickness and its compression do not fight the bolt.</td><td>–</td></tr>
<tr><td>H3</td><td>110</td><td>Plank screws</td><td>#10 × 2-3/4 type 316 stainless wood screws, pan or washer head, driven up from below through the 7/32 holes in the frame, 1-1/4 into the ash with a 1/8 pilot. Eight per plank; two fewer on the landing tread.</td><td>–</td></tr>
<tr><td>H2</td><td>7</td><td>Stub pads</td><td>1/16" solid neoprene, 6 × 4, self-adhesive backed, on the open stub top under M3.</td><td>–</td></tr>
<tr><td>A1</td><td>6</td><td>Wall anchors</td><td>1/2" 316 SS all-thread in SET-3G, 9/16" hole, 3-1/2" minimum to 4-1/2" maximum embed, located between the wall verticals.</td><td>–</td></tr>
<tr><td>A2</td><td>4</td><td>Existing pier rods</td><td>1/2" diameter, measured at 3/4 and 5-1/4 from the first riser, 5-1/4 apart across. 1-1/4" OD hardened round washer, nut and acorn cap. The round washer clears the M2b stub wall.</td><td>–</td></tr>
<tr><td colspan="5" class="sub">Guard mounting, by the guard package, shown here for coordination</td></tr>
<tr><td>P1</td><td>6</td><td>Tread spigot stems</td><td>HSS 2-1/2×2-1/2×3/16 × 7, welded all around to the top of the 3 in end tube at each post. 3/16" drain in the stem wall just above the tube.</td><td>3</td></tr>
<tr><td>P5</td><td>12</td><td>Post through bolts</td><td>3/8-16 × 4-1/2 type 316, (2) per post at 2-1/2 and 5-3/4 above the post base, interleaved between the cable holes. Drill post and stem together at dry fit.</td><td>–</td></tr>
<tr><td>–</td><td>3</td><td>Guard posts</td><td>HSS 3×3×3/16, bare tube, sleeved over the P1 stem and through-bolted. {fr(POST_U)} each side of centreline. Centred on treads 1 and 4; on the landing tread the post sits at the nosing, centre 1-1/2 uphill of it.</td><td>–</td></tr>
</tbody>
<tfoot><tr><td colspan="4">Stair weldment to powder coater, approx.</td><td>{w_total:.0f}</td></tr></tfoot>
</table></div>
"""

welds = """
<div class="scroll"><table class="grid">
<thead><tr><th>Joint</th><th>Weld</th><th>Note</th></tr></thead>
<tbody>
<tr><td>M2 stub → M1 stringer</td><td>3/16" fillet on the uphill and downhill faces; flare-bevel groove filled flush along the two matched sides</td><td>4" stub on the 4" stringer face is a matched-width joint. Drill the 3/16" hole in M1 first.</td></tr>
<tr><td>M8 collars → M7 frame</td><td>3/16" fillet both sides at each end</td><td>Collars run between the front and back members, never notched into them.</td></tr>
<tr><td>M3 plate → M8 collars</td><td>Square groove, 1/16" root opening, full 3/8" penetration from the top, ground flush</td><td>Continuous: this weld is the water seal over the open stub. Set the gap with 1/16" shims.</td></tr>
<tr><td>M7 tread frame</td><td>Full perimeter welds, crosses fitted and welded both faces</td><td>Check the frame flat and square before welding out. Drains at the low corners before coating.</td></tr>
<tr><td>M2b stub → M4</td><td>1/4" fillet, all around</td><td>Square cut both ends, open top.</td></tr>
<tr><td>M1 → M4 base plate</td><td>1/4" fillet, all around</td><td>Tacked only until the dry fit confirms the bearing plane; trim the level cut to suit, then weld.</td></tr>
<tr><td>M1 → M6 wall plate</td><td>1/4" fillet, all around</td><td>Check the plate stays flat after welding.</td></tr>
<tr><td>Stem → M7 end tube</td><td>1/4" fillet all around</td><td>The stem lands on a 3 in wide tube, so its load goes into the tube side walls. Posts are not welded; they sleeve on and bolt.</td></tr>
</tbody></table></div>
"""

finish = """
<div class="scroll"><table class="grid">
<thead><tr><th>Item</th><th>Requirement</th></tr></thead>
<tbody>
<tr><td>Surface preparation</td><td><b>SSPC-SP10 near-white blast</b>, by the coater. Do not accept SP6 commercial blast. Grind all welds smooth and break every sharp edge before blasting; blasting will not fix a sharp arris or a weld crater.</td></tr>
<tr><td>Coating system</td><td>Zinc-rich powder primer, then super-durable polyester (TGIC) topcoat. Tell the coater: exterior, high UV at 4,500 ft, freeze-thaw, snowmelt at grade. <b>Do not hot-dip galvanize.</b> The stair is a single precision weldment; an 840°F kettle dip will distort the stringer and take the seven saddles out of plane, and it cannot be straightened once coated.</td></tr>
<tr><td>Before it goes to the coater</td><td>No oil, grease, cutting fluid, layout dye or wax crayon on any face that stays. Blasting drives oil in rather than removing it. Mark with soapstone or on offcuts only.</td></tr>
<tr><td>Storage between dry fit and coating</td><td>Light flash rust is removed by the blast and is not a concern. Pitting is. Store off the ground on blocks, sloped to drain, either open or fully covered. Never leave a tarp lying on the steel; it traps condensation.</td></tr>
<tr><td>Vents and drains, all before coating</td><td>3/16" hole in the stringer top face under each M2 stub, its downhill edge flush with the inside of the stub's downhill wall, so each stub drains and vents into the stringer. 3/16" weep notch in the bottom edge of M1 at its lowest corner on M4, as set in the field. 3/16" weep hole through the side wall of M2b at its lowest corner, centred 3/8" above M4 so it clears the 1/4" fillet. No other vents in M1 or the stubs; the stubs vent through their open tops. 3/8" in every guard post near its base. Any closed section that is welded shut and not vented can blow a weld in the cure oven.</td></tr>
<tr><td>After coating</td><td>Tape over the stub holes, the M1 weep notch and the M2b weep hole while blasting so media stays out of the stringer; pull the tape before coating so they vent in the oven. After coating, leave all of them open. Water that gets past a stub pad runs down the stringer and out the notch onto M4.</td></tr>
<tr><td>Drilled and tapped holes</td><td>All drilling and tapping happens at dry fit, before coating: rod holes in M4, wall anchors through M6, through-bolt holes in the collars and stubs, plank screw holes in the tread frames, rail-to-plate taps, guard post cable holes at the rake angle, and the handrail bracket taps. Tapping through powder coat leaves bare threads in a wet location. Plug unused tapped holes with stainless button-head screws and sealant.</td></tr>
<tr><td>Dissimilar metals</td><td>Type 316 stainless fasteners against coated steel. Use EPDM-bonded or nylon washers at every stainless-to-steel contact so the coating is not cut and the couple is broken.</td></tr>
<tr><td>Interiors the powder cannot reach</td><td>Electrostatic powder does not throw down a long tube. Anything more than an inch or two inside a rail or post will be bare. Coat splines and reachable interior surfaces with a <b>cold galvanizing compound of 90%+ zinc in the dry film</b> (ZRC or Rust-Oleum Cold Galvanizing Compound), two coats. Hardware-store "galvanized look" paint is not sacrificial and does nothing.</td></tr>
<tr><td>Fasteners</td><td>Type 316 throughout. <b>Button or pan head, not countersunk</b>, wherever the host material is 1/8" or thinner; countersinking a 1/8" wall leaves almost no bearing and the head pulls through. Bonded EPDM sealing washer under every head that passes through an exterior surface. Anti-seize on all stainless-to-stainless threads; 316 galls badly when dry.</td></tr>
<tr><td>Drains</td><td>3/16" hole in the bottom wall within 1" of the low end of every rail and hollow post, in addition to the coating vents. Every closed section in this job gets water in it eventually; the only question is whether it can leave.</td></tr>
<tr><td>Touch-up</td><td>Keep a matched aerosol or brush-grade epoxy from the coater for field damage. Any bare steel left in contact with wood or concrete will bleed rust through the finish within a season.</td></tr>
<tr><td>Treads</td><td>Thermally modified ash: surface four sides, sand 120 grit, ease edges 1/8", seal ends. Finish all faces before install with a penetrating oil that carries UV pigment (Cutek, Penofin or a hardwax oil) to hold the brown. Recoat every 2–3 years. Left unfinished it silvers without harm, but colour is the reason for the finish.</td></tr>
</tbody></table></div>
"""

seq = """
<ol class="seq">
<li>Verify the hold points on S-001. Confirm the bearing plane at the pier and locate the rods and the wall reinforcing.</li>
<li>Tap the guard posts for the handrail brackets: (2) 1/4-20 in the inboard face of each stair post, left side ascending, at 4" centres about 34" above the nosing line. Plug with stainless button heads until the handrail is fitted. This cannot be added after coating without drilling finished steel.</li>
<li>Cut M1. Lay out the six stub centrelines along the top face from the long point. Drill a 3/16" hole 1-3/8" downhill of each, before the stubs go on.</li>
<li>Build a slope jig at 31.43°. Fit and weld the M2 stubs, checking every one square, level and on the nosing line. Build the seven M7 tread frames on a flat jig and check both diagonals. Weld the M8 collars between the front and back members, then the M3 plate between the collars on 1/16" shims.</li>
<li>Weld M6. Tack M4 and the M2b stub.</li>
<li>Dry fit. Trim the M1 level cut to suit the actual bearing plane. Drill the 9/16" rod holes through M4 to the rods as set. Drill wall anchors through M6 as a template. Drop each tread frame onto its stub, with the neoprene pad in place, and drill the through-bolt holes through collars and stub together: 13/32 round in the stub, slotted 13/32 × 9/16 in the collars. At the three post treads, notch both planks at each end around the post, 3-1/8 along the plank, 1-7/16 deep on the front plank and 1-1/2 on the back, and seal the end grain.</li>
<li>Remove, finish all welds, drill vents, grind, deburr. Blast and powder coat; cold-galvanize any interior surfaces that the coating will not reach.</li>
<li>Install the stair: flashing under M4, set and torque the rods, install wall anchors per the ICC-ES cure time, set the stub pads, drop the tread frames on, fit the through bolts, then screw the ash from below.</li>
<li>Install the guard: stand the posts on their stems and through-bolt, then the top rail with its splines and the wall connection. Tension cables last.</li>
</ol>
"""

setout_tbl = f"""
<div class="scroll"><table class="grid">
<thead><tr><th>Point</th><th>From wall face</th><th>Below top of wall</th></tr></thead>
<tbody>
<tr><td>Wall plate, top edge</td><td>at the wall</td><td>{fr(TOTAL_RISE-WP_TOP)}</td></tr>
<tr><td>Wall plate, bottom edge</td><td>at the wall</td><td>{fr(TOTAL_RISE-WP_BOT)}</td></tr>
<tr><td>Anchor rows, three</td><td>±4-1/2 from ℄</td><td>{fr(TOTAL_RISE-AN_Y[0])}, {fr(TOTAL_RISE-AN_Y[1])}, {fr(TOTAL_RISE-AN_Y[2])}</td></tr>
<tr><td>Stringer, top of plumb cut</td><td>1/2 (plate face)</td><td>{fr(TOTAL_RISE-YT)}</td></tr>
<tr><td>Stringer, bottom of plumb cut</td><td>1/2 (plate face)</td><td>{fr(TOTAL_RISE-YB)}</td></tr>
<tr><td>Base plate, uphill end</td><td>{fr(X_WALL-28.5)}</td><td>{fr(TOTAL_RISE-BP_TOP)} to its top</td></tr>
<tr><td>Base plate, downhill end</td><td>{fr(X_WALL+1.5)}</td><td>{fr(TOTAL_RISE-BP_TOP)} to its top</td></tr>
<tr><td>Stringer level cut, bottom-face toe</td><td>{fr(X_WALL-XB)}</td><td>{fr(TOTAL_RISE-BP_TOP)}</td></tr>
<tr><td>Stringer level cut, top-face toe</td><td>{fr(X_WALL-XT)}</td><td>{fr(TOTAL_RISE-BP_TOP)}</td></tr>
<tr><td>Pier rod, downhill row</td><td>{fr(X_WALL-RODS_X[0])}</td><td>at grade, {fr(2*RODS_U)} apart across</td></tr>
<tr><td>Pier rod, uphill row</td><td>{fr(X_WALL-RODS_X[1])}</td><td>at grade</td></tr>
<tr><td>First riser face</td><td>{fr(X_WALL)}</td><td>{fr(TOTAL_RISE)} to grade</td></tr>
<tr><td>Landing nosing</td><td>{fr(X_WALL-RUN)}</td><td>0</td></tr>
<tr><td>Tread 6 top / nosing</td><td>{fr(X_WALL-T*5)}</td><td>{fr(TOTAL_RISE-R*6)}</td></tr>
<tr><td>Tread 5 top / nosing</td><td>{fr(X_WALL-T*4)}</td><td>{fr(TOTAL_RISE-R*5)}</td></tr>
<tr><td>Tread 4 top / nosing</td><td>{fr(X_WALL-T*3)}</td><td>{fr(TOTAL_RISE-R*4)}</td></tr>
<tr><td>Tread 3 top / nosing</td><td>{fr(X_WALL-T*2)}</td><td>{fr(TOTAL_RISE-R*3)}</td></tr>
<tr><td>Tread 2 top / nosing</td><td>{fr(X_WALL-T)}</td><td>{fr(TOTAL_RISE-R*2)}</td></tr>
<tr><td>Tread 1 top / nosing</td><td>{fr(X_WALL)}</td><td>{fr(TOTAL_RISE-R)}</td></tr>
</tbody></table></div>
"""

drill_tbl = f"""
<div class="scroll"><table class="grid">
<thead><tr><th>Height above post base</th><th>Stair posts, treads 1 and 4</th><th>Landing post, stair face</th><th>Landing post, level face</th></tr></thead>
<tbody>
<tr><td>Cable 1</td><td>{fr(CH0+CHS*0)}</td><td>{fr(TH0+THS*0)}</td><td>{fr(TL0+TLS*0)}</td></tr>
<tr><td>Cable 2</td><td>{fr(CH0+CHS*1)}</td><td>{fr(TH0+THS*1)}</td><td>{fr(TL0+TLS*1)}</td></tr>
<tr><td>Cable 3</td><td>{fr(CH0+CHS*2)}</td><td>{fr(TH0+THS*2)}</td><td>{fr(TL0+TLS*2)}</td></tr>
<tr><td>Cable 4</td><td>{fr(CH0+CHS*3)}</td><td>{fr(TH0+THS*3)}</td><td>{fr(TL0+TLS*3)}</td></tr>
<tr><td>Cable 5</td><td>{fr(CH0+CHS*4)}</td><td>{fr(TH0+THS*4)}</td><td>{fr(TL0+TLS*4)}</td></tr>
<tr><td>Cable 6</td><td>{fr(CH0+CHS*5)}</td><td>{fr(TH0+THS*5)}</td><td>{fr(TL0+TLS*5)}</td></tr>
<tr><td>Cable 7</td><td>{fr(CH0+CHS*6)}</td><td>{fr(TH0+THS*6)}</td><td>{fr(TL0+TLS*6)}</td></tr>
<tr><td>Cable 8</td><td>{fr(CH0+CHS*7)}</td><td>{fr(TH0+THS*7)}</td><td>{fr(TL0+TLS*7)}</td></tr>
<tr><td>Cable 9</td><td>{fr(CH0+CHS*8)}</td><td>{fr(TH0+THS*8)}</td><td>{fr(TL0+TLS*8)}</td></tr>
<tr><td>Cable 10</td><td>{fr(CH0+CHS*9)}</td><td>{fr(TH0+THS*9)}</td><td>{fr(TL0+TLS*9)}</td></tr>
<tr><td>Through bolts</td><td>2-1/2" and 5-3/4"</td><td>2-1/2" and 5-3/4"</td><td>same holes</td></tr>
<tr><td>Handrail bracket taps</td><td>33" and 37", inboard face</td><td>30-3/4" and 34-3/4"</td><td>–</td></tr>
<tr><td>Post length</td><td>{fr(POST_LEN)}</td><td>35-1/2"</td><td>35-1/2"</td></tr>
<tr><td>Hole size</td><td colspan="3">Cable 5/16" clearance, drilled at the rake where noted, chamfered and deburred both faces. Handrail taps 1/4-20, plugged with stainless button heads until the rail is fitted.</td></tr>
<tr><td>Base</td><td colspan="3">Stair posts: the spigot stem is welded to the tread frame in the shop, so there is nothing to drill at the base. Notch the outboard ash plank 3-1/8" square around each post.</td></tr>
</tbody></table></div>
"""

survey = """
<p>Everything below is taken to one datum: <b>top of the concrete wall at the upper stairwell</b>. Record the date and who shot it. Values marked on other sheets as assumed are replaced by these once recorded.</p>
<div class="scroll"><table class="grid survey">
<thead><tr><th>Group</th><th>What to record</th><th>What it locks</th></tr></thead>
<tbody>
<tr><td rowspan="3">Stairs</td><td>Finish grade at the first riser face, each flight</td><td>Total rise and riser height</td></tr>
<tr><td>Top of wall at each flight</td><td>Total rise; confirms 48-1/8 &plusmn; 3/8</td></tr>
<tr><td>Cross-slope of the bearing plane at the base, each flight</td><td>Whether the M1 level cut is trimmed at dry fit and by how much</td></tr>
<tr><td rowspan="3">Piers</td><td>Top of pier or paver where M4 bears</td><td>M2b stub length and the base elevation</td></tr>
<tr><td>Flatness across all four rods, straightedge</td><td>Whether the weldment sits flat or the cut is trimmed</td></tr>
<tr><td>Rod positions from the first riser face, spacing across, and stickup</td><td>M4 hole layout; currently 3/4 and 5-1/4, 5-1/4 apart, 1/2 dia</td></tr>
<tr><td rowspan="3">Wall</td><td>Top of wall along its length</td><td>Whether the level runs are truly level</td></tr>
<tr><td>Plumb of the face at the stringer plate</td><td>Every horizontal dimension on S-105 starts here</td></tr>
<tr><td>Rebar scan at the wall plate and each spigot</td><td>Anchor layout between the verticals</td></tr>
<tr><td rowspan="3">Paver path</td><td>Elevation at each post location on the 16 ft 6 in run</td><td>Confirms the 4.5&deg; rake and 15-1/2 in rise</td></tr>
<tr><td>Elevation at each end of the raked run</td><td>Rake angle and top plate cut</td></tr>
<tr><td>Step heights as built</td><td>Guard height above each surface</td></tr>
<tr><td rowspan="2">Angles</td><td>Actual plan angle at the 110&deg; corner</td><td>Compound miter and blade tilt</td></tr>
<tr><td>Any other non-90 corner</td><td>L spline angles</td></tr>
<tr><td rowspan="2">Gates</td><td>Paver elevation at each jamb</td><td>Leaf height and ground clearance</td></tr>
<tr><td>Paver elevation across the swing arc</td><td>Whether the leaf clears when open</td></tr>
<tr><td>Guard extent</td><td>At final grade, the point past the 110&deg; corner where grade within 36 in falls under 30 in below the walk</td><td>Last required guard post; everything past is garden fence</td></tr>
</tbody></table></div>
<p><b>Assumptions this survey confirms.</b> The 16 ft 6 in run is drawn as a continuous 4.5&deg; rake over 15-1/2 in of rise. Pier top taken at finish grade. Wall taken as plumb and its top as level. Total rise taken as 48-1/8.</p>
"""

html_sheets = [
    sheet("S-001", "General notes and hold points", gen_notes),
    sheet("S-002", "Field survey checklist", survey),
    sheet("S-101", "Side elevation", fig(side_elev(), "The stair weldment carries no guard steel. Posts stand on the tread frame end tubes: centred on treads 1 and 4, in line with the nose on the landing.", "big")),
    sheet("S-102", "Plan", fig(plan(), "Plates, collars, stubs, base plate and the 3 in frame end tubes hidden below. Guard posts shown at 22-1/2\" each side of centreline, standing on the end tubes through notches in the ash.", "big")),
    sheet("S-103", "Typical tread, front elevation", fig(tread_section(), "All seven treads are built the same way. Frame front member solid; everything inside the frame hidden.", "big") + fig(tread_centre_detail(), "The stub drops between the collars with 1/16 clearance each side. Two through bolts at dry fit hold it: 13/32 round in the stub, slotted vertically in the collars.", "big")),
    sheet("S-104", "Guard post mounting, front elevation", fig(post_section(), "The 2-1/2 stem is welded to the 3 in end tube of the tread frame, and both planks are notched at each end around the post. The post sleeves over the stem and through-bolts, same as at the wall.", "big")),
    sheet("S-105", "Setting out", fig(setout(), "All stair geometry dimensioned from two datums: the top of the wall and the wall face.", "big")),
    sheet("S-107", "Setting-out table", setout_tbl),
    sheet("S-106", "Guard post drilling schedule", fig(drilling(), "Every hole in the three stair posts, repeated on both sides of the stair. Stair holes are drilled at 31.43° to the rake; at the landing post the stair and level holes are each offset 3/4\" off the face centreline so the internal fittings pass each other.", "big") + "<h3>Hole schedule</h3>" + drill_tbl),
    sheet("S-501", "Base connection", fig(base_detail(), "Tread 1 base. The M2b stub rises off M4 into the tread frame collar; round washers on the rods clear its walls.", "big")),
    sheet("S-502", "Wall connection", fig(wall_detail(), "Top connection. The landing tread is a plain tread.", "big") + fig(wall_face(), "Wall plate face, six anchors.", "big")),
    sheet("S-503", "Stringer, plate and collar fabrication", fig(stringer_cut(), "M1 cut and stub layout along the tube axis. Six stubs on the stringer; tread 1 sits on M2b off the base plate.", "big") + fig(saddles(), "Plate and collars, seen from below. Same at every tread. Set the 1/16 gaps with shims while tacking.", "big")),
    sheet("S-504", "Stub and open riser check", fig(stub(), "M2 stub cut, 3 in in the run direction.", "big") + fig(sphere(), "4 in sphere check at the open risers.", "big")),
    sheet("S-505", "Tread frame fabrication", fig(tread_frame_plan(), "Seven identical frames. Build on a flat jig and check both diagonals before welding out. Set the plate between the collars on 1/16 shims so any frame fits any stub. Red: 7/32 plank screw holes, which also vent the frame; on the landing tread omit the front hole in each end member.", "big") + fig(tread_frame_section(), "Section through the frame at the stub.", "big")),
    sheet("S-506", "Base plate fabrication", fig(base_plate(), "Rod holes are drilled at dry fit to the rods as found; the positions shown are as measured.", "big")),
    sheet("S-601", "Material and cut list", bom),
    sheet("S-602", "Weld schedule and sequence", "<h3>Weld schedule</h3>" + welds + "<h3>Fabrication sequence</h3>" + seq),
    sheet("S-603", "Finish schedule", finish),
]

nav = "".join(f'<a href="#s{n}"><b>{n}</b>{t}</a>' for n, t in SHEETS)
css = open('css.txt').read() + "\n.cmplan{fill:color-mix(in srgb,var(--steel) 70%,transparent);stroke:var(--ink);stroke-width:1}\n"

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mono stringer stair — preliminary drawing set, rev C</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Mono stringer stair,<br>7 risers to retaining wall</h1>
<p>Mono stringer stair, two flights. Ash planks on steel tread frames, each dropped over its stub between two collars, guard stems welded to the tread frame end tubes. {fr(TOTAL_RISE)} rise, {fr(RUN)} run plus a flush landing tread, {DEG:.2f}°.</p></div>
<div class="stamp">PRELIMINARY<br>not for construction<br>engineer review required</div></header>
<nav aria-label="Sheets">{nav}</nav>
<main>{''.join(html_sheets)}</main></body></html>"""

open("out/mono-stringer-drawings.html", "w").write(html)
print("XT", round(XT, 3), "LONG", round(LONG_PT, 3), "SHORT", round(SHORT_PT, 3),
      "stub", round(STUB_LONG, 3), round(STUB_SHORT, 3), "wt", round(w_total))

import json
open("part_S.html", "w").write("".join(html_sheets))
json.dump(SHEETS, open("part_S.json", "w"))


