import json
exec(open('head.py').read())

SHEETS = []


def fig(svg, cap, cls=""):
    return f'<figure class="{cls}"><div class="scroll">{svg}</div><figcaption>{cap}</figcaption></figure>'


def sheet(num, title, body, scale="Not to scale; dimensions govern"):
    SHEETS.append((num, title))
    return (f'<article class="sheet" id="s{num}">'
            f'<header class="tb"><div class="num">{num}</div><div class="ttl"><h2>{title}</h2><p>{scale}</p></div></header>'
            f'<div class="body">{body}</div></article>')


# landing geometry, inches
LL, LO = 45.0, 48.0          # along the house, out from the house
SLAT, SLAT_T, GAP = 2.0, 1.75, 0.375
FR = 3.0                     # HSS 3x3 perimeter depth
TOP = 44.5                   # slat top above grade at the house
JOISTS = (6.0, 18.0, 30.0, 42.0)
NR, RR, TT = 5, 29.0 / 5, 11.25
TREAD = 3.25


# ================================================================= L-101
def plan():
    d = D(-12, 118, -8, 98, 5.2, "lp")
    d.rect(-7, -6, 0, 95, "CC ob")
    d.line(-0.3, 6, -0.3, 38, "rod")
    for i in range(19):
        a = i * (SLAT + GAP)
        d.rect(0, a, LO, a + SLAT, "wdplan ob")
    for n in range(4):
        a = LL + TT * n
        d.rect(0, a, LO, a + TT, "wdplan ob")
        d.text(LO / 2, a + TT / 2, str(n + 1), "tn", "middle")
    d.rect(0, 0, 3, LL, "hid")
    d.rect(LO - 3, 0, LO, LL, "hid")
    d.rect(0, 0, LO, 3, "hid")
    d.rect(0, LL - 3, LO, LL, "hid")
    for o in JOISTS:
        d.rect(o - 1.5, 3, o + 1.5, LL - 3, "hid")
    d.rect(22, LL, 26, LL + 4 * TT, "hid")
    for (o, l) in ((LO - 1.5, 1.5), (LO - 1.5, 22.5), (LO - 1.5, LL - 1.5), (1.5, 1.5), (24, 1.5), (LO - 1.5, LL + TT / 2)):
        d.rect(o - 1.5, l - 1.5, o + 1.5, l + 1.5, "steel ob")
    d.line(LO + 0.6, 0, LO + 0.6, LL + TT, "guard")
    d.line(0, -0.6, LO, -0.6, "guard")
    d.dim((LO, 0), (LO, LL), -6, fr(LL) + " landing")
    d.dim((LO, LL), (LO, LL + 4 * TT), -6, "4 treads at 11-1/4")
    d.dim((0, -4), (LO, -4), 0, fr(LO))
    d.dim((6, LL + 4 * TT), (18, LL + 4 * TT), 3, '12"')
    d.tag(LO / 2, 10, 60, 8, "1", "Ash slats 2 x 1-3/4, 3/8 gap")
    d.tag(18, 30, 60, 20, "2", "Channel joists at 12, open down")
    d.tag(1.5, 30, 60, 32, "3", "HSS 3x3 perimeter, 1 x 1/8 nailer")
    d.tag(LO - 1.5, LL - 1.5, 60, 44, "4", "Landing posts on piers")
    d.tag(LO + 0.6, LL + 8, 60, 56, "5", "Guard: outboard edge and return")
    d.tag(24, LL + 20, 60, 68, "6", "Mono stringer on centreline")
    d.text(-3.5, 45, "house", "sm", "middle")
    d.text(24, LL + 4 * TT + 5, "descends", "sm", "middle")
    return d.svg("Landing and stair plan")


# ================================================================= L-102
def section():
    d = D(-14, 108, -14, 84, 5.4, "ls")
    d.line(-14, 0, 70, 0, "grade")
    d.rect(-10, 20, -0.5, 60, "void ob")
    d.text(-5.2, 56, "house", "sm", "middle")
    d.rect(-2.5, 36, -0.5, 44, "wdplan ob")
    y0 = TOP - SLAT_T - FR
    d.rect(0, y0, FR, y0 + FR, "steel ob")
    d.rect(LO - FR, y0, LO, y0 + FR, "steel ob")
    for o in JOISTS:
        d.rect(o - 1.5, y0 + 1, o + 1.5, y0 + FR, "steel ob")
    d.rect(0, TOP - SLAT_T, LO, TOP, "WD ob")
    for y in (y0 + 0.8, y0 + 2.2):
        d.line(-4, y, 1.5, y, "lag")
    d.pline([(-0.5, TOP + 3), (-0.5, TOP + 0.4), (3.4, TOP + 0.4), (3.4, TOP - 0.6)], "flash")
    d.rect(LO - 3, 0, LO, y0, "steel ob")
    d.rect(LO - 6, -12, LO + 3, 0, "CC ob")
    d.rect(LO - 3, TOP, LO, TOP + 34, "steel ob")
    d.rect(LO - 3, TOP + 34, LO, TOP + 36, "steel ob")
    d.dim((LO + 4, 0), (LO + 4, TOP), -2, fr(TOP) + " to grade")
    d.dim((LO + 4, TOP), (LO + 4, TOP + 36), -2, "36 guard")
    d.dim((0, TOP), (LO, TOP), 2, fr(LO))
    d.tag(0.5, y0 + 1.5, -12, 70, "1", "Ledger HSS 3x3x1/4, stood off 1/2 on SS washers", side="r")
    d.tag(-1, y0 + 2.2, -12, 64, "2", "1/2 structural lags at 16 staggered into the TJI rim", side="r")
    d.tag(1.5, TOP + 0.4, -12, 76, "3", "Metal cap flashing over the ledger, butyl behind", side="r")
    d.tag(30, y0 + 2, 54, 22, "4", "Channel joist, slats screwed from below")
    d.tag(LO - 1.5, 20, 54, 12, "5", "Landing post, bolted to the rim")
    d.tag(LO - 1.5, -6, 54, 4, "6", "Pier")
    return d.svg("Section out from the house")


# ================================================================= L-103
def stair():
    d = D(-6, 150, -6, 86, 5.0, "st")
    d.pline([(-6, 0), (LL, 0), (LL + 4 * TT + 2, TOP - 29), (104, TOP - 29)], "grade")
    d.rect(-6, -6, 0, 70, "CC ob")
    d.rect(0, TOP - SLAT_T, LL, TOP, "WD ob")
    d.rect(0, TOP - SLAT_T - FR, LL, TOP - SLAT_T, "steel ob")
    for n in range(1, 5):
        a = LL + TT * (n - 1)
        top = TOP - RR * n
        d.rect(a, top - 1.75, a + TT, top, "WD ob")
        d.rect(a, top - TREAD, a + TT, top - 1.75, "steel ob")
    foot = LL + 4 * TT
    d.poly([(LL - 1, TOP - SLAT_T - FR), (LL + 2, TOP - SLAT_T - FR), (foot - 2, TOP - 29 + 0.5), (foot - 8, TOP - 29 + 0.5)], "steel ob")
    d.rect(foot - 10, TOP - 29, foot - 1, TOP - 29 + 0.5, "steel ob")
    d.rect(foot - 11, TOP - 29 - 10, foot, TOP - 29, "CC ob")
    for l in (1.5, LL - 1.5):
        d.rect(l - 1.5, 0, l + 1.5, TOP - SLAT_T - FR, "steel ob")
        d.rect(l - 4, -6, l + 4, 0, "CC ob")
    for l in (1.5, 22.5, LL - 1.5):
        d.rect(l - 1.5, TOP - SLAT_T, l + 1.5, TOP + 34, "steel ob")
    tp = LL + TT / 2
    d.rect(tp - 1.5, TOP - RR - 1.75, tp + 1.5, TOP - RR + 36 - 2, "steel ob")
    d.rect(-1, TOP + 34, LL, TOP + 36, "coral ob")
    d.pline([(LL, TOP + 36), (tp + 1.5, TOP - RR + 36)], "rail2")
    d.pline([(LL, TOP + 34 - 2), (foot, TOP - 29 + 34 + 5.8)], "hrail")
    d.dim((foot + 4, TOP - 29), (foot + 4, TOP), -2, "29 total rise")
    d.dim((LL, TOP + 44), (foot, TOP + 44), 0, "4 at 11-1/4 = 45")
    d.dim((0, TOP + 44), (LL, TOP + 44), 0, fr(LL) + " landing")
    d.tag(LL + 3 * TT, TOP - 3 * RR, 100, 60, "1", "5 risers at 5-13/16, tread frame as S-103")
    d.tag(foot - 12, TOP - 20, 100, 52, "2", "Stringer: stair-end beam to a pier")
    d.tag(tp, TOP - RR + 20, 100, 72, "3", "Guard post on tread 1 only")
    d.tag(foot - 10, TOP + 2, 100, 44, "4", "Handrail on the house wall, 34 to 38")
    return d.svg("Elevation along the house")


sched = """
<div class="scroll"><table class="grid">
<thead><tr><th>Mark</th><th>Item</th><th>Spec</th></tr></thead>
<tbody>
<tr><td>LF-1</td><td>Ledger</td><td>HSS 3x3x1/4 x 45, stood off 1/2 on stainless washers, 1/2 structural lags at 16 staggered into the TJI rim, butyl behind, metal cap flashing over</td></tr>
<tr><td>LF-2</td><td>Rim beam</td><td>HSS 3x3x1/4 x 45, through-bolted to both posts, carries the guard</td></tr>
<tr><td>LF-3</td><td>End beams</td><td>HSS 3x3x1/4 x 48, ledger to post; the landing-end beam carries the guard return, the stair-end beam carries the stringer</td></tr>
<tr><td>LF-4</td><td>Joists</td><td>Channel 3 x 2 x 1/8, open side down, at 6, 18, 30 and 42 in out from the house, welded between the end beams, tapped for #10 slat screws</td></tr>
<tr><td>LF-5</td><td>Nailer bar</td><td>1 x 1/8 flat bar welded to the inner face of the ledger, rim and both end beams, flush with the top, tapped for the perimeter slat screws</td></tr>
<tr><td>LF-6</td><td>Posts</td><td>Mild steel, two, at the outboard corners, base plate on a pier; size to be confirmed, 3x3 minimum</td></tr>
<tr><td>LW-1</td><td>Slats</td><td>Thermally modified ash, 2 x 1-3/4 x 48, ripped from 8/4, 19 pieces, 3/8 gaps, screwed from below, oiled to match the treads</td></tr>
<tr><td>LS-1</td><td>Stair</td><td>5 risers at 5-13/16, 4 treads at 11-1/4, 48 wide, same tread frame, ash and collar connection as S-103; mono stringer bolted to the stair-end beam</td></tr>
<tr><td>LG-1</td><td>Guard</td><td>Outboard edge and landing-end return, posts through-bolted to the rim and end beams; one post on tread 1; handrail wall-mounted on the house side. Cables tensioned to about 100 lb each, half the main runs, since the spans are about half as long.</td></tr>
</tbody></table></div>
<p><b>Everything welded is welded before coating.</b> The frame is one weldment that bolts to the ledger and drops onto the two posts. Screws into steel are machine screws into tapped holes, so slats come off individually later.</p>
<p><b>Held for the field survey:</b> post size and pier detail, finish grade at the stair foot, and whether the landing frame fits past the door as one piece.</p>
"""

html_sheets = [
    sheet("L-101", "Master bath landing, plan", fig(plan(), "Landing off the door, stair descending along the house.", "big")),
    sheet("L-102", "Landing section", fig(section(), "Section out from the house through the landing.", "big")),
    sheet("L-103", "Landing stair elevation", fig(stair(), "Elevation along the house. Guard required on the landing and tread 1 only.", "big")),
    sheet("L-601", "Landing schedule", sched),
]
open("part_L.html", "w").write("".join(html_sheets))
json.dump(SHEETS, open("part_L.json", "w"))
print("ok")


def frame_plan():
    d = D(-8, 96, -8, 56, 7, "lf")
    d.rect(0, 0, 3, LL, "steel ob")
    d.rect(LO - 3, 0, LO, LL, "steel ob")
    d.rect(3, 0, LO - 3, 3, "steel ob")
    d.rect(3, LL - 3, LO - 3, LL, "steel ob")
    for o in JOISTS:
        d.rect(o - 1.5, 3, o + 1.5, LL - 3, "steel ob")
    for a, b in ((3, 3.125), (LO - 3.125, LO - 3)):
        d.rect(a, 3, b, LL - 3, "coral ob")
    for l in range(8, 44, 16):
        d.circle(1.5, l, 0.3, "void ob")
    for l in (1.5, LL - 1.5):
        d.circle(LO - 1.5, l, 0.25, "void ob")
    d.dim((0, LL), (LO, LL), 2.4, '48 out from the house')
    d.dim((LO, 0), (LO, LL), -2.4, '45 along the house')
    d.dim((0, -1), (6, -1), -1.4, '6')
    d.dim((6, -1), (18, -1), -1.4, '12')
    d.dim((18, -1), (30, -1), -1.4, '12')
    d.dim((30, -1), (42, -1), -1.4, '12')
    d.dim((-1, 8), (-1, 24), 1.4, '16 lags')
    d.text(-4, LL / 2, "house", "sm", "middle")
    d.tag(1.5, 30, 56, 44, "1", "Ledger HSS 3x3x1/4 x 45, 9/16 holes at 16 staggered")
    d.tag(LO - 1.5, 20, 56, 36, "2", "Rim beam HSS 3x3x1/4 x 45, post bolts at each end")
    d.tag(24, 1.5, 56, 28, "3", "End beams HSS 3x3x1/4 x 42, between ledger and rim")
    d.tag(18, 30, 56, 20, "4", "Channel 3 x 2 x 1/8 x 39, open down, tapped for slats")
    d.tag(LO - 3.06, 10, 56, 12, "5", "1 x 1/8 nailer bar, inner face, flush with the top")
    d.tag(LO - 1.5, 1.5, 56, 4, "6", "Post bolt holes; guard posts bolt on the same beams")
    return d.svg("Landing frame weldment, plan from above")


cut = """
<div class="scroll"><table class="grid">
<thead><tr><th>Mark</th><th>Qty</th><th>Section</th><th>Length</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>LF-1</td><td>1</td><td>HSS 3x3x1/4</td><td>45</td><td>Ledger. (6) 9/16 holes at 16 staggered 1 in above and below centre</td></tr>
<tr><td>LF-2</td><td>1</td><td>HSS 3x3x1/4</td><td>45</td><td>Rim beam. Post and guard bolt holes drilled at dry fit</td></tr>
<tr><td>LF-3</td><td>2</td><td>HSS 3x3x1/4</td><td>42</td><td>End beams, square cut, between ledger and rim</td></tr>
<tr><td>LF-4</td><td>4</td><td>Channel 3 x 2 x 1/8</td><td>39</td><td>Joists, open side down, welded between end beams; #10-24 taps for slats</td></tr>
<tr><td>LF-5</td><td>4</td><td>Flat bar 1 x 1/8</td><td>to suit</td><td>Nailer, inner face of each perimeter member, flush with the top; tapped</td></tr>
<tr><td>LF-6</td><td>2</td><td>TBD, 3x3 minimum</td><td>to pier</td><td>Landing posts, base plate on pier, through-bolted to the rim beam</td></tr>
</tbody></table></div>
<p>One weldment, about 110 lb before posts. Tack all four perimeter corners, check both diagonals, then weld out. Vent every closed member for the coating oven and drain the low corners.</p>
"""
extra = sheet("L-104", "Landing frame fabrication", fig(frame_plan(), "Everything welded here is welded before coating.", "big") + "<h3>Cut list</h3>" + cut)
open("part_L.html", "a").write(extra)
json.dump(SHEETS, open("part_L.json", "w"))


