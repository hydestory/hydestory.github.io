# Hydestory

Roger 的個人網站，使用靜態 HTML、CSS 與 JavaScript，可直接部署至 GitHub Pages。

## 本機預覽

在專案目錄執行 `python -m http.server 8765 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8765/`。

## 驗證

```sh
node --test tests/*.test.cjs
python tests/test_links.py
node --check static/js/site.js
node --check static/js/weather-integration.js
git diff --check
```

測試使用 Node.js 內建測試工具與 Python 標準函式庫，不需安裝測試套件。

## 維護

- `index.html`：首頁文案、專案入口與聯絡表單。
- `static/css/site.css`：首頁樣式、共用導覽與手機斷點。
- `static/js/site.js`：手機選單、聯絡表單；EmailJS SDK 在使用表單時才載入。
- `static/js/weather-integration.js`：天氣與應用程式使用紀錄。讀取失敗時不顯示模擬資料。
- `src/text/usage_log.json`：已保存的應用程式使用秒數，沒有日期欄位，不能解讀為今日即時統計。
- `src/50lan.html` 與 `src/data/drinks.json`：飲品試算工具及配方資料。
- `src/image/roger-portrait.webp`：首頁輕量圖片。原始 JPEG 保留在同資料夾。

聯絡表單沿用原有 EmailJS 設定。郵件服務的網域許可與額度由 EmailJS 管理；本機測試不會寄出真實郵件。前端只有收到服務成功回應才顯示寄送成功，失敗或逾時會保留內容。

課堂筆記、每日紀錄、股票紀錄沿用既有內容與網址。每日紀錄沒有對應文章的項目改為連結至原始完整統計圖。課程入口改為實際存在的筆記／測驗清單；深層筆記與股票文章採用共用閱讀版型。筆記附文章目錄及返回課程連結，雲端小考可直接開啟 PDF。

## 發布

GitHub Pages 使用 `main` 分支的根目錄發布。更新前先抓取遠端最新內容、整合本機修改並完成驗證，再推送至 `main`。

- 一般首頁：https://hydestory.github.io/
- 獨立翻書預覽：https://hydestory.github.io/book-prototype.html

`book-prototype.html` 使用原生 HTML、CSS 3D 與 JavaScript 製作，支援捲動翻頁及一般閱讀模式，與首頁分開保留。

## 本輪更新

- 首頁加入萬問島與諾斯菲作品卡，使用文字封面與外部入口；外部存取限制下未加入產品截圖或未經確認的功能介紹。
- 四門課程改用可直接開啟的內容連結，文章採用一致字體、閱讀寬度與手機版型。
- 保留未發布的 PDF 範例頁，不列入課程清單。
