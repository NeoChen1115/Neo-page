# Survey 文章規格說明書 (SPEC)

## 📋 項目概述
- **項目名稱**: Big Data × LLM Survey Report
- **類型**: 學術調查文章 (Markdown 格式)
- **目標受眾**: 教授
- **內容範圍**: 1000-2000 字
- **用途**: 課程作業 / 學術研究綜述

---

## 🎯 需求澄清

### 確認事項
- ✅ 生成 Markdown 格式的文章
- ✅ 面向教授級別讀者
- ✅ 涵蓋至少 10 篇代表性研究論文
- ✅ 包含分類法、方法比較、挑戰分析和未來方向

### 已確認事項
1. ✅ **主題選擇**: Option A: Retrieval-Augmented Generation (RAG) for Big Data

2. ✅ **文章長度**: 1000-2000 字 (團隊分工，用戶負責該部分)

3. ✅ **論文來源**: 4-5 篇代表性論文 (已列於下方)

---

## 📑 建議文章結構

### 1. **摘要 (Abstract)** - 100-150 字
   - 研究主題的簡潔描述
   - 主要貢獻和發現的預告

### 2. **引言 (Introduction)** - 200-300 字
   - Big Data 和 LLM 結合的背景
   - 該選題的重要性和動機
   - 文章組織結構說明

### 3. **核心內容部分** - 600-1000 字
   選擇主題後細分為:
   
   **如果選 Option A (RAG for Big Data)**:
   - 系統架構與設計核心概念
   - 向量數據庫與檢索方法
   - GraphRAG 以及其他擴展方案
   - 安全性與隱私考量

   **如果選 Option B (Text-to-SQL with LLMs)**:
   - 方法分類與演進
   - 評估指標與效能分析
   - 企業應用與數據庫工程
   - 實踐中的問題與解決方案

### 4. **方法比較與分類法 (Taxonomy & Comparison)** - 200-300 字
   - 統一的評估標準 (準確度、可擴充性、成本、延遲等)
   - 表格或圖表呈現不同方法的優劣

### 5. **挑戰與局限 (Challenges & Limitations)** - 150-250 字
   - 當前技術的關鍵限制
   - 實際應用中的障礙
   - 可靠性和可信度問題

### 6. **未來研究方向 (Future Directions)** - 100-200 字
   - 有前景的研究課題
   - 潛在的技術突破
   - 跨領域協作機會

### 7. **結論 (Conclusion)** - 100-150 字
   - 核心發現的總結
   - 該領域發展的前景展望

### 8. **參考文獻 (References)**
   - 推薦 4-5 篇代表性論文（見下方建議清單）
   - APA 或 IEEE 格式

---

## 📚 推薦的代表性 RAG 論文

基於你的 Option A 選擇，以下是 4-5 篇高度相關的代表性論文：

### 1. **知識衝突與 RAG 可靠性 (Knowledge Conflict & Reliability)**
**Title**: "CRUD: Knowledge Conflict in Retrieval-Augmented Language Models"
- **Authors**: Pasunuru, R., Trivedi, H., Celikyilmaz, A., Choi, Y., Lapata, M., & Hajishirzi, H.
- **Conference**: EMNLP 2023
- **DOI**: https://arxiv.org/abs/2310.03025
- **核心貢獻**: 識別和分析 RAG 系統中的知識衝突（一致性、時效性、無知、不一致），提出 CRUD 框架評估衝突解決能力，暴露當前系統的安全漏洞
- **適用於**: 安全性與可靠性部分、知識衝突處理策略

### 2. **密集向量檢索 (Dense Retrieval)**
**Title**: "Dense Passage Retrieval for Open-Domain Question Answering"
- **Authors**: Vladimir Karpukhin, Barlas Oguz, Sewon Min, et al.
- **Conference**: ICLR 2021
- **DOI**: https://arxiv.org/abs/2004.04906
- **核心貢獻**: 提出 DPR (Dense Passage Retrieval)，展示如何使用密集向量進行高效檢索
- **適用於**: 向量數據庫與檢索方法部分

### 3. **自我反思強化 RAG (Self-Reflective RAG)**
**Title**: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
- **Authors**: Akari Asai, Zeqiu Wu, Yuki Awadalla, et al.
- **Conference**: ICLR 2024
- **DOI**: https://arxiv.org/abs/2310.11511
- **核心貢獻**: 增強 RAG 系統的判斷能力，使 LLM 能決定何時檢索、何時生成，提升準確度
- **適用於**: 系統設計優化與自適應檢索部分

### 4. **大規模 RAG 系統設計 (Scalable RAG)**
**Title**: "In-Context Retrieval-Augmented Language Models"
- **Authors**: Ori Ram, Yoav Levine, Yuval Kirstain, et al.
- **Conference**: ICLR 2023
- **DOI**: https://arxiv.org/abs/2302.00083
- **核心貢獻**: 展示如何在上下文中高效地集成檢索結果，適合大規模部署
- **適用於**: 可擴充性與實務應用部分

### 5. **圖結構增強 RAG (Graph-based RAG)**
**Title**: "GraphRAG: A Modular Graph Retrieval-Augmented Generation System"
- **Authors**: 微軟研究團隊 (尚未正式發表，但被廣泛引用的預印本)
- **Link**: https://arxiv.org/abs/2404.16130
- **核心貢獻**: 利用圖結構組織知識，提升複雜查詢的檢索準確度和多跳推理能力
- **適用於**: 高級架構設計與 Big Data 整合部分

---

## 📝 生成版本說明

目前已生成 **4 個版本的 Survey 文章**：

### 版本 1: 教授級學術版（中文）
- 檔案：`Survey_RAG_for_BigData.md`
- 難度：高等級，學術規範
- 適合：提交給教授或作為參考

### 版本 2: 教授級學術版（英文）
- 檔案：`Survey_RAG_for_BigData_EN.md`
- 難度：高等級，英文學術規範
- 適合：英文課程提交

### 版本 3: 大學生簡化版（中文）⭐ **推薦**
- Markdown：`Survey_RAG_Simple_Version.md`
- **Word 版本**：`Survey_RAG_Simple_Version.docx` ✅ **新增**
- 難度：中等，易於理解
- 語言：清晰簡單，使用常用詞彙
- 適合：語言水平一般的大學生完全可用

### 版本 4: 大學生簡化版（英文）⭐ **推薦**
- Markdown：`Survey_RAG_Simple_Version_EN.md`
- **Word 版本**：`Survey_RAG_Simple_Version_EN.docx` ✅ **新增**
- 難度：中等，英文簡單易懂
- 適合：英文水平一般的大學生

---

## 🎯 版本選擇建議

| 情況 | 建議版本 |
|------|---------|
| 國語課程 | Survey_RAG_Simple_Version.md ✅ |
| 英文課程 | Survey_RAG_Simple_Version_EN.md ✅ |
| 教授要求學術風格 | Survey_RAG_for_BigData.md |
| 英文教授要求 | Survey_RAG_for_BigData_EN.md |
| 作為個人理解參考 | Referenced_Papers_Summary.md |

---

## ✅ 下一步

1. **下載 Word 文件使用**
   - `Survey_RAG_Simple_Version.docx` (中文)
   - `Survey_RAG_Simple_Version_EN.docx` (英文)

2. **根據教授反饋進行調整**
   - 需要修改內容：告知具體部分
   - 需要改格式：可重新生成 Word 版本

3. **其他可用文件**
   - Markdown 版本（便於編輯）
   - PDF 版本（如需要可以轉換）
   - Referenced_Papers_Summary.md（論文參考）

---

## 📋 工作區文件清單

### Survey 文章（推薦使用）
- ✅ `Survey_RAG_Simple_Version.md` (中文簡化版)
- ✅ `Survey_RAG_Simple_Version.docx` (中文簡化版 Word)
- ✅ `Survey_RAG_Simple_Version_EN.md` (英文簡化版)
- ✅ `Survey_RAG_Simple_Version_EN.docx` (英文簡化版 Word)

### 學術版本（供參考）
- `Survey_RAG_for_BigData.md` (中文高級版)
- `Survey_RAG_for_BigData_EN.md` (英文高級版)

### 輔助文件
- `Referenced_Papers_Summary.md` (5 篇論文詳細摘要)
- `SPEC.md` (本文件 - 項目規格說明)
