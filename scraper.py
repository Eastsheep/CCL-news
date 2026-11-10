# -*- coding: utf-8 -*-
"""CCL 新聞爬蟲（DIGITIMES、優分析）

只抓公開可見的內容：標題、日期、連結、網站提供的摘要（meta description / 導言）。
不抓付費全文，遵守 robots.txt，每次請求間隔 REQUEST_DELAY_SEC 秒。

用法：
    python3 scraper.py              # 抓新聞，更新 data/news.json 與 web/news.js
    python3 scraper.py --debug URL  # 印出某頁解析結果，方便調整
"""
import json
import re
import sys
import time
import urllib.robotparser
from datetime import datetime, timedelta, timezone

TW = timezone(timedelta(hours=8))
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, quote

import requests
from bs4 import BeautifulSoup

import config

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "news.json"
JS_FILE = ROOT / "web" / "news.js"

for _s in config.SOURCES:
    _s["_re"] = re.compile(_s["article_re"], re.I)
DATE_RES = [
    re.compile(r"(20\d{2})[/\-.年](\d{1,2})[/\-.月](\d{1,2})"),
]

session = requests.Session()
session.headers.update({
    "User-Agent": config.USER_AGENT,
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.6",
})
_robots = {}
_last_request = 0.0


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def allowed(url):
    """依 robots.txt 判斷能否抓取；robots.txt 讀不到時保守處理為允許但記錄。"""
    host = urlparse(url).scheme + "://" + urlparse(url).netloc
    if host not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = session.get(host + "/robots.txt", timeout=config.TIMEOUT_SEC)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            log(f"[robots] {host}/robots.txt -> HTTP {r.status_code}")
        except Exception as e:
            log(f"[robots] 讀取失敗 {e}")
            rp.parse([])
        _robots[host] = rp
    return _robots[host].can_fetch(config.USER_AGENT, url)


def fetch(url):
    global _last_request
    if not allowed(url):
        log(f"[skip] robots.txt 不允許：{url}")
        return None
    wait = config.REQUEST_DELAY_SEC - (time.time() - _last_request)
    if wait > 0:
        time.sleep(wait)
    _last_request = time.time()
    try:
        r = session.get(url, timeout=config.TIMEOUT_SEC)
    except Exception as e:
        log(f"[error] {url}: {e}")
        return None
    if r.status_code != 200:
        log(f"[error] {url}: HTTP {r.status_code}")
        return None
    if not r.encoding or r.encoding.lower() in ("iso-8859-1", "ascii"):
        r.encoding = r.apparent_encoding
    return r.text


def source_of(url):
    host = urlparse(url).netloc
    for src in config.SOURCES:
        if host.endswith(src["domain"]):
            return src
    return None


def article_id(url):
    """回傳 (來源, 文章編號)；不是文章網址就回傳 (None, None)。"""
    src = source_of(url)
    if src:
        m = src["_re"].search(url)
        if m:
            return src, m.group(1)
    return None, None


def item_key(url):
    src, aid = article_id(url)
    return f'{src["domain"]}:{aid}' if aid else None


def canonical(url):
    src, aid = article_id(url)
    return src["canonical"].format(id=aid) if aid else url


def _compile(term):
    if "\\" in term or "(" in term:
        return re.compile(term, re.I | re.A)
    return re.compile(re.escape(term), re.I)


def matches(text, terms):
    return any(_compile(t).search(text) for t in terms)


def classify(text):
    companies = []
    for name, terms in config.COMPANIES.items():
        if matches(text, terms):
            excl = config.COMPANY_EXCLUDES.get(name, [])
            # 若只因排除字（如「南亞科」）而命中，就不算
            cleaned = text
            for e in excl:
                cleaned = cleaned.replace(e, "")
            if matches(cleaned, terms):
                companies.append(name)
    topics = [name for name, terms in config.TOPICS.items() if matches(text, terms)]
    return companies, topics


def find_article_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    found = {}
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"])
        if article_id(href)[1]:
            url = canonical(href)
            text = a.get_text(" ", strip=True)
            if url not in found or len(text) > len(found[url]):
                found[url] = text
    return found


def _meta(soup, *names):
    for n in names:
        tag = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n}) \
            or soup.find("meta", attrs={"itemprop": n})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def parse_date(soup, html):
    raw = _meta(soup, "article:published_time", "pubdate", "publishdate", "date", "datePublished")
    for src in ([raw] if raw else []) + [t.get_text(" ", strip=True) for t in soup.find_all(["time", "span", "div"], class_=re.compile("date|time", re.I))][:5] + [html]:
        for rx in DATE_RES:
            m = rx.search(src or "")
            if m:
                y, mo, d = map(int, m.groups())
                try:
                    return datetime(y, mo, d).strftime("%Y-%m-%d")
                except ValueError:
                    continue
    return ""


def parse_article(url, html):
    soup = BeautifulSoup(html, "html.parser")
    title = _meta(soup, "og:title") or (soup.title.get_text(strip=True) if soup.title else "")
    title = re.sub(r"\s*[|｜\-–]\s*(DIGITIMES|優分析|Uanalyze|UAnalyze).*$", "", title, flags=re.I).strip()
    summary = _meta(soup, "og:description", "description")
    if len(summary) < 30:
        # 退而求其次：取內文第一段（通常是公開導言）
        for p in soup.select("article p, .main_p p, #newsText p, p"):
            t = p.get_text(" ", strip=True)
            if len(t) > 40:
                summary = t
                break
    summary = re.sub(r"\s+", " ", summary)[:300]
    if re.search(r"(會員登入|忘記密碼|帳號啟用|記住帳號)", summary):
        summary = ""   # 抓到的是登入框文字，不是摘要
    paywall = not summary
    return {
        "id": item_key(url),
        "title": title,
        "date": parse_date(soup, html),
        "url": url,
        "summary": summary,
        "source": source_of(url)["name"],
        "author": _meta(soup, "author", "article:author"),
        "paywall_hint": paywall,
    }


def load_existing():
    if DATA_FILE.exists():
        try:
            return {n["id"]: n for n in json.loads(DATA_FILE.read_text("utf-8"))["items"]}
        except Exception:
            pass
    return {}


def save(items):
    items = sorted(items.values(), key=lambda n: (n.get("date") or "", n["id"]), reverse=True)
    payload = {
        "updated_at": datetime.now(TW).strftime("%Y-%m-%d %H:%M"),
        "sources": [x["name"] for x in config.SOURCES],
        "companies": list(config.COMPANIES.keys()),
        "topics": list(config.TOPICS.keys()),
        "items": items,
    }
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), "utf-8")
    (ROOT / "web" / "news.json").write_text(json.dumps(payload, ensure_ascii=False), "utf-8")
    JS_FILE.write_text("window.NEWS_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n", "utf-8")
    log(f"[done] 共 {len(items)} 則，寫入 {DATA_FILE.name} 與 web/{JS_FILE.name}")


def run():
    existing = load_existing()
    candidates = {}
    for src in config.SOURCES:
        candidates.update({canonical(u): "" for u in src.get("seeds", [])})
        pages = [(p, False) for p in src.get("list_pages", [])]
        pages += [(t.format(q=quote(q)), True) for t in src.get("search_pages", []) for q in src.get("search_terms", [])]
        for page, _ in pages:
            html = fetch(page)
            if not html:
                continue
            links = find_article_links(html, page)
            # 搜尋/標籤頁的側欄常混有熱門文章，所以一律再用標題關鍵字過濾
            kept = {u: t for u, t in links.items() if matches(t, config.RELEVANCE_TERMS)}
            log(f"[list] {src['name']} {page} -> {len(links)} 篇連結，相關 {len(kept)}")
            candidates.update(kept)

    new = [u for u in candidates if item_key(u) and item_key(u) not in existing]
    log(f"[info] 候選 {len(candidates)} 篇，新文章 {len(new)} 篇（本次最多抓 {config.MAX_ARTICLES_PER_RUN}）")
    for url in new[: config.MAX_ARTICLES_PER_RUN]:
        html = fetch(url)
        if not html:
            continue
        item = parse_article(url, html)
        text = item["title"] + " " + item["summary"]
        if not item["title"] or not matches(text, config.RELEVANCE_TERMS):
            log(f"[drop] 不相關：{item['title'][:40]}")
            continue
        item["companies"], item["topics"] = classify(text)
        item["fetched_at"] = datetime.now(TW).strftime("%Y-%m-%d %H:%M")
        existing[item["id"]] = item
        log(f"[ok] {item['date']} {item['title'][:50]}")

    # 同來源同標題只留一則（同一篇文章可能有多個網址）
    seen = {}
    for key, item in sorted(existing.items(), key=lambda kv: kv[1].get("summary", "") == ""):
        sig = (item["source"], re.sub(r"\s+", "", item["title"]))
        if sig in seen:
            del existing[key]
        else:
            seen[sig] = key

    # 設定檔改過後，舊資料也重新分類
    for item in existing.values():
        item["companies"], item["topics"] = classify(item["title"] + " " + item["summary"])
    save(existing)


def debug(url):
    html = fetch(url)
    if not html:
        return
    if article_id(url)[1]:
        print(json.dumps(parse_article(canonical(url), html), ensure_ascii=False, indent=2))
    else:
        for u, t in find_article_links(html, url).items():
            print(("★ " if matches(t, config.RELEVANCE_TERMS) else "  ") + t[:60], u)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--debug":
        debug(sys.argv[2])
    else:
        run()
