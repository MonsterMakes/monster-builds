# Review only: the revised centre connection and base, drawn from scratch.
# Nothing in the drawing set, the model or the Part guide is touched by this file.
import math
exec(open('head.py').read())   # D, fr, R, T, SL, STACK, PL, PAD, BP_TOP, s_top, xc

FD = 11.25            # frame depth, run direction
F1W, F1H, F1T = 3.0, 1.5, 0.125
NOTCH = 0.5           # new: depth of the notch cut into each F1
CLR = FD - 2 * F1W + 2 * NOTCH          # clear between the notch bottoms = collar length
SWn = 6.0             # new stub, run direction
SAn = 4.0             # stub across, unchanged
CT = 0.375            # collar thickness
CGAP = 4.125          # clear between collars, unchanged
NW = 4.875            # notch width across the stair


def fig(svg, cap):
    return f'<figure><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


# ---------------------------------------------------------------- 1. plan from below
def plan_below():
    d = D(-9.5, 26, -9.8, 9.8, 32, "pb")
    for s in (1, -1):
        # F1 member, notched at the centre
        d.poly([(s * 2.625, -9), (s * 5.625, -9), (s * 5.625, 9), (s * 2.625, 9),
                (s * 2.625, NW / 2), (s * (2.625 + NOTCH), NW / 2),
                (s * (2.625 + NOTCH), -NW / 2), (s * 2.625, -NW / 2)], "steel ob")
        d.line(s * 5.625, 9, s * 2.625, 9, "brk")
        d.line(s * 5.625, -9, s * 2.625, -9, "brk")
        # inner wall line of the tube, and the material removed by the notch
        d.line(s * (2.625 + F1T), -9, s * (2.625 + F1T), -NW / 2, "thin")
        d.line(s * (2.625 + F1T), NW / 2, s * (2.625 + F1T), 9, "thin")
        d.line(s * 2.625, -NW / 2 - 1.4, s * 2.625, NW / 2 + 1.4, "hidc")
        # collars, running into the notches
        d.rect(-CLR / 2, s * (CGAP / 2), CLR / 2, s * (CGAP / 2 + CT), "steel ob")
    d.rect(-SWn / 2, -SAn / 2, SWn / 2, SAn / 2, "hidc")
    d.rect(-CLR / 2, -2.0, CLR / 2, 2.0, "hid")
    for u in (-0.75, 0.75):
        for s in (1, -1):
            d.circle(u, s * (CGAP / 2 + CT / 2), 0.2, "void ob")
    d.line(-8, 0, 8, 0, "cl")
    d.line(0, -8.5, 0, 8.5, "cl")
    d.dim((-CLR / 2, 3.1), (CLR / 2, 3.1), 3.0, fr(CLR) + " collar")
    d.dim((2.625, -NW / 2), (3.125, -NW / 2), -1.1, fr(NOTCH))
    d.dim((3.35, -NW / 2), (3.35, NW / 2), 0, fr(NW) + " notch")
    d.dim((-SWn / 2, -2.0), (SWn / 2, -2.0), -2.2, fr(SWn) + " stub")
    d.dim((-6.4, -CGAP / 2), (-6.4, CGAP / 2), 0, fr(CGAP))
    d.dim((7.0, -SAn / 2), (7.0, SAn / 2), 0, fr(SAn))
    d.tag(2.875, 2.2, 12, 8.2, "F1", "Frame front and back member, notched|1/2 deep × 4-7/8 wide, full height.|Dashed: the original inner face")
    d.tag(1.6, CGAP / 2 + CT, 12, 5.0, "M8", "Collar, now 6-1/4, running into both|notches and welded to F1")
    d.tag(-2.9, -1.0, 12, 2.2, "M2a", "Stub, HSS 6×4×1/4, dashed.|1/16 clear each side of the notch bottoms")
    d.tag(-2.4, 1.2, 12, -0.4, "M3", "Plate above the collars, 4 × 6-1/4,|dashed, flush with the frame top")
    d.tag(0.75, CGAP / 2 + CT / 2, 12, -3.0, "H1", "13/32 through-bolt holes, 1-1/2 apart,|drilled through M8 and the stub at dry fit")
    return d.svg("Centre connection, plan from below")


# ---------------------------------------------------------------- 2. section along the run
def sect_run():
    d = D(-9.5, 26, -7.2, 3.2, 30, "sr")
    d.rect(-9, -1.75, 9, 0, "WD ob")
    d.line(-9, -1.75, -9, 0, "brk"); d.line(9, -1.75, 9, 0, "brk")
    for s in (1, -1):
        x0, x1 = s * (2.625 + NOTCH), s * 5.625
        a, b = min(x0, x1), max(x0, x1)
        d.rect(a, -3.25, b, -1.75, "STH ob")
        d.rect(a + (F1T if s < 0 else 0), -3.25 + F1T, b - (F1T if s > 0 else 0), -1.75 - F1T, "void ob")
        d.line(s * 9, -3.25, x1, -3.25, "thin")
    d.rect(-CLR / 2, -3.25, CLR / 2, -1.75, "STH ob")
    d.rect(-SWn / 2, -6.9, SWn / 2, -3.25, "hid")
    d.rect(-SWn / 2, -3.375, SWn / 2, -3.25, "pad")
    d.rect(-CLR / 2, -2.125, CLR / 2, -1.75, "hidc")
    for u in (-0.75, 0.75):
        d.circle(u, -2.75, 0.2, "void ob")
    d.line(0, -7.0, 0, 1.2, "cl")
    d.dim((-CLR / 2, -3.25), (CLR / 2, -3.25), -0.9, fr(CLR) + " collar, notch to notch")
    d.dim((2.625, -1.75), (3.125, -1.75), 1.0, fr(NOTCH))
    d.dim((-5.625, 0), (5.625, 0), 2.2, fr(FD) + " frame depth")
    d.dim((-0.75, -2.75), (0.75, -2.75), -0.55, "1-1/2")
    d.dim((6.4, 0), (6.4, -1.75), 0, "1-3/4")
    d.dim((6.4, -1.75), (6.4, -3.25), 0, "1-1/2")
    d.tag(4.0, -2.5, 12, 2.4, "F1", "Cut back 1/2 at the centre; the tube is|open here, so both F1s get end drains")
    d.tag(-3.0, -2.2, 12, 0.6, "M8", "Collar, 3/8 × 1-1/2 bar, welded into|the notch at each end")
    d.tag(-1.2, -2.0, 12, -1.6, "M3", "Plate, dashed: it sits between the collars,|out of this cut, flush with the frame top")
    d.tag(-SWn / 2 + 0.5, -5.0, 12, -3.8, "M2a", "Stub, HSS 6×4×1/4, rising 1 in|between the collars")
    d.tag(1.6, -3.31, 12, -5.9, "H2", "1/8 EPDM pad, 6 × 4, on the open stub top")
    d.tag(-4.6, -0.9, 12, 3.9, "W1", "Ash planks, screwed from below")
    return d.svg("Section along the run through one collar")


# ---------------------------------------------------------------- 3. base, M2b and the toe
def base_notch(trim, pid, tag=True):
    XTt = XT - trim
    d = D(-2.0, 31, -1.8, 7.6, 31, "bn" + pid)
    d.rect(-1.5, -1.2, 24, 0, "CC ob")
    d.line(-1.5, -1.4, -1.5, 0.9, "brk"); d.line(24, -1.4, 24, 0.9, "brk")
    d.rect(-1.5, 0, 24, BP_TOP, "steel ob")
    u0, u1 = xc(1) - SWn / 2, xc(1) + SWn / 2
    top = BP_TOP + R - STACK - BP_TOP
    st = R - STACK
    # stringer wedge, level cut starting at the toe
    d.poly([(XTt, BP_TOP), (24, SL * (24 - XTt) + BP_TOP), (24, BP_TOP)], "steel ob")
    if XTt < u1:
        d.rect(u0, BP_TOP, u1, st, "hidc")
        d.rect(u0, BP_TOP, XTt, st, "steel ob")
        d.poly([(XTt, BP_TOP), (24, SL * (24 - XTt) + BP_TOP), (24, BP_TOP)], "steel ob")
        d.poly([(XTt, BP_TOP), (XTt + 0.35, BP_TOP), (XTt, BP_TOP + 0.35)], "weld")
        d.poly([(XTt, st), (XTt - 0.35, st), (XTt, st - 0.35)], "weld")
        d.text((XTt + u1) / 2 + 0.3, st - 0.7, "notched to the toe", "sm", "middle")
    else:
        d.rect(u0, BP_TOP, u1, st, "steel ob")
    d.rect(u0, st, u1, st + 0.125, "pad")
    d.dim((u0, st + 0.4), (u1, st + 0.4), 0.5, fr(SWn))
    d.dim((0, -0.6), (XTt, -0.6), -0.5, fr(XTt) + " toe")
    d.line(0, -1.4, 0, 1.4, "thin")
    d.text(0, -1.4, "first riser", "sm", "start", dx=3, rot=-90)
    if tag:
        d.tag(u1 - 0.3, 1.2, 15, 6.4, "M2b", "Tread 1 stub, 6 in the run")
        d.tag(20, SL * (20 - XTt) + BP_TOP - 0.5, 15, 4.2, "M1", "Stringer level cut")
        d.tag(12, BP_TOP / 2, 15, 2.0, "M4", "Base plate")
    return d.svg("Base, tread 1 stub and the stringer toe")


css = open('css.txt').read() + """
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
.cover,nav,main{max-width:1180px}
.sheet{padding:18px}
.hold{font:700 11px 'Archivo Narrow',sans-serif;color:var(--hold);border:1px solid var(--hold);border-radius:3px;padding:0 4px}
.hidc{fill:none;stroke:var(--ink2);stroke-width:1.1;stroke-dasharray:4 3}
.pair{display:grid;grid-template-columns:1fr;gap:10px}
.note{color:var(--ink2);font-size:14px}
h3{font-family:"Archivo Narrow",sans-serif;font-size:18px;margin:16px 0 8px}
"""

changes = """
<div class="scroll"><table class="grid">
<thead><tr><th>Part</th><th>Rev O</th><th>Proposed</th></tr></thead><tbody>
<tr><td>M2a stubs</td><td>HSS 4×3×1/4, 3 in the run</td><td>HSS 6×4×1/4, 6 in the run, 4 across unchanged, still 6 at the centreline, single 31.43° cut, long point 7-13/16, short point 4-3/16</td></tr>
<tr><td>M2b, tread 1</td><td>HSS 4×3×1/4 × 4-1/8 on M4</td><td>HSS 6×4×1/4 × 4-1/8 on M4, uphill wall notched at dry fit to take the stringer toe, 1/4 fillet all around, ground smooth</td></tr>
<tr><td>F1 front and back</td><td>Plain HSS 3×1-1/2×1/8</td><td>Notched 1/2 deep × 4-7/8 wide at the centre, full height, through the inner wall. Screw holes and miters unchanged</td></tr>
<tr><td>M8 collars</td><td>3/8 × 1-1/2 × 5-1/4, butted between the F1 members, 3/16 fillet at each end</td><td>3/8 × 1-1/2 × 6-1/4, running into both notches, welded to F1 top wall, bottom wall and both cut edges</td></tr>
<tr><td>M3 plate</td><td>3/8 × 4 × 5-1/4</td><td>3/8 × 4 × 6-1/4, still flush with the frame top, still groove welded to the collars and ground flush</td></tr>
<tr><td>H2 stub pad</td><td>1/8 EPDM, 4 × 3</td><td>1/8 EPDM, 6 × 4</td></tr>
<tr><td>Drains</td><td>3/16 in one F1 near each end</td><td>3/16 in both F1 members near each end; the notch opens the tube at the centre</td></tr>
<tr><td>Through bolts</td><td>(2) 3/8 × 5-1/2, 1-1/2 apart</td><td>Unchanged</td></tr>
<tr><td>Weight</td><td>—</td><td>About +4 lb per tread, +28 lb on the flight</td></tr>
</tbody></table></div>
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Proposed rev P – notched connection review</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Proposed rev P</h1>
<p>The 6 in stub with the F1 members notched and the collars welded into them, and the tread 1 stub notched around the stringer toe. Drawn for review. The drawing set is still rev O and nothing has been regenerated.</p></div>
<div class="stamp">For review<br>not yet issued</div></header>
<main>
<article class="sheet"><h2>Marks used here</h2><div class="scroll"><table class="grid"><tbody><tr><td>M1</td><td>Mono stringer, HSS 8×4×1/4</td><td>M2a</td><td>Stub under treads 2 to 7, welded to the stringer</td></tr><tr><td>M2b</td><td>Stub under tread 1, welded to the base plate</td><td>M3</td><td>Plate between the collars, flush with the frame top, caps the open stub</td></tr><tr><td>M4</td><td>Base plate on the pier</td><td>M7</td><td>Tread frame, 48 × 11-1/4</td></tr><tr><td>F1</td><td>Frame front and back members, HSS 3×1-1/2×1/8, the ones being notched</td><td>M8</td><td>Collars, 3/8 × 1-1/2 bar, the pair the stub rises between</td></tr><tr><td>H1</td><td>Tread through bolts, 3/8 × 5-1/2</td><td>H2</td><td>EPDM pad on the stub top</td></tr><tr><td>W1</td><td>Ash planks</td><td>F2, F3</td><td>Frame end members and joists, unchanged</td></tr></tbody></table></div></article>

<article class="sheet"><h2>Centre connection</h2>
{fig(plan_below(), "Looking up at the underside of the frame. The collars now run past the F1 inner faces into a notch in each member. The stub is dashed; M3 sits above the collars, also dashed.")}
{fig(sect_run(), "Cut along the run through one collar. F1 is cut back 1/2 at the centre so the collar lands in it and the 6 in stub clears the notch bottoms by 1/16 a side.")}
</article>

<article class="sheet"><h2>Tread 1 stub and the stringer toe</h2>
<div class="pair">
<div><h3>Design values, no trim</h3>{fig(base_notch(0.0, "a"), "At the drawn toe of 8-11/16 the stub and the stringer clear each other by 1/16, so there is nothing to notch.")}</div>
<div><h3>Toe trimmed 1-1/2 in the field</h3>{fig(base_notch(1.5, "b"), "With the level cut trimmed to the pier as found, the toe moves downhill into the stub. The stub's uphill wall is cut away to the toe, dashed here, and the stringer welds into the notch, ground smooth.")}</div>
</div>
<p class="note">The notch depth is a field dimension <span class="hold">HOLD</span>: it is whatever the trimmed level cut needs, cut at dry fit before coating. The stringer and the stub are both 4 across, so the notch runs the full width of the stub wall.</p>
</article>

<article class="sheet"><h2>What changes</h2>
{changes}
<p class="note">Everything else holds: 48 × 11-1/4 frame, 6-7/8 riser, 11-1/4 run, 3-5/8 open riser, the 1 in collar engagement, the plank screw pattern, the P1 stems and the guard.</p>
</article>
</main></body></html>"""
open('out/revp-review.html', 'w').write(html)
print("ok")

