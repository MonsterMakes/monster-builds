# Study only: side-profile comparison of a 3 in and a 6 in stub.
# Reads gen3.py without changing it, and writes its own page. Nothing in the drawing set moves.
src = open('gen3.py').read().replace(
    'open("out/mono-stringer-drawings.html", "w").write(html)', 'pass').replace(
    'open("part_S.html", "w").write("".join(html_sheets))', 'pass')

A, B = {}, {}
exec(src, A)                                   # as drawn, SW = 3
exec(src.replace('SW = 3.0', 'SW = 6.0', 1), B)  # study, SW = 6


def panel(ns, lo, hi, S, pid, dims=True, marks=True):
    D, T, R, fr = ns['D'], ns['T'], ns['R'], ns['fr']
    SH, WOOD, DV = ns['SH'], ns['WOOD'], ns['DV']
    s_top, xc, sad_bot = ns['s_top'], ns['xc'], ns['sad_bot']
    x0 = T * (lo - 1) - 2.5
    x1 = T * hi + 2.5
    deep = DV + 2 if hi > lo else 5.5
    y0 = s_top(x0) - deep
    y1 = R * hi + 3.5
    d = D(x0 - (6 if dims else 2), x1 + (15 if marks else 2), y0, y1, S, pid)
    ns['draw_stringer'](d)
    for n in range(lo, hi + 1):
        ns['draw_tread'](d, n)
    # nosing line and clipped stringer ends
    SL = ns["SL"]
    d.line(x0 - 1, SL * (x0 - 1) + R, x1 + 1, SL * (x1 + 1) + R, "cl")
    for xb in (x0 - 0.5, x1 + 0.5):
        d.line(xb, s_top(xb) + 0.9, xb, s_top(xb) - deep + 1.2, "brk")
    if dims:
        n = lo + 1 if hi > lo else lo
        d.dim((T * (n - 1) - 1.2, R * n), (T * (n - 1) - 1.2, R * (n - 1)), -1.4, fr(R))
        d.dim((T * (n - 1) - 1.2, R * (n - 1)), (T * (n - 1) - 1.2, R * n - WOOD), -4.2, fr(R - WOOD) + " clear")
        d.dim((T * n + 1.0, R * n), (T * n + 1.0, R * n - WOOD), -1.4, fr(WOOD))
        c = xc(n)
        d.dim((c - SH, s_top(c)), (c + SH, s_top(c)), -(deep - 0.8), fr(2 * SH) + " in the run")
    if marks:
        n = hi
        c = xc(n)
        sec = "4×3" if SH < 2 else "6×4"
        d.tag(c, (sad_bot(n) + s_top(c)) / 2, x1 + 1.5, R * n - 1.5, "M2",
              f"HSS {sec}×1/4 stub|{fr(2*SH, unit='')} in the run, 4 across")
        d.tag(T * (n - 1) + 2, R * n - 1.75, x1 + 1.5, R * n + 2.2, "W1", "Ash planks, 1-3/4")
        d.tag(T * (n - 1) + 1, R * n - WOOD + 0.75, x1 + 1.5, R * n - 5.0, "M7", "Tread frame, 1-1/2")
    return d.svg("Side profile study")



def flight(ns, S, pid):
    D, T, R, fr = ns['D'], ns['T'], ns['R'], ns['fr']
    SH, WOOD, DV, SL = ns['SH'], ns['WOOD'], ns['DV'], ns['SL']
    s_top, xc, sad_bot = ns['s_top'], ns['xc'], ns['sad_bot']
    NB, X_WALL, TOTAL_RISE, BP_TOP = ns['NB'], ns['X_WALL'], ns['TOTAL_RISE'], ns['BP_TOP']
    d = D(-16, X_WALL + 30, -8, TOTAL_RISE + 12, S, pid)
    d.line(-14, 0, X_WALL, 0, "grade")
    d.rect(-14, -1.8, X_WALL, 0, "GR none")
    ns['draw_wall'](d)
    ns['draw_base'](d)
    ns['draw_stringer'](d)
    ns['draw_wallplate'](d)
    for n in range(1, NB + 1):
        ns['draw_tread'](d, n)
    d.line(-4, SL * -4 + R, X_WALL + 4, SL * (X_WALL + 4) + R, "cl")
    d.dim((-8, TOTAL_RISE), (-8, 0), -2.4, fr(TOTAL_RISE) + " total rise")
    d.dim((-4, R), (-4, 0), -1.0, fr(R))
    d.dim((0, -3.2), (T, -3.2), -1.0, fr(T))
    d.dim((0, -3.2), (X_WALL, -3.2), -3.6, fr(X_WALL) + " first riser to wall")
    c1 = xc(1)
    d.tag(c1, (BP_TOP + sad_bot(1)) / 2, X_WALL + 5, R * 2 + 2, "M2b",
          f"Tread 1 stub on the base plate|{fr(2*SH, unit='')} in the run, 4 across")
    c4 = xc(4)
    d.tag(c4, (sad_bot(4) + s_top(c4)) / 2, X_WALL + 5, R * 4 + 2, "M2a",
          f"Stubs on the stringer, treads 2 to 7|{fr(2*SH, unit='')} in the run, 4 across")
    d.tag(20, BP_TOP - 0.1, X_WALL + 5, R - 2, "M4", "Base plate on the pier")
    d.tag(X_WALL - 0.3, TOTAL_RISE - 12, X_WALL + 5, TOTAL_RISE + 4, "M6", "Wall plate")
    return d.svg("Full flight side elevation")


def fig(svg, cap):
    return f'<figure><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


css = open('css.txt').read() + """
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
.cover,nav,main{max-width:1420px}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:26px;align-items:start}
.pair h3{margin:0 0 8px}
.sheet{padding:18px}
.hold{font:700 11px 'Archivo Narrow',sans-serif;color:var(--hold);border:1px solid var(--hold);border-radius:3px;padding:0 4px}
figcaption{margin-top:8px}
.note{color:var(--ink2);font-size:14px;max-width:80ch}
@media (max-width:640px){.pair{grid-template-columns:1fr}}
"""

FLIGHT = """
<article class="sheet">
<h2>Full flight, {rise} total rise</h2>
<h3>As drawn, 3 in the run</h3>
{f3}
<h3>Study, 6 in the run</h3>
{f6}
<p class="note">Seven treads including the landing tread. Tread 1 stands on M2b off the base plate; treads 2 to 7 stand on stubs welded to the stringer. The stair is 48-1/8 of total rise, seven risers at 6-7/8, so this is the 4 ft flight.</p>
</article>
"""

rows = f"""
<article class="sheet">
<h2>Two treads, side profile</h2>
<div class="pair">
<div><h3>As drawn, 3 in the run</h3>{fig(panel(A, 2, 3, 13.5, 'a3'), "HSS 4×3×1/4 stubs, 4 across the stair and 3 in the run direction.")}</div>
<div><h3>Study, 6 in the run</h3>{fig(panel(B, 2, 3, 13.5, 'b3'), "HSS 6×4×1/4 stubs, same 4 across, 6 in the run direction.")}</div>
</div>
<p class="note">Everything else is identical: the same 6-7/8 riser, 11-1/4 run, 3-5/8 open riser, the same tread frame and ash, and the same stringer on the same line. Only the stub's dimension in the run direction changes.</p>
</article>

<article class="sheet">
<h2>One connection, enlarged</h2>
<div class="pair">
<div><h3>3 in the run</h3>{fig(panel(A, 3, 3, 26, 'a1', dims=True, marks=False), "The stub crosses the open riser as a slim leg; the frame and collars are dashed behind the ash.")}</div>
<div><h3>6 in the run</h3>{fig(panel(B, 3, 3, 26, 'b1', dims=True, marks=False), "At 6 the stub fills roughly half the visible gap between treads.")}</div>
</div>
</article>
""" + FLIGHT.format(rise=A["fr"](A["TOTAL_RISE"]), f3=fig(flight(A, 11, "fa"), "3 in the run, the whole flight from the pier to the wall."), f6=fig(flight(B, 11, "fb"), "6 in the run, everything else unchanged."))

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Stub width study – side profile</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Stub width study</h1>
<p>Side profile of the upper stair with the stub at 3 in the run, as drawn, beside the same stair with a 6 in stub. Drawn from the same model as the drawing set, rev O.</p></div>
<div class="stamp">Study only<br>not a design change</div></header>
<main>{rows}</main></body></html>"""
open('out/stub-width-study.html', 'w').write(html)
print("ok")

