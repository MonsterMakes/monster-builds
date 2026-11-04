# Drawings made for the Part guide. Exec'd inside gen_parts.py after g is loaded.
import math as _m
D, fr = g['D'], g['fr']
XT_, XB_, SL_ = g['XT'], g['XB'], g['SL']


# ---------------------------------------------------------------- isometric helper
class Iso:
    def __init__(self, cam=(-0.55, -0.62, 0.58)):
        n = _m.sqrt(sum(c * c for c in cam)); self.c = [c / n for c in cam]
        c = self.c
        r = (-c[1], c[0], 0.0); rn = _m.hypot(r[0], r[1]); self.r = (r[0] / rn, r[1] / rn, 0.0)
        r = self.r
        self.up = (c[1] * r[2] - c[2] * r[1], c[2] * r[0] - c[0] * r[2], c[0] * r[1] - c[1] * r[0])
        self.items = []  # (layer, svg-fn)

    def P(self, p):
        return (sum(a * b for a, b in zip(p, self.r)), sum(a * b for a, b in zip(p, self.up)))

    def vis(self, pts):
        a, b, c = pts[0], pts[1], pts[2]
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        return sum(n[i] * self.c[i] for i in range(3)) > 1e-9

    def box(self, u0, u1, v0, v1, w0, w1, cls):
        """Faces listed counter-clockwise seen from outside."""
        F = [
            [(u0, v0, w1), (u1, v0, w1), (u1, v1, w1), (u0, v1, w1)],  # top
            [(u0, v0, w0), (u0, v1, w0), (u1, v1, w0), (u1, v0, w0)],  # bottom
            [(u0, v0, w0), (u1, v0, w0), (u1, v0, w1), (u0, v0, w1)],  # -v
            [(u1, v1, w0), (u0, v1, w0), (u0, v1, w1), (u1, v1, w1)],  # +v
            [(u0, v1, w0), (u0, v0, w0), (u0, v0, w1), (u0, v1, w1)],  # -u
            [(u1, v0, w0), (u1, v1, w0), (u1, v1, w1), (u1, v0, w1)],  # +u
        ]
        tone = ["T", "B", "S", "S", "F", "F"]
        return [(f, cls + tone[i]) for i, f in enumerate(F) if self.vis(f)]


def _hull(pts):
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
    if len(pts) < 3: return pts
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def base_iso():
    I = Iso()
    polys = []   # (2d pts, cls) in draw order

    def add_faces(faces):
        for f, cls in faces:
            polys.append(([I.P(p) for p in f], cls))

    def cyl(u, v, w0, w1, r, cls, n=24, sides=None):
        k = sides or n
        off = _m.pi / 6 if sides else 0
        ring = lambda w: [(u + r * _m.cos(off + 2 * _m.pi * i / k), v + r * _m.sin(off + 2 * _m.pi * i / k), w) for i in range(k)]
        body = _hull([I.P(p) for p in ring(w0) + ring(w1)])
        polys.append((body, cls + "S"))
        polys.append(([I.P(p) for p in ring(w1)], cls + "T"))

    def rod(u, v):
        cyl(u, v, 0.5, 0.625, 0.625, "iw")            # washer 1-1/4 OD
        cyl(u, v, 0.625, 1.0625, 0.433, "in", sides=6)  # nut
        cyl(u, v, 1.0625, 1.45, 0.34, "in")           # acorn body
        cyl(u, v, 1.45, 1.62, 0.22, "in")              # acorn dome, stepped

    # pier and flashing
    add_faces(I.box(-2.25, 29.25, -6.75, 6.75, -0.0625, 0, "if"))
    # plate
    add_faces(I.box(-1.5, 28.5, -6, 6, 0, 0.5, "is"))
    # rods behind the stub
    rod(5.25, 2.625)
    rod(0.75, 2.625)
    # stringer, clipped
    clip = 25.0
    wt = lambda u: 0.5 + (u - XT_) * SL_
    wb = lambda u: 0.5 + (u - XB_) * SL_
    side = [(XT_, -2, 0.5), (XB_, -2, 0.5), (clip, -2, wb(clip)), (clip, -2, wt(clip))]
    top = [(XT_, -2, 0.5), (clip, -2, wt(clip)), (clip, 2, wt(clip)), (XT_, 2, 0.5)]
    for f, c in ((top, "isT"), (side, "isS")):
        if I.vis(f): polys.append(([I.P(p) for p in f], c))
    brk = [I.P((clip, -2, wt(clip) + 0.6)), I.P((clip, -2, wb(clip) - 0.6))]
    # stub
    su0, su1, sw1 = 2.625, 8.625, 0.5 + 4.125
    add_faces(I.box(su0, su1, -2, 2, 0.5, sw1, "is"))
    polys.append(([I.P(p) for p in [(su0 + .25, -1.75, sw1), (su1 - .25, -1.75, sw1), (su1 - .25, 1.75, sw1), (su0 + .25, 1.75, sw1)]], "iv"))
    # rods in front
    rod(5.25, -2.625)
    rod(0.75, -2.625)

    xs = [x for p, _ in polys for x, _ in p]; ys = [y for p, _ in polys for _, y in p]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = (x1 + 19) - x0
    d = D(x0, x1 + 19, y0 - 1, y1 + 1, 1000 / span, "iso")
    for p, c in polys:
        d.poly(p, c + " io")
    d.line(brk[0][0], brk[0][1], brk[1][0], brk[1][1], "brk")
    T = lambda u, v, w: I.P((u, v, w))
    lab = x1 + 2.5
    tags = [
        (T(clip - 3, -2, wt(clip - 3) - 3), "M1", "Stringer, level cut on M4,|1/4 fillet all around"),
        (T(5.625, -2, 3.2), "M2b", "Tread 1 stub, HSS 6×4×1/4 × 4-3/16,|open top, 1/4 fillet all around"),
        (T(5.25, -2.625, 1.3), "A2", "Existing 1/2 rods: washer,|nut and acorn cap"),
        (T(24, -6, 0.3), "M4", "Base plate, PL 1/2 × 12 × 30"),
        (T(27, -6.75, -0.03), "F", "Self-adhered flashing under M4"),
    ]
    tags.sort(key=lambda t: -t[0][1])
    prev = y1 + 10
    gap = 44 / d.S
    for p, m, l in tags:
        ty = min(p[1], prev - gap)
        d.tag(p[0], p[1], lab, ty, m, l)
        prev = ty
    return d.svg("Base plate assembly, view from downhill")


# ---------------------------------------------------------------- plan, horizontal
def base_plan():
    d = D(-10, 50, -12.5, 15.5, 16.5, "bph")
    d.rect(-1.5, -6, 28.5, 6, "steel ob")
    d.rect(2.625, -2, 8.625, 2, "hid")
    d.rect(XT_, -2, XB_, 2, "hid")
    for u in (0.75, 5.25):
        for v in (-2.625, 2.625):
            d.circle(u, v, 0.28125, "void ob")
            d.line(u - 0.55, v, u + 0.55, v, "thin"); d.line(u, v - 0.55, u, v + 0.55, "thin")
    d.line(-3.5, 0, 31, 0, "cl")
    d.line(0, -7.5, 0, 7.5, "thin")
    d.text(0, -5.8, "first riser", "sm", "start", dx=-4, rot=-90)
    d.text(31, 0, "stringer ℄", "sm", "start", dx=4, dy=4)
    # section mark A-A at the uphill rod row
    d.line(5.25, 6.9, 5.25, -6.9, "cl")
    for y in (6.9, -6.9):
        d.text(5.25, y, "A", "tn", "start", dx=5, dy=5)
    # dims along, stacked above
    ys = 6
    for i, (u, lab) in enumerate([(0.75, fr(0.75)), (5.25, fr(5.25)), (5.625, fr(5.625) + " stub ℄"), (XT_, fr(XT_) + " stringer toe"), (XB_, fr(XB_) + " heel")]):
        d.dim((0, ys), (u, ys), 2.2 + i * 1.2, lab)
    d.dim((-1.5, -6), (0, -6), -1.3, fr(1.5))
    d.dim((-1.5, -6), (28.5, -6), -3.0, '30"')
    d.dim((2.625, -2), (8.625, -2), -1.0, "6")
    d.dim((XT_, -2), (XB_, -2), -1.0, fr(XB_ - XT_) + " level cut")
    # dims across, left
    d.dim((-1.5, 2.625), (-1.5, -2.625), -1.4, fr(5.25))
    d.dim((-1.5, 6), (-1.5, -6), -3.2, '12"')
    d.dim((7.125, 2), (7.125, -2), -1.0, "4")
    d.tag(5.25 + 0.2, 2.625 + 0.2, 33, 11.5, "1", "(4) 9/16 rod holes, drilled at dry fit|to the rods as set — HOLD")
    d.tag(6.6, -1.4, 33, 7.5, "2", "M2b stub footprint, 4 across × 6 along,|1/4 fillet all around")
    d.tag(18, 1.2, 33, 3.5, "3", "M1 level cut footprint, 4 wide —|HOLD, moves with the level cut")
    d.tag(26, -4.5, 33, -3.5, "4", "PL 1/2 × 12 × 30, A36")
    d.tag(5.25, -6.9, 33, -7.5, "A", "Section A–A below")
    return d.svg("M4 plan from above, uphill to the right")


# ---------------------------------------------------------------- section across at the uphill rod row
def base_section():
    d = D(-3.8, 16.2, -2.7, 4.4, 50, "bsx")
    d.rect(-3.6, -2.4, 7.5, -0.0625, "CC ob")
    d.line(-3.6, -2.6, -3.6, 0.7, "brk")
    d.rect(-3.6, -0.0625, 6.75, 0, "pad")
    d.rect(-3.6, 0, 6, 0.5, "STH ob")
    top = 3.3
    # far (uphill) stub wall seen beyond, then cut side walls
    d.rect(-1.75, 0.5, 1.75, top, "steel ob")
    for s in (-1, 1):
        d.rect(s * 1.75, 0.5, s * 2.0, top, "STH ob")
        d.poly([(s * 2.0, 0.5), (s * 2.25, 0.5), (s * 2.0, 0.75)], "weld")
        x = s * 2.625
        d.rect(x - 0.28125, 0, x + 0.28125, 0.5, "void")
        d.rect(x - 0.25, -2.2, x + 0.25, 1.5, "nut")
        d.rect(x - 0.625, 0.5, x + 0.625, 0.625, "nut")
        d.rect(x - 0.375, 0.625, x + 0.375, 1.0625, "nut")
        d.rect(x - 0.34, 1.0625, x + 0.34, 1.45, "nut")
        d.add(f'<path d="M {d.X(x-0.34):.1f} {d.Y(1.45):.1f} A {0.34*d.S:.1f} {0.3*d.S:.1f} 0 0 1 {d.X(x+0.34):.1f} {d.Y(1.45):.1f} Z" class="nut"/>')
        d.poly([(s * 2.0, 0.5), (s * 2.25, 0.5), (s * 2.125, 0.5625), (s * 2.0, 0.625)], "clash")
    d.line(-1.9, top + 0.12, 1.9, top + 0.12, "brk")
    d.line(0, -2.6, 0, 3.7, "cl")
    d.line(2.625, -2.6, 2.625, 2.3, "cl")
    d.dim((0, 2.9), (2.0, 2.9), 0.5, "2")
    d.dim((0, 3.3), (2.625, 3.3), 0.6, fr(2.625))
    d.dim((2.0, 1.8), (2.625, 1.8), 0, "5/8")
    d.dim((2.0, -0.35), (3.25, -0.35), -0.5, '1-1/4 OD')
    d.tag(2.07, 0.54, 8.2, 4.0, "C", "Washer overlaps the stub's 1/4 fillet|by 1/4 — open question")
    d.tag(1.88, 2.6, 8.2, 2.9, "M2b", "Stub walls cut; the uphill wall beyond")
    d.tag(2.9, 1.3, 8.2, 1.7, "A2", "1/2 rod, washer, nut and acorn cap")
    d.tag(4.5, 0.25, 8.2, 0.5, "M4", "PL 1/2, hatched where cut")
    d.tag(6.4, -0.03, 8.2, -0.7, "F", "Flashing")
    d.text(-1.2, -1.6, "existing pier", "sm", "middle")
    d.text(-3.4, 3.9, "symmetric about ℄", "sm", "start")
    return d.svg("Section A–A across M4 at the uphill rod row, looking uphill")


# ---------------------------------------------------------------- section 2: wall plate
def wall_iso():
    """M6 on the wall face with the stringer's plumb cut welded to it, seen from below and outboard."""
    I = Iso(cam=(-0.56, -0.52, 0.52))
    WP_TOP_, WP_BOT_, YT_, YB_ = g['WP_TOP'], g['WP_BOT'], g['YT'], g['YB']
    AN = g['AN_Y']
    polys = []

    def add(faces):
        for f, cls in faces:
            polys.append(([I.P(p) for p in f], cls))

    def cyl(u, v, w, du, r, cls, n=20):
        ring = lambda uu: [(uu, v + r * _m.cos(2 * _m.pi * i / n), w + r * _m.sin(2 * _m.pi * i / n)) for i in range(n)]
        polys.append((_hull([I.P(p) for p in ring(u) + ring(u + du)]), cls + "S"))
        polys.append(([I.P(p) for p in ring(u + du)], cls + "T"))

    # wall face at u = 0, wall body behind it (u > 0)
    add(I.box(0, 6, -11, 11, WP_BOT_ - 5, WP_TOP_ + 5, "ic"))
    # plate, 1/2 thick, standing off the wall face
    add(I.box(-0.5, 0, -6, 6, WP_BOT_, WP_TOP_, "is"))
    # stringer, plumb cut on the plate, running downhill (u negative)
    clip = -22.0
    sl = g['SL']
    drop = sl * abs(clip + 0.5)
    side = lambda v: [(-0.5, v, YT_), (-0.5, v, YB_), (clip, v, YB_ - drop), (clip, v, YT_ - drop)]
    polys.append(([I.P(p) for p in side(-2)], "isS"))
    topf = [(-0.5, -2, YT_), (-0.5, 2, YT_), (clip, 2, YT_ - drop), (clip, -2, YT_ - drop)]
    botf = [(-0.5, -2, YB_), (clip, -2, YB_ - drop), (clip, 2, YB_ - drop), (-0.5, 2, YB_)]
    polys.append(([I.P(p) for p in topf], "isT"))
    polys.append(([I.P(p) for p in [(clip, -2, YT_ - drop), (clip, 2, YT_ - drop), (clip, 2, YB_ - drop), (clip, -2, YB_ - drop)]], "isF"))
    endbrk = [I.P((clip, -2, YT_ - drop)), I.P((clip, 2, YB_ - drop))]
    # anchors: rod, washer, nut standing off the plate face
    for v in (-4.5, 4.5):
        for w in AN:
            cyl(-1.4, v, w, 1.4, 0.25, "in")
            cyl(-0.65, v, w, 0.15, 0.55, "iw")
            cyl(-1.05, v, w, 0.40, 0.42, "in")

    xs = [x for p, _ in polys for x, _ in p]; ys = [y for p, _ in polys for _, y in p]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = (x1 + 19) - x0
    d = D(x0, x1 + 19, y0 - 1, y1 + 1, 1000 / span, "wiso")
    for p, c in polys:
        d.poly(p, c + " io")
    d.line(endbrk[0][0], endbrk[0][1], endbrk[1][0], endbrk[1][1], "brk")
    T = lambda u, v, w: I.P((u, v, w))
    tags = [
        (T(-0.25, -5, WP_TOP_ - 1), "M6", "Wall plate, PL 1/2 × 12 × 16"),
        (T(-1.0, -4.5, AN[1]), "A1", "(6) 1/2 threaded rod in adhesive,|nut and washer over M6"),
        (T(-12, -2, YT_ - sl * 11.5 - 1.5), "M1", "Stringer, plumb cut on the plate,|1/4 fillet all around"),
        (T(3, -11, WP_BOT_ - 2), "W", "Concrete wall, 6 in stem"),
    ]
    tags.sort(key=lambda t: -t[0][1])
    prev, gap = y1 + 10, 46 / d.S
    for p, m, l in tags:
        ty = min(p[1], prev - gap)
        d.tag(p[0], p[1], x1 + 2.5, ty, m, l)
        prev = ty
    return d.svg("Wall plate assembly, seen from outboard and below")


# ---------------------------------------------------------------- section 3: stringer weldment
def stringer_iso():
    """M1 with its six stubs, the base plate and the wall plate, seen from downhill and outboard."""
    I = Iso(cam=(-0.54, -0.56, 0.42))
    XTa, XBa, XE = g['XT'], g['XB'], g['X_END']
    YTa, YBa, BP, SLg = g['YT'], g['YB'], g['BP_TOP'], g['SL']
    s_top, xc, stub_top, NB = g['s_top'], g['xc'], g['stub_top'], g['NB']
    WPT, WPB, XW = g['WP_TOP'], g['WP_BOT'], g['X_WALL']
    polys = []

    def add(faces):
        for f, cls in faces:
            polys.append(([I.P(p) for p in f], cls))

    # base plate and the wall
    add(I.box(-1.5, 28.5, -6, 6, 0, BP, "is"))
    add(I.box(XW, XW + 6, -11, 11, WPB - 10, WPT + 4, "ic"))
    polys.append(([I.P(p) for p in [(XW, -6, WPB), (XW, 6, WPB), (XW, 6, WPT), (XW, -6, WPT)]], "isF"))
    # stringer: side face, top face, wall end
    polys.append(([I.P(p) for p in [(XTa, -2, BP), (XBa, -2, BP), (XE, -2, YBa), (XE, -2, YTa)]], "isS"))
    polys.append(([I.P(p) for p in [(XTa, -2, BP), (XTa, 2, BP), (XE, 2, YTa), (XE, -2, YTa)]], "isT"))
    # the six stubs: level top, bottom cut to the stringer's slope. Uphill first so the
    # downhill ones, which are nearer the camera, paint over them.
    def stub(u0, u1, zb0, zb1, ztop):
        polys.append(([I.P(p) for p in [(u0, -2, zb0), (u1, -2, zb1), (u1, -2, ztop), (u0, -2, ztop)]], "isS"))
        polys.append(([I.P(p) for p in [(u0, -2, zb0), (u0, -2, ztop), (u0, 2, ztop), (u0, 2, zb0)]], "isF"))
        polys.append(([I.P(p) for p in [(u0, -2, ztop), (u1, -2, ztop), (u1, 2, ztop), (u0, 2, ztop)]], "isT"))

    for n in range(NB, 1, -1):
        c = xc(n)
        stub(c - 3, c + 3, s_top(c - 3), s_top(c + 3), stub_top(n))
    # tread 1 stub stands square on the base plate
    stub(xc(1) - 3, xc(1) + 3, BP, BP, stub_top(1))

    xs = [x for p, _ in polys for x, _ in p]; ys = [y for p, _ in polys for _, y in p]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = (x1 + 34) - x0
    d = D(x0, x1 + 34, y0 - 1, y1 + 1, 1000 / span, "siso")
    for p, c in polys:
        d.poly(p, c + " io")
    T = lambda u, v, w: I.P((u, v, w))
    tags = [
        (T(xc(5), -2, (s_top(xc(5)) + stub_top(5)) / 2), "M2a", "(6) stubs on the stringer,|HSS 6×4×1/4, 6 at the centreline"),
        (T(xc(1), -2, (BP + stub_top(1)) / 2), "M2b", "Tread 1 stub, on M4, not on M1"),
        (T(40, -2, s_top(40) - 4), "M1", "Mono stringer, HSS 8×4×1/4,|level cut at the base, plumb cut at the wall"),
        (T(20, -6, BP / 2), "M4", "Base plate, part 1"),
        (T(XW, -6, WPT - 2), "M6", "Wall plate, part 2"),
    ]
    tags.sort(key=lambda t: -t[0][1])
    prev, gap = y1 + 10, 46 / d.S
    for p, m, l in tags:
        ty = min(p[1], prev - gap)
        d.tag(p[0], p[1], x1 + 2.5, ty, m, l)
        prev = ty
    return d.svg("Stringer weldment, seen from downhill")



# ---------------------------------------------------------------- section 4: tread frame
def tread_iso():
    """One frame from above and outboard, ash off: mitred corners, stem on the post-tread end."""
    I = Iso(cam=(-0.48, -0.50, 0.72))
    W2, Dp, MEM, MEMP, H = 24.0, 11.25, 2.5, 3.0, 1.5
    CH_ = (Dp - 2 * MEM) / 2
    F, B = -Dp / 2, Dp / 2
    items = []

    def emit(pts3, cls):
        dep = sum(sum(a * b for a, b in zip(p, I.c)) for p in pts3) / len(pts3)
        items.append((dep, [I.P(p) for p in pts3], cls))

    def prism(poly, z0, z1, cls):
        emit([(u, v, z1) for u, v in poly], cls + "T")
        n = len(poly)
        for k in range(n):
            (u0, v0), (u1, v1) = poly[k], poly[(k + 1) % n]
            face = [(u0, v0, z0), (u1, v1, z0), (u1, v1, z1), (u0, v0, z1)]
            if I.vis(face):
                emit(face, cls + ("S" if abs(v1 - v0) > abs(u1 - u0) else "F"))

    prism([(-W2, F), (W2, F), (W2 - MEMP, F + MEM), (-W2 + MEMP, F + MEM)], -H, 0, "is")
    prism([(-W2 + MEMP, B - MEM), (W2 - MEMP, B - MEM), (W2, B), (-W2, B)], -H, 0, "is")
    prism([(W2, F), (W2, B), (W2 - MEMP, B - MEM), (W2 - MEMP, F + MEM)], -H, 0, "is")
    prism([(-W2, B), (-W2, F), (-W2 + MEMP, F + MEM), (-W2 + MEMP, B - MEM)], -H, 0, "is")
    for u in (-12.5, 12.5):
        prism([(u - 0.75, F + MEM), (u + 0.75, F + MEM), (u + 0.75, B - MEM), (u - 0.75, B - MEM)], -H, 0, "is")
    for a, b in ((2.0625, 2.4375), (-2.4375, -2.0625)):
        prism([(a, -CH_), (b, -CH_), (b, CH_), (a, CH_)], -H, 0, "is")
    prism([(-2, -CH_), (2, -CH_), (2, CH_), (-2, CH_)], -0.375, 0, "is")
    prism([(-2, -3), (2, -3), (2, 3), (-2, 3)], -5.5, -0.4375, "is")
    prism([(W2 - MEMP + 0.25, -1.25), (W2 - 0.25, -1.25), (W2 - 0.25, 1.25), (W2 - MEMP + 0.25, 1.25)], 0, 7.0, "is")

    items.sort(key=lambda t: t[0])
    xs = [x for _, p, _ in items for x, _ in p]; ys = [y for _, p, _ in items for _, y in p]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = (x1 + 26) - x0
    d = D(x0, x1 + 26, y0 - 1, y1 + 1, 1000 / span, "tiso")
    for _, p, c in items:
        d.poly(p, c + " io")
    T = lambda u, v, w: I.P((u, v, w))
    tags = [
        (T(W2 - 1.5, -1.25, 5.0), "P1", "Guard stem, post treads only"),
        (T(W2 - 1.5, 1.0, -0.4), "F2", "End member, 3 wide on post treads"),
        (T(12.5, -1.0, -0.4), "F3", "Joist"),
        (T(-6, F + 1.2, -0.4), "F1", "Front member, the nose"),
        (T(2.25, -1.5, -0.9), "M8", "Collars, the stub rises between them"),
        (T(0, 1.5, -0.02), "M3", "Plate, flush with the frame top, over the stub"),
    ]
    tags.sort(key=lambda t: -t[0][1])
    prev, gap = y1 + 10, 44 / d.S
    for p, m, l in tags:
        ty = min(p[1], prev - gap)
        d.tag(p[0], p[1], x1 + 2.5, ty, m, l)
        prev = ty
    return d.svg("Tread frame, one post tread")


# ---------------------------------------------------------------- section 5: spigots
def spigot_iso():
    """Wall spigot: plate on the wall top, stem rising, post sleeved over it, rod below."""
    I = Iso(cam=(-0.52, -0.54, 0.66))
    items = []

    def emit(pts3, cls):
        dep = sum(sum(a * b for a, b in zip(p, I.c)) for p in pts3) / len(pts3)
        items.append((dep, [I.P(p) for p in pts3], cls))

    def prism(poly, z0, z1, cls):
        emit([(u, v, z1) for u, v in poly], cls + "T")
        n = len(poly)
        for k in range(n):
            (u0, v0), (u1, v1) = poly[k], poly[(k + 1) % n]
            face = [(u0, v0, z0), (u1, v1, z0), (u1, v1, z1), (u0, v0, z1)]
            if I.vis(face):
                emit(face, cls + ("S" if abs(v1 - v0) > abs(u1 - u0) else "F"))

    sq = lambda a, b, c, d2: [(a, c), (b, c), (b, d2), (a, d2)]
    prism(sq(-7, 7, -3, 3), -9, 0, "ic")
    prism(sq(-3, 3, -3, 3), 0, 0.375, "is")
    prism(sq(-1.25, 1.25, -1.25, 1.25), 0.375, 10.375, "is")
    prism(sq(-1.5, 1.5, -1.5, 1.5), 7.0, 19.0, "iw")
    prism(sq(-0.28, 0.28, -0.28, 0.28), -6, 0.9, "in")

    items.sort(key=lambda t: t[0])
    xs = [x for _, p, _ in items for x, _ in p]; ys = [y for _, p, _ in items for _, y in p]
    x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    span = (x1 + 30) - x0
    d = D(x0, x1 + 30, y0 - 1, y1 + 1, 760 / span, "spiso")
    for _, p, c in items:
        d.poly(p, c + " io")
    T = lambda u, v, w: I.P((u, v, w))
    tags = [
        (T(0, -1.5, 15), "P", "Guard post, 3×3×3/16, sleeved over the stem|and through-bolted. Part 6"),
        (T(0, -1.25, 5.5), "K5", "Stem, HSS 2-1/2×2-1/2×3/16 × 10"),
        (T(2.0, -3, 0.19), "K5", "Plate, PL 6 × 6 × 3/8, shimmed and|bedded in adhesive"),
        (T(0, -0.28, -3.5), "A", "1/2 316 rod, 6 embed in SET-3G"),
    ]
    tags.sort(key=lambda t: -t[0][1])
    prev, gap = y1 + 10, 46 / d.S
    for p, m, l in tags:
        ty = min(p[1], prev - gap)
        d.tag(p[0], p[1], x1 + 2.5, ty, m, l)
        prev = ty
    return d.svg("Wall spigot, post shown cut away")
