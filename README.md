# 命理测算系统 (Life Fortune System)

这是一个基于 Cloudflare Workers 全栈开发的命理测算系统，集成了八字命理、紫微斗数排盘算法，并利用 Google Gemini AI 模型生成个性化的命理分析报告。

## ✨ 主要功能

*   **八字排盘**：精准计算四柱八字（年、月、日、时）、十神、五行强弱、纳音、神煞等。
*   **紫微斗数**：完整的紫微斗数排盘，包含命宫、十二宫位及主星分析。
*   **AI 智能解读**：集成 Google Gemini 2.0 Flash 模型，对命盘数据进行深度润色和解读，生成通俗易懂的运势报告。
*   **Markdown 报告渲染**：前端支持 Markdown 格式渲染，排版精美。
*   **PDF 导出**：支持将测算结果一键导出为 PDF 文件，并自动添加“斯蒂文监制”及免责声明水印。
*   **邀请码机制**：
    *   必须使用有效的邀请码才能进行测算。
    *   邀请码使用后自动失效（一次性），或由管理员控制。
*   **后台管理系统**：
    *   生成、查看、禁用/启用、删除邀请码。
    *   查看所有用户的测算记录及详细结果。
*   **数据存储**：使用 Cloudflare D1 (SQLite) 存储邀请码和测算记录，安全可靠。

## 🛠 技术栈

*   **后端 Runtime**: [Cloudflare Workers](https://workers.cloudflare.com/) (Hono 框架)
*   **数据库**: [Cloudflare D1](https://developers.cloudflare.com/d1/) (Serverless SQLite)
*   **AI 模型**: Google Gemini 2.0 Flash (`gemini-2.0-flash-exp`)
*   **核心算法库**:
    *   `lunar-javascript`: 农历及八字计算
    *   `iztro`: 紫微斗数排盘
*   **前端**: 原生 HTML/CSS/JavaScript
    *   `flatpickr`: 日期时间选择
    *   `marked`: Markdown 渲染
    *   `html2pdf.js`: PDF 导出

## 🚀 快速开始

### 1. 环境准备
确保本地已安装 Node.js (>= 18.0.0) 和 `wrangler` CLI。

```bash
npm install
npm install -g wrangler
```

### 2. 数据库初始化
本项目依赖 Cloudflare D1 数据库。请按照以下文档初始化数据库：

*   👉 **[快速开始指南 (命令行)](QUICK-START.md)**：适合开发者，使用 CLI 快速完成配置。
*   👉 **[Cloudflare Web 控制台配置指南](CLOUDFLARE-WEB-SETUP.md)**：适合不熟悉命令行的用户，通过网页界面配置。
*   👉 **[数据库详细文档](README-DB.md)**：数据库表结构及高级操作说明。

### 3. 本地开发
在项目根目录创建 `.dev.vars` 文件，配置必要的环境变量：

```env
GEMINI_API_KEY=your_gemini_api_key
ADMIN_PASSWORD=your_admin_password
```

启动开发服务器：

```bash
npm run dev
```
访问 `http://localhost:8787` 进行测算，访问 `http://localhost:8787/admin.html` 进入后台。

### 4. 部署上线

```bash
npm run deploy
```

部署后，请记得在 Cloudflare Dashboard 中配置生产环境的 Secrets (`GEMINI_API_KEY`, `ADMIN_PASSWORD`)。

## 📂 项目结构

```
.
├── public/                 # 静态资源 (HTML, CSS, JS)
│   ├── index.html          # 用户测算前台
│   ├── admin.html          # 管理员后台
│   └── ...
├── src/
│   ├── ai/                 # AI 提示词与处理逻辑
│   ├── core/               # 八字排盘核心逻辑
│   ├── ziwei/              # 紫微斗数逻辑
│   ├── db/                 # 数据库操作
│   ├── index.js            # 后端入口 (Hono 应用)
│   └── ...
├── schema.sql              # 数据库建表语句
├── wrangler.toml           # Cloudflare Workers 配置
└── ...
```

## ⚠️ 免责声明

本系统生成的命理分析结果仅供娱乐和参考，不构成任何形式的建议或指导。请勿迷信，理性看待。
