#!/bin/bash
# 雙擊執行：抓取最新 CCL 新聞並打開網頁
cd "$(dirname "$0")"
python3 -m pip install -q -r requirements.txt 2>/dev/null || python3 -m pip install -q --user -r requirements.txt
python3 scraper.py
open web/index.html
