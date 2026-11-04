import json
css = open('css.txt').read() + """
.coral{fill:var(--steeld)}
.hidp{stroke:var(--mark);stroke-width:1.2;stroke-dasharray:5 3;fill:none}
.redc{fill:none;stroke:var(--hold);stroke-width:1.6}
.cable{stroke:#1D9E75;stroke-width:1.1}
.guard{stroke:#1D9E75;stroke-width:3}
.flash{stroke:var(--mark);stroke-width:1.4;fill:none}
.rail2{stroke:var(--steeld);stroke-width:3;fill:none}
.hrail{stroke:var(--mark);stroke-width:2;stroke-dasharray:8 4;fill:none}
.grid td[rowspan]{font-weight:600}
.survey td:first-child{font-weight:400;color:var(--ink)}
.survey td[rowspan]{font-weight:600;color:var(--mark)}
nav h4{margin:10px 0 2px;font:600 11px/1.2 'Archivo Narrow',sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
"""
parts = [("S", "Stairs, both main flights"), ("R", "Rail, guard, fence and gates"), ("L", "Master bath landing and stair")]
body, nav = "", ""
for key, label in parts:
    body += open(f'part_{key}.html').read()
    nav += f"<h4>{label}</h4>" + "".join(f'<a href="#s{n}"><b>{n}</b>{t}</a>' for n, t in json.load(open(f'part_{key}.json')))
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1, viewport-fit=cover">
<title>Stairs, rail and landing — drawing set, rev Q, 23 Sep 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Narrow:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header class="cover"><div><h1>Stairs, rail<br>and landing</h1>
<p><b>Rev Q, issued 23 September 2026.</b> S series: the two main flights on mono stringers with ash treads on steel frames. R series: the cable rail, guard, fence and gates. L series: the master bath landing and its stair. One order, one coating batch.</p></div>
<div class="stamp">PRELIMINARY<br>not for construction<br>engineer review required</div></header>
<nav aria-label="Sheets">{nav}</nav>
<main>{body}</main></body></html>"""
open('out/combined-drawings.html', 'w').write(html)
ids = []
for key, _ in parts:
    ids += [n for n, _ in json.load(open(f'part_{key}.json'))]
json.dump(ids, open('all_ids.json', 'w'))
print(len(ids), "sheets")


