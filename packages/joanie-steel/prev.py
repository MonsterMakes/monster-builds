g = {}
src = open('gen3.py').read().replace(
 'open("out/mono-stringer-drawings.html", "w").write(html)','pass').replace(
 'open("part_S.html", "w").write("".join(html_sheets))','pass')
exec(src, g)
exec(open('draw_parts.py').read())
css = open('css.txt').read() + """
.isT{fill:var(--steel)}.isS{fill:color-mix(in srgb,var(--steel) 72%,var(--ink) 28%)}.isF{fill:color-mix(in srgb,var(--steel) 86%,var(--ink) 14%)}
.icT{fill:var(--conc)}.icS{fill:color-mix(in srgb,var(--conc) 75%,var(--ink) 25%)}.icF{fill:color-mix(in srgb,var(--conc) 88%,var(--ink) 12%)}
.iwT{fill:var(--steeld)}.iwS{fill:color-mix(in srgb,var(--steeld) 70%,var(--ink) 30%)}
.inT{fill:var(--steeld)}.inS{fill:color-mix(in srgb,var(--steeld) 65%,var(--ink) 35%)}
.io{stroke:var(--ink);stroke-width:1;stroke-linejoin:round}
body{background:var(--paper);padding:20px}
"""
open('t.html','w').write('<style>' + css + '</style>' + wall_iso())
print("ok")

