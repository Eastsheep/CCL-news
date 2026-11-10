# -*- coding: utf-8 -*-
"""CCL 新聞爬蟲設定：來源網址、分類關鍵字。要新增公司或主題，改這個檔案即可。"""

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 CCLNewsBot/0.1 (internal research)"
REQUEST_DELAY_SEC = 3.0      # 每次請求間隔，避免造成對方負擔
MAX_ARTICLES_PER_RUN = 60    # 每次最多抓幾篇文章內頁
TIMEOUT_SEC = 20

# ── 新聞來源 ────────────────────────────────────────────
# 每個來源：
#   name          顯示名稱
#   domain        只收這個網域的連結
#   list_pages    列表頁（從這些頁面找文章連結）
#   search_pages  搜尋/標籤頁樣板，{q} 會被替換成 search_terms 裡的關鍵字
#   article_re    文章網址的正規式，第一個群組是文章編號
#   canonical     文章標準網址樣板，{id} 為文章編號
#   seeds         已知相關文章（第一次執行當作種子）
SOURCES = [
    {
        "name": "DIGITIMES",
        "domain": "digitimes.com.tw",
        "list_pages": ["https://www.digitimes.com.tw/"],
        "search_pages": ["https://www.digitimes.com.tw/tech/searchdomain/srchlst_main.asp?query={q}"],
        "search_terms": ["銅箔基板", "CCL", "台光電", "台燿", "聯茂", "玻纖布", "HVLP", "低介電"],
        "article_re": r"shwnws\.asp\?[^\"'#\s]*id=([0-9A-Za-z_]+)",
        "canonical": "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id={id}",
        "seeds": [
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000763513_DDR6UL740IO6Q64AMT3D0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000756720_ENZ821DU1H2TDR1629ECE",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000752161_RDH29R6Z5HB6AU2JTPU13",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000751041_U6W1HOON3PS2D02HCM8CL",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000745128_RMT2562M1RL9TX90LGEMM",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000716730_7H18LZSN2KWO1D1U2NHWR",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000717278_GI53C07661XTHW95VKC55",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000705600_DI77U0QMLOJ9Q818AQEK2",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000697434_7L653LSX26OWLC5SWXTHV",
        ],
    },
    {
        "name": "優分析",
        "domain": "uanalyze.com.tw",
        "list_pages": [],
        # 優分析有標籤頁（股票代號或主題）與站內搜尋；robots.txt 全站允許
        "search_pages": [
            "https://uanalyze.com.tw/index.php/articles?tag={q}",
            "https://uanalyze.com.tw/articles/search/{q}",
        ],
        "search_terms": ["CCL", "M9", "2383", "6274", "6213", "台光電", "台燿", "聯茂", "玻纖布", "銅箔基板"],
        "article_re": r"uanalyze\.com\.tw/(?:index\.php/)?articles/(\d{6,})",
        "canonical": "https://uanalyze.com.tw/articles/{id}",
        "seeds": [],
    },
]

# 判斷「是否與 CCL 相關」：標題或摘要命中任一個才收錄
RELEVANCE_TERMS = [
    "銅箔基板", "CCL", "基板材料", "高頻高速材料", "玻纖布", "玻纖紗", "Low-Dk", "Low Dk", "低介電",
    "HVLP", "石英布", "Q布", "台光電", "台燿", "聯茂", "生益", "斗山", "建滔積層板", "騰輝",
    "Megtron", r"\bM ?(7|8|9|10)\b", "PTFE", "碳氫樹脂", "PPE樹脂", "含浸",
]

# 公司分類：顯示名稱 -> 關鍵字（命中任一即標記）
COMPANIES = {
    "台光電": ["台光電", r"\bEMC\b", "2383"],
    "台燿": ["台燿", r"\bTUC\b", "6274"],
    "聯茂": ["聯茂", "ITEQ", "6213"],
    "南亞": ["南亞", "1303"],
    "騰輝": ["騰輝"],
    "生益": ["生益"],
    "斗山": ["斗山", "Doosan"],
    "建滔": ["建滔"],
    "松下": ["Panasonic", "松下", "Megtron"],
    "玻纖布廠": ["台玻", "富喬", "日東紡", "Nittobo", "建榮", "德宏"],
    "銅箔廠": ["金居", "長春", "三井金屬", "古河", "福田金屬"],
}
# 「南亞」容易誤判成南亞科(DRAM)，含這些字的不標記為南亞
COMPANY_EXCLUDES = {"南亞": ["南亞科", "南亞電路板", "南電"]}

TOPICS = {
    "M7/M8/M9 等級": [r"\bM ?(6|7|8|9|10)\b", "高階CCL", "高階材料"],
    "玻纖布 / Low-Dk": ["玻纖布", "玻纖紗", "Low-Dk", "Low Dk", "低介電", "石英布", "Q布", "LDK"],
    "銅箔 / HVLP": ["HVLP", "銅箔", "RTF", "VLP"],
    "樹脂 / 添加劑": ["樹脂", "PPE", "PPO", "碳氫", "BMI", "PTFE", "添加劑"],
    "漲價 / 報價": ["漲價", "漲幅", "報價", "調漲", "價格", "漲勢"],
    "擴產 / 產能": ["擴產", "產能", "新廠", "稼動率", "滿載", "含浸機", "上膠機"],
    "AI 伺服器 / 交換器": ["AI伺服器", "AI 伺服器", "GB200", "GB300", "Rubin", "ASIC", "交換器", "NVIDIA", "輝達"],
    "CPO / 載板": ["CPO", "共同封裝", "載板", "ABF", r"\bBT\b"],
    "營收 / 財報": ["營收", "財報", "EPS", "毛利率", "法說", "獲利"],
}
