import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1240,"height":900})
        await pg.goto("file://out/combined-drawings.html")
        await pg.wait_for_timeout(700)
        for sid in sys.argv[1:]:
            el = await pg.query_selector("#s"+sid)
            await el.screenshot(path=f"c{sid}.png")
        await b.close()
asyncio.run(main())


