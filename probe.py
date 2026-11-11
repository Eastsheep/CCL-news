import asyncio, re
from playwright.async_api import async_playwright
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/124.0 Safari/537.36 CCLNewsBot/0.1 (internal research)"
URLS=["https://www.wealth.com.tw/articles/8c734bf6-0b00-4e2b-a574-6c9c7084b43b",
      "https://www.wealth.com.tw/search?keyword=CCL",
      "https://www.wealth.com.tw/search?q=CCL",
      "https://www.wealth.com.tw/"]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(user_agent=UA)
        for u in URLS:
            apis=[]
            pg.on("request", lambda r: apis.append(r.url) if r.resource_type in ("xhr","fetch") else None)
            await pg.goto(u, wait_until="networkidle", timeout=45000); await pg.wait_for_timeout(2000)
            print("=====",u,"->",pg.url); print("TITLE",await pg.title())
            for m in await pg.query_selector_all("meta[property^='og:'],meta[name='description']"):
                print("META",await m.get_attribute("property") or await m.get_attribute("name"),(await m.get_attribute("content") or "")[:150])
            links=set(re.findall(r'/articles/[0-9a-f-]{36}',await pg.content())); print("LINKS",len(links))
            txt=await pg.inner_text("body"); print("DATES",re.findall(r'20\d\d[./-]\d\d?[./-]\d\d?',txt)[:5])
            print("TEXT",txt[:600].replace("\n"," | "))
            print("XHR",[a for a in apis][:15])
            await asyncio.sleep(3)
        await b.close()
asyncio.run(main())
