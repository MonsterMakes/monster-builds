import asyncio, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else 'shop-guide-upper-stairs'
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto(f"file://out/{OUT}.html")
        await pg.wait_for_timeout(700)
        await pg.emulate_media(media="print")
        await pg.pdf(path=f"out/{OUT}.pdf", format="Letter", print_background=True,
                     margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"})
        await b.close()
asyncio.run(main())


