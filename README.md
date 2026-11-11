# CCL 產業新聞

自動收集 CCL（銅箔基板）相關新聞並分類的網站。來源：DIGITIMES、優分析、財訊。

- 只收公開的標題、日期、連結與網站提供的摘要；全文請點連結到原網站閱讀。
- 遵守各網站 robots.txt，每次請求間隔 3 秒。

## 使用方式

**在自己電腦執行**：雙擊 `run.command`（Mac），或執行
```
pip install -r requirements.txt
python3 scraper.py
open web/index.html
```

**GitHub 自動更新**：`.github/workflows/update.yml` 每天台灣時間 7:00 執行爬蟲並更新 GitHub Pages。
需在 repo 的 Settings → Pages 把 Source 設為「GitHub Actions」。

## 調整分類

公司、主題、關鍵字、新聞來源都在 `config.py`，改完重新執行即可（舊資料會依新設定重新分類）。
