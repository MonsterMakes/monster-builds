import math
from fractions import Fraction

# ---------------------------------------------------------------- geometry
R = 6.875          # riser
T = 11.25          # tread run
N = 6              # treads
SL = R / T
ANG = math.atan(SL)
COS, SIN = math.cos(ANG), math.sin(ANG)
DEG = math.degrees(ANG)
WOOD = 3.25          # tread assembly: 1-1/2 frame + 1-3/4 ash plank
PAD = 0.0625
PL = 0.375           # centre plate, flush with the frame top
STACK = (WOOD - 1.5) + PL + PAD  # tread top to stub top: ash + centre plate + pad
STUB_CL = 6.0                    # stub length at centerline, 1-1/2 of it inside the frame
C = -STACK + (SL * 5.625 - (R - STACK)) * 0  # placeholder
# stub top at tread n centre = SL*xc - 0.6875 ; stringer top = that - STUB_CL
C = -(STACK - 3.4375) - STUB_CL
DV = 8 / COS                     # vertical depth of 8" tube
BP_TOP, BP_BOT = 0.5, 0.0
RUN = T * N                      # nosing to landing nosing
X_WALL = T * (N + 1)             # landing tread back edge = wall face
NB = N + 1                       # boards incl. landing tread
X_END = X_WALL - 0.5
TOTAL_RISE = 7 * R


def s_top(x):
    return SL * x + C


XT = (BP_TOP - C) / SL           # top-face toe on base plate
XB = XT + DV / SL                # bottom-face toe
YT = s_top(X_END)
YB = YT - DV
WP_C = (YT + YB) / 2
WP_TOP = WP_C + 6
WP_BOT = WP_TOP - 16
AN_T, AN_B = WP_TOP - 4, WP_BOT + 2
WP_MID = (WP_TOP + WP_BOT) / 2
WP_H = 12.0
LONG_PT = (X_END - XT) / COS
SHORT_PT = (X_END - XB) / COS
STUB_LONG = STUB_CL + 2 * SL
STUB_SHORT = STUB_CL - 2 * SL
RODS_X = (0.75, 5.25)
RODS_U = 2.625


def xc(n):
    return T * n - T / 2


def stub_top(n):
    return R * n - STACK


def fr(v, den=16, unit='"'):
    neg = v < 0
    v = abs(v)
    n = round(v * den)
    whole, rem = divmod(n, den)
    if rem:
        f = Fraction(rem, den)
        s = f"{whole}-{f.numerator}/{f.denominator}" if whole else f"{f.numerator}/{f.denominator}"
    else:
        s = f"{whole}"
    return ('-' if neg else '') + s + unit


# ---------------------------------------------------------------- svg helper
class D:
    def __init__(self, x0, x1, y0, y1, S, pid):
        self.x0, self.x1, self.y0, self.y1, self.S, self.pid = x0, x1, y0, y1, S, pid
        self.W = (x1 - x0) * S
        self.H = (y1 - y0) * S
        self.el = []

    def X(self, x):
        return (x - self.x0) * self.S

    def Y(self, y):
        return (self.y1 - y) * self.S

    def add(self, s):
        self.el.append(s)

    def poly(self, pts, cls):
        p = " ".join(f"{self.X(a):.1f},{self.Y(b):.1f}" for a, b in pts)
        self.add(f'<polygon points="{p}" class="{cls}"/>')

    def pline(self, pts, cls):
        p = " ".join(f"{self.X(a):.1f},{self.Y(b):.1f}" for a, b in pts)
        self.add(f'<polyline points="{p}" class="{cls}" fill="none"/>')

    def rect(self, xa, ya, xb, yb, cls, rx=0):
        x, y = self.X(min(xa, xb)), self.Y(max(ya, yb))
        w, h = abs(xb - xa) * self.S, abs(yb - ya) * self.S
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" class="{cls}"/>')

    def line(self, xa, ya, xb, yb, cls):
        self.add(f'<line x1="{self.X(xa):.1f}" y1="{self.Y(ya):.1f}" x2="{self.X(xb):.1f}" y2="{self.Y(yb):.1f}" class="{cls}"/>')

    def circle(self, x, y, r, cls, px=False):
        rr = r if px else r * self.S
        self.add(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{rr:.1f}" class="{cls}"/>')

    def text(self, x, y, s, cls="t", anchor="start", dx=0, dy=0, rot=None):
        tx, ty = self.X(x) + dx, self.Y(y) + dy
        r = f' transform="rotate({rot:.2f} {tx:.1f} {ty:.1f})"' if rot is not None else ''
        self.add(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" class="{cls}"{r}>{s}</text>')

    def dim(self, p1, p2, off, label, ext_from=None):
        ax, ay = self.X(p1[0]), self.Y(p1[1])
        bx, by = self.X(p2[0]), self.Y(p2[1])
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = uy, -ux
        o = off * self.S
        sg = 1 if o >= 0 else -1
        a2 = (ax + nx * o, ay + ny * o)
        b2 = (bx + nx * o, by + ny * o)
        g = 3 * sg
        e = 5 * sg
        self.add(f'<line x1="{ax+nx*g:.1f}" y1="{ay+ny*g:.1f}" x2="{a2[0]+nx*e:.1f}" y2="{a2[1]+ny*e:.1f}" class="ext"/>')
        self.add(f'<line x1="{bx+nx*g:.1f}" y1="{by+ny*g:.1f}" x2="{b2[0]+nx*e:.1f}" y2="{b2[1]+ny*e:.1f}" class="ext"/>')
        self.add(f'<line x1="{a2[0]:.1f}" y1="{a2[1]:.1f}" x2="{b2[0]:.1f}" y2="{b2[1]:.1f}" class="dl"/>')
        tx, ty = (ux + nx) / math.sqrt(2) * 4.5, (uy + ny) / math.sqrt(2) * 4.5
        for P in (a2, b2):
            self.add(f'<line x1="{P[0]-tx:.1f}" y1="{P[1]-ty:.1f}" x2="{P[0]+tx:.1f}" y2="{P[1]+ty:.1f}" class="tick"/>')
        ang = math.degrees(math.atan2(uy, ux))
        if ang > 90.01 or ang < -90.01:
            ang += 180
        mx, my = (a2[0] + b2[0]) / 2 + nx * 7 * sg, (a2[1] + b2[1]) / 2 + ny * 7 * sg
        self.add(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" dominant-baseline="central" class="dt" transform="rotate({ang:.2f} {mx:.1f} {my:.1f})">{label}</text>')

    def tag(self, px, py, tx, ty, mark, label, side="r"):
        X1, Y1, X2, Y2 = self.X(px), self.Y(py), self.X(tx), self.Y(ty)
        self.add(f'<circle cx="{X1:.1f}" cy="{Y1:.1f}" r="2.4" class="dot"/>')
        sh = 12 if side == "r" else -12
        self.add(f'<polyline points="{X1:.1f},{Y1:.1f} {X2:.1f},{Y2:.1f} {X2+sh:.1f},{Y2:.1f}" class="ldr" fill="none"/>')
        bx = X2 + sh + (13 if side == "r" else -13)
        self.add(f'<circle cx="{bx:.1f}" cy="{Y2:.1f}" r="12.5" class="bub"/>')
        self.add(f'<text x="{bx:.1f}" y="{Y2:.1f}" text-anchor="middle" dominant-baseline="central" class="bt">{mark}</text>')
        lx = bx + (17 if side == "r" else -17)
        anc = "start" if side == "r" else "end"
        lines = label.split("|")
        for i, ln in enumerate(lines):
            yy = Y2 + (i - (len(lines) - 1) / 2) * 13
            self.add(f'<text x="{lx:.1f}" y="{yy:.1f}" text-anchor="{anc}" dominant-baseline="central" class="lt">{ln}</text>')

    def note(self, x, y, lines, cls="nt", anchor="start"):
        for i, ln in enumerate(lines.split("|")):
            self.text(x, y, ln, cls, anchor, dy=i * 13)

    def svg(self, title):
        p = self.pid
        defs = f'''<defs>
<pattern id="{p}cc" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" class="ccb"/><circle cx="3" cy="4" r="1" class="ccd"/><circle cx="10" cy="9" r="1.4" class="ccd"/><path d="M6 12 l3 -2 l1 3z" class="ccd"/></pattern>
<pattern id="{p}wd" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(0)"><rect width="10" height="10" class="wdb"/><path d="M0 3 Q5 1 10 3 M0 8 Q5 6.5 10 8" class="wdl"/></pattern>
<pattern id="{p}st" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" class="stb"/><line x1="0" y1="0" x2="0" y2="6" class="stl"/></pattern>
<pattern id="{p}gr" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="8" class="grl"/></pattern>
</defs>'''
        body = "\n".join(self.el).replace("url(#", f"url(#{p}")
        body = body.replace('class="CC', f'fill="url(#{p}cc)" class="').replace('class="WD', f'fill="url(#{p}wd)" class="').replace('class="STH', f'fill="url(#{p}st)" class="').replace('class="GR', f'fill="url(#{p}gr)" class="')
        return f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}" width="{self.W:.0f}" height="{self.H:.0f}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">{defs}{body}</svg>'




