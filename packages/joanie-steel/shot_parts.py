import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, dark in ((1200, False), (390, True)):
            pg = await b.new_page(viewport={"width": w, "height": 900}, color_scheme="dark" if dark else "light")
            await pg.goto("file://out/part-guide.html"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"pg_{w}.png", full_page=True)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            print(w, "scrollWidth", sw)
        await b.close()
asyncio.run(main())

