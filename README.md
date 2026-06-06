<div align="center">

# 📜 GitChronicle

**AI-powered Git commit history storytelling and changelog generator**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-12%20passing-brightgreen)](tests/)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## English

### 🎉 Introduction

GitChronicle transforms your boring `git log` into **engaging stories**, **structured changelogs**, and **professional release notes**. No more sifting through cryptic commit messages — let GitChronicle narrate your development journey!

**Inspiration:** Born from the pain of reading endless conventional commit logs, GitChronicle adds a human touch to version control history.

### ✨ Core Features

- 📝 **Smart Changelog** — Auto-categorize commits by conventional commit standards
- 📖 **Story Mode** — Three narrative styles: Hero, Journal, Adventure
- 🚀 **Release Notes** — Generate professional release notes with one command
- 📊 **Statistics Dashboard** — Rich terminal UI with commit analytics
- 🎯 **Conventional Commit Support** — Auto-parse `feat:`, `fix:`, `docs:`, etc.
- 💥 **Breaking Change Detection** — Automatically flag breaking changes
- 🎨 **Beautiful Terminal Output** — Powered by Rich library
- 🔧 **Zero Config** — Works out of the box with any git repo

### 🚀 Quick Start

```bash
# Install
pip install gitchronicle

# Generate changelog
gitchronicle changelog

# Tell a story
gitchronicle story --style adventure

# Show statistics
gitchronicle stats

# Generate release notes
gitchronicle release --version v1.0.0
```

### 📖 Usage Guide

#### Changelog Generation

```bash
# Basic usage
gitchronicle changelog

# With date range
gitchronicle changelog --since "1 week ago" --until "today"

# Filter by author
gitchronicle changelog --author "John Doe"

# Save to file
gitchronicle changelog --output CHANGELOG.md
```

#### Story Mode

```bash
# Journal style (default)
gitchronicle story

# Hero style
gitchronicle story --style hero

# Adventure style with custom title
gitchronicle story --style adventure --title "My Project Journey"
```

#### Release Notes

```bash
gitchronicle release --version v2.0.0 --since "v1.0.0"
```

### 💡 Design Philosophy

GitChronicle follows the **"Developer Experience First"** principle:
- **Zero dependencies** for core functionality
- **Intuitive CLI** with helpful error messages
- **Extensible architecture** for custom narrative styles
- **Beautiful by default** terminal output

### 📦 Installation

```bash
pip install gitchronicle
```

Requirements: Python 3.8+

### 🤝 Contributing

PRs welcome! Please follow conventional commit format:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation updates
- `test:` test additions

### 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 简体中文

### 🎉 项目介绍

GitChronicle 将枯燥的 `git log` 转化为**生动的故事**、**结构化的更新日志**和**专业的发布说明**。不再面对晦涩的提交信息 —— 让 GitChronicle 为您讲述开发历程！

**灵感来源：** 源于阅读 endless conventional commit logs 的痛苦，GitChronicle 为版本控制历史增添人文气息。

### ✨ 核心特性

- 📝 **智能更新日志** — 按约定式提交规范自动分类
- 📖 **故事模式** — 三种叙事风格：英雄、日记、冒险
- 🚀 **发布说明** — 一键生成专业版发布说明
- 📊 **统计仪表盘** — 富终端界面提交数据分析
- 🎯 **约定式提交支持** — 自动解析 `feat:`、`fix:`、`docs:` 等
- 💥 **破坏性变更检测** — 自动标记破坏性更新
- 🎨 **精美终端输出** — 基于 Rich 库
- 🔧 **零配置** — 开箱即用，支持任意 Git 仓库

### 🚀 快速开始

```bash
# 安装
pip install gitchronicle

# 生成更新日志
gitchronicle changelog

# 讲述故事
gitchronicle story --style adventure

# 查看统计
gitchronicle stats

# 生成发布说明
gitchronicle release --version v1.0.0
```

### 📖 详细使用指南

#### 更新日志生成

```bash
# 基础用法
gitchronicle changelog

# 指定日期范围
gitchronicle changelog --since "1 week ago" --until "today"

# 按作者筛选
gitchronicle changelog --author "John Doe"

# 保存到文件
gitchronicle changelog --output CHANGELOG.md
```

#### 故事模式

```bash
# 日记风格（默认）
gitchronicle story

# 英雄风格
gitchronicle story --style hero

# 冒险风格 + 自定义标题
gitchronicle story --style adventure --title "我的项目之旅"
```

#### 发布说明

```bash
gitchronicle release --version v2.0.0 --since "v1.0.0"
```

### 💡 设计思路

GitChronicle 遵循 **"开发者体验优先"** 原则：
- 核心功能**零依赖**
- **直观的 CLI** 搭配友好的错误提示
- **可扩展架构** 支持自定义叙事风格
- 默认输出**精美优雅**

### 📦 打包与部署

```bash
# 从源码安装
git clone https://github.com/gitstq/GitChronicle.git
cd GitChronicle
pip install -e .

# 运行测试
pytest tests/ -v
```

环境要求：Python 3.8+

### 🤝 贡献指南

欢迎提交 PR！请遵循约定式提交格式：
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `test:` 测试补充

### 📄 开源协议

MIT 协议 — 详见 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 🎉 專案介紹

GitChronicle 將枯燥的 `git log` 轉化為**生動的故事**、**結構化的更新日誌**和**專業的發布說明**。不再面對晦澀的提交資訊 —— 讓 GitChronicle 為您講述開發歷程！

**靈感來源：** 源於閱讀無盡 conventional commit logs 的痛苦，GitChronicle 為版本控制歷史增添人文氣息。

### ✨ 核心特性

- 📝 **智能更新日誌** — 按約定式提交規範自動分類
- 📖 **故事模式** — 三種敘事風格：英雄、日記、冒險
- 🚀 **發布說明** — 一鍵生成專業版發布說明
- 📊 **統計儀表盤** — 富終端界面提交數據分析
- 🎯 **約定式提交支援** — 自動解析 `feat:`、`fix:`、`docs:` 等
- 💥 **破壞性變更檢測** — 自動標記破壞性更新
- 🎨 **精美終端輸出** — 基於 Rich 庫
- 🔧 **零配置** — 開箱即用，支援任意 Git 倉庫

### 🚀 快速開始

```bash
# 安裝
pip install gitchronicle

# 生成更新日誌
gitchronicle changelog

# 講述故事
gitchronicle story --style adventure

# 查看統計
gitchronicle stats

# 生成發布說明
gitchronicle release --version v1.0.0
```

### 📖 詳細使用指南

#### 更新日誌生成

```bash
# 基礎用法
gitchronicle changelog

# 指定日期範圍
gitchronicle changelog --since "1 week ago" --until "today"

# 按作者篩選
gitchronicle changelog --author "John Doe"

# 儲存到檔案
gitchronicle changelog --output CHANGELOG.md
```

#### 故事模式

```bash
# 日記風格（預設）
gitchronicle story

# 英雄風格
gitchronicle story --style hero

# 冒險風格 + 自訂標題
gitchronicle story --style adventure --title "我的專案之旅"
```

#### 發布說明

```bash
gitchronicle release --version v2.0.0 --since "v1.0.0"
```

### 💡 設計思路

GitChronicle 遵循 **"開發者體驗優先"** 原則：
- 核心功能**零依賴**
- **直觀的 CLI** 搭配友善的錯誤提示
- **可擴展架構** 支援自訂敘事風格
- 預設輸出**精美優雅**

### 📦 打包與部署

```bash
# 從原始碼安裝
git clone https://github.com/gitstq/GitChronicle.git
cd GitChronicle
pip install -e .

# 執行測試
pytest tests/ -v
```

環境要求：Python 3.8+

### 🤝 貢獻指南

歡迎提交 PR！請遵循約定式提交格式：
- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文件更新
- `test:` 測試補充

### 📄 開源協議

MIT 協議 — 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

Made with ❤️ by GitChronicle Team

</div>
