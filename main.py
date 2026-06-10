from fastapi import FastAPI
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

app = FastAPI()

async def solve_lootlabs(page, url):
    await page.goto(url)
    return page.url

async def solve_linkvertise(page, url):
    await page.goto(url)
    return page.url

@app.get("/bypass")
async def bypass(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        
        if "lootlabs" in url:
            final_url = await solve_lootlabs(page, url)
        elif "linkvertise" in url:
            final_url = await solve_linkvertise(page, url)
        else:
            await page.goto(url)
            final_url = page.url
            
        await browser.close()
        return {"final_url": final_url}
