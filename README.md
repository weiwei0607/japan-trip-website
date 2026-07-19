# 日本神社之旅 2026

個人日本旅遊行程網站(PWA),單頁應用,收錄多日行程規劃、神社御朱印資訊、藥妝與伴手禮購物指南、交通 Pass 提醒等內容,支援離線瀏覽。

## Demo

https://weiwei0607.github.io/japan-trip-website/

## 功能

- 多日行程卡片(每日景點、交通、餐廳、時間軸)
- 神社 / 御朱印收集清單
- 藥妝、伴手禮購物指南(含優惠券連結與已購勾選)
- 關西 Pass、巴士票、行李等重要提醒
- Service Worker 離線快取,可安裝為 PWA
- 行程資料加密儲存(CryptoJS)

## 技術

- 純前端單頁應用:單一 `index.html`(HTML + CSS + Vanilla JS),無框架、無建置步驟
- [CryptoJS](https://github.com/brix/crypto-js)(CDN)用於行程資料加解密
- Service Worker(`sw.js`)+ `manifest.json` 提供 PWA / 離線支援
- 部署:GitHub Pages

## 本地執行

不需建置,直接用任一靜態伺服器開啟即可:

```bash
npx serve .
# 或
python3 -m http.server 8000
```

## 開發工具腳本(未追蹤)

根目錄下的 `fix_*.js`、`super_patch.js` 等為一次性行程資料批次修改腳本;`sync_to_notion.py`、`update_itinerary.py` 用於與 Notion 同步(需自備 `notion_config.py`,內含 `TOKEN`,已列入 .gitignore)。
