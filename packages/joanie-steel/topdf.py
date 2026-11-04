import asyncio, subprocess
from playwright.async_api import async_playwright
IDS = ["S-001","S-002","S-101","S-102","S-103","S-104","S-105","S-106","S-501","S-502","S-601"]
FILL2 = {"S-101","S-102","S-103","S-104"}
FILL = FILL2
PW, PH = 16.4*96, 10.4*96
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        files=[]
        for i, sid in enumerate(IDS):
            pg = await b.new_page(color_scheme="light", viewport={"width":1800,"height":1200})
            await pg.goto("file://out/mono-stringer-drawings.html")
            await pg.evaluate("""([sid, first, fill, PW]) => {
              document.querySelectorAll('.sheet').forEach(s => { if (s.id !== 's'+sid) s.remove(); });
              document.querySelector('nav').remove();
              if (!first) document.querySelector('.cover').remove();
              const st=document.createElement('style');
              st.textContent='body{margin:0;background:#f6f8f4} main{padding:6px 0 0!important;max-width:none!important} .cover{max-width:none!important;padding:0 0 10px!important} .big .scroll svg{min-width:0!important} .row{flex-wrap:nowrap!important;gap:32px;justify-content:space-around!important}' + (fill ? '.sheet figure svg{width:100%!important}' : '');
              document.head.appendChild(st);
              const w=document.createElement('div'); w.id='wrap';
              while (document.body.firstChild) w.appendChild(document.body.firstChild);
              document.body.appendChild(w);
              w.style.width = PW + 'px';
            }""", [sid, i == 0, sid in FILL, PW])
            h = await pg.evaluate("() => document.getElementById('wrap').getBoundingClientRect().height")
            z = min(1.0, PH / h) * 0.99
            for _ in range(8):
                hh = await pg.evaluate(f"() => {{ const w=document.getElementById('wrap'); w.style.zoom={z}; w.style.width='{(PW if sid in FILL else PW/z)}px'; return w.getBoundingClientRect().height; }}")
                if hh <= PH: break
                z *= PH / hh * 0.99
            f=f"p{i}.pdf"
            await pg.pdf(path=f, width="17in", height="11in", margin={"top":"0.3in","bottom":"0.3in","left":"0.3in","right":"0.3in"}, print_background=True, page_ranges="1")
            files.append(f); print(sid, h, round(z,3))
            await pg.close()
        await b.close()
    subprocess.run(["qpdf","--empty","--pages",*files,"--","out/mono-stringer-drawings.pdf"],check=True)
asyncio.run(main())


