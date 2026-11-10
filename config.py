# -*- coding: utf-8 -*-
"""CCL 新聞爬蟲設定：來源網址、分類關鍵字。要新增公司或主題，改這個檔案即可。"""

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 CCLNewsBot/0.1 (internal research)"
REQUEST_DELAY_SEC = 3.0      # 每次請求間隔，避免造成對方負擔
MAX_ARTICLES_PER_RUN = 150   # 每次最多抓幾篇文章內頁
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
        # DIGITIMES 站內搜尋是 JavaScript 動態載入，全部新聞列表需要登入，所以只抓首頁與
        # 「半導體．零組件」頻道（CCL 新聞歸在這裡），每天累積；種子文章補歷史資料。
        "list_pages": [
            "https://www.digitimes.com.tw/",
            "https://www.digitimes.com.tw/tech/industries/?CnlID=1&cat=40",
        ],
        "search_pages": [],
        "search_terms": [],
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
            # 2026-11-10 以搜尋引擎補進的 DIGITIMES CCL 相關舊聞
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773908_D6ULZTKTL3R9JO9WDT988",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000765355_KKH4WBMP4B1MBQ6ASCHY8",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000763109_QAF04F681KN1858JWBXC7",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000746667_DXZ5QUX473M3AU6YLI4GC",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000760365_VI92I2FE7T6C8V4MBOO2L",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000765211_QXZ3V51Y0CT3VI2WEHEA5",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000756488_KKM389049Q90HT7M6GO19",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000759604_6M35J77F1LBEPI3GIZ2V4",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000750417_KNO5L2GN0XUAYR84728OU",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000772084_RJL190TW7AEL465BDCYP8",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000757595_CXY6I6NB81XKME6EUR6P4",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000754973_JAM8AWAK8TIY842X1CVN6",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000724748_SJ88Q1Q23BKM3C9GDWV25",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=729779",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000730563_Y1S6NZJU51B81U4SC71KC",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000723051_GYW1NRS84DSDS125NCLX3",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000619623_XD154U0431V0CV2Y6UM9V",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000570682_FNQ7PYMH7TUK2Z3QWCHGE",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000768964_VB78BC5C78XRKL3XPBZAA",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770776_RLJ6PSS68DFE705MPR0Q0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000772890_U1N7K75ULGAV0AL768GB8",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000754724_6Y46FPBD3ZJKPZ3PUQHIJ",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000766194_XG00AF4WLD2G3939Q1GUN",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000736032_ZX0L9M6U4C7FFU12W6GU0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000762236_1NU17FBN4OKIOZ5P4TSW0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000740014_D271GBT90JNDBG5RRBBUN",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000772178_DH30RV6M8QRJUC7CT68AF",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000588658_1UL7Q8GD4S7F219S0K35I",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=663572",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000754150_TPB2RTVP44DHB81EMFM84",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000587987_46I8WTAZ9DVTEG61I1I4O",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000759228_Z6319LZZ3RO8W57ERH9QY",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000589725_TP86G4Z53TXDRU4M2P9TF",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000731319_S0N2QPJE2NNU9U8V0NF3M",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000756638_R305ZIKO4UMESV7LJKBAL",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769066_S281S3MA5FTT0T7D59GEI",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000757992_Q3M8NDWFLXUS1F1OJAEM6",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000730729_S9O8TGVD1FUALSL2312JR",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000748672_7225UONM8FHXVQ1P1DVNE",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000758368_7H7263CB76C13C7JM3DN0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000765418_AVI5TYBZ0429S999X3HHW",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000764550_UZT62PND4V0OND1X0QYRV",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000768724_QTS6SP3O30GQCS39BVJBI",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000755705_Z2065I001VEKXO4L9629W",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000619612_KU650RQF2UQSME1U6EMZP",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000766642_J5O5AIPU5LNI2H1NSJ6F4",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000588179_BAO211SF69BFLZLPNOJV0",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000771369_O1Z4NP725XP5HXL25MDDM",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000760885_5DU9EIQJ70OF3X6MXWLG2",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000767006_MVKLIBZV146EWB50VK70D",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000747702_BCI83D0DLHM3PQ3FD1JLA",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000753028_67C168V51NDZF89N7SDU4",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000748027_VE519FG11OHQ398K0UDFE",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000757750_7NM643OM64BG4FLETN80V",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000710583_EHR6YY3H78VA8B42SUBMJ",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000670496_OXJ54TJ38M8OJV7SCXOM9",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000755006_X5SLGI0I1HWQ5M5SEFAFL",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000693743_MR28EDEO38205C4L5QLVF",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000738906_DFJ8F7WC1HTVCZ5YTK8QB",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000766875_8OO7RJI98UWTIW4KOPE29",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770180_04R0YCM29UA5PGL8AL7VV",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000731329_8MG2GKUE367XH78I3372S",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000738403_44Q5Z0YOLTRDVA4M88UC6",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000747485_PM73ZLYH9GPCFM4D5WT50",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773104_U9D0HLSU169UQL36R6WHG",
            "https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000755031_6CUL6W5Q4U40UP0ABKSGW",
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
