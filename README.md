<!-- mcp-name: io.github.263311487-ux/imprint-pdf -->
# Imprint · 印记

> **Markdown 进，出版社级 PDF 出，自带 0–100 印刷级质检报告。**

<p align="center">
  <a href="https://263311487-ux.github.io/imprint-pdf/"><img src="docs/social-preview.svg" alt="Imprint · 印记 — Markdown 进，出版社级 PDF 出"></a>
</p>

[English](README.en.md) · [简体中文](README.md) · [在线画廊与演示](https://263311487-ux.github.io/imprint-pdf/) · [本地生成指南](docs/first-success.md)

Imprint 是一个 AI 原生的中文印刷级 PDF 生成器。它把 Markdown 当成草稿，把 PDF 当成成品——按出版物的标准排版：宋体正文、黑体标题、首行缩进、标点避头尾、目录页码精确、表格跨页重复表头、代码不截断。生成之后，机器自动给这份 PDF 打分：**0–100 印刷级评分，逐项给出证据**。

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/imprint-pdf.svg">
  <img alt="npm" src="https://img.shields.io/npm/v/imprint-pdf.svg">
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/imprint-pdf.svg">
  <img alt="License" src="https://img.shields.io/pypi/l/imprint-pdf.svg">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/imprint-pdf.svg">
  <img alt="CI" src="https://github.com/263311487-ux/imprint-pdf/actions/workflows/ci.yml/badge.svg">
  <img alt="Stars" src="https://img.shields.io/github/stars/263311487-ux/imprint-pdf">
</p>

> **在线演示可用性有限。** 提交的 Markdown 会发送到临时托管服务器进行渲染；请勿上传私密或敏感文档。需要处理私密内容时，请按[本地生成指南](docs/first-success.md)在本机运行。


## 快速开始（需先准备平台依赖）

```bash
# 方式一：npm 包装器（首次可能联网安装 Python 引擎）
npx imprint-pdf 论文.md

# 方式二：pip 安装（已发布到 PyPI）
pip install imprint-pdf
imprint 论文.md

# 常用命令
npx imprint-pdf --new report     # 从模板起稿
npx imprint-pdf --list-themes    # 24 套主题
npx imprint-pdf 论文.md --theme academic --out 论文.pdf
```

### 首次成功与平台依赖

以下仅用于已安装本源码的仓库根目录（pip 包不含顶层 examples）：先运行 `python3 -m imprint --version`，应输出 `imprint 0.14.0`；再运行 `python3 -m imprint examples/sample.md --out sample.pdf` 完成离线样例。需要 Python 3.10+、项目依赖，以及 WeasyPrint 的原生 Pango/GLib：macOS 用 Homebrew 安装 Pango，Debian/Ubuntu 安装 `libpango-1.0-0` 与 `libpangoft2-1.0-0`，Windows 安装当前 GTK3 runtime。中文字体需由使用者自行安装。

质检分数是本仓库检查项的可重复启发式评分，不是印刷厂认证；PDF/UA 行只检查 Tagged PDF 标记，并不等同于完整 PDF/UA 合规。正式发布仍需专用无障碍校验器和人工印前打样。

完整安装指南和平台矩阵见 [首次成功指南](docs/first-success.md)。源码版本与注册表版本可能不同；发布前请分别核对 PyPI、npm 和 GitHub Release。

![封面](examples/qa/sample-01.png)

![目录](examples/qa/sample-02.png)

![正文](examples/qa/sample-04.png)

![提示框](examples/qa/alerts-03.png)

![mermaid 流程图](examples/qa/charts-03.png)

## 主题画廊（24 套 · 全部通过印刷级质检）

<p align="center">
<img src="examples/qa/modern-01.png" width="150" alt="modern"/>
<img src="examples/qa/academic-01.png" width="150" alt="academic"/>
<img src="examples/qa/nord-01.png" width="150" alt="nord"/>
<img src="examples/qa/sepia-01.png" width="150" alt="sepia"/>
<img src="examples/qa/newspaper-01.png" width="150" alt="newspaper"/>
</p>
<p align="center">
<img src="examples/qa/catppuccin-01.png" width="150" alt="catppuccin"/>
<img src="examples/qa/mono-01.png" width="150" alt="mono"/>
<img src="examples/qa/jade-01.png" width="150" alt="jade"/>
<img src="examples/qa/coffee-01.png" width="150" alt="coffee"/>
<img src="examples/qa/ocean-01.png" width="150" alt="ocean"/>
</p>
<p align="center">
<img src="examples/qa/lavender-01.png" width="150" alt="lavender"/>
<img src="examples/qa/rose-01.png" width="150" alt="rose"/>
<img src="examples/qa/pine-01.png" width="150" alt="pine"/>
<img src="examples/qa/wine-01.png" width="150" alt="wine"/>
<img src="examples/qa/graphite-01.png" width="150" alt="graphite"/>
</p>
<p align="center">
<img src="examples/qa/midnight-01.png" width="150" alt="midnight"/>
<img src="examples/qa/coral-01.png" width="150" alt="coral"/>
<img src="examples/qa/amber-01.png" width="150" alt="amber"/>
<img src="examples/qa/mint-01.png" width="150" alt="mint"/>
<img src="examples/qa/sand-01.png" width="150" alt="sand"/>
</p>
<p align="center">
<img src="examples/qa/minimal-01.png" width="150" alt="minimal"/>
<img src="examples/qa/ink-01.png" width="150" alt="ink"/>
<img src="examples/qa/gongwen-01.png" width="150" alt="gongwen 公文"/>
<img src="examples/qa/ieee-03.png" width="150" alt="ieee 英文论文"/>
</p>

## 双栏学术论文模板

`imprint --new paper` 一键生成双栏学术论文：摘要/关键词通栏，正文双栏排版，标题不落页尾、表格不跨栏截断、行内公式不断行。

<p align="center">
<img src="examples/qa/paper-03.png" width="260" alt="paper 双栏正文"/>
<img src="examples/qa/paper-04.png" width="260" alt="paper 双栏图表"/>
</p>

英文论文用 `imprint --new ieee`：IEEE 风格（Times 10pt 紧凑双栏 + IEEE 蓝），
`lang: en` 自动切换文档语言标签，Abstract / Index Terms 通栏。

<p align="center">
<img src="examples/qa/ieee-03.png" width="300" alt="ieee 双栏英文论文"/>
</p>

## 公文风格模板（不宣称 GB/T 9704 合规）

`imprint --new gongwen` 生成公文风格草稿（未按 GB/T 9704 全项验证，不宣称标准合规）：
红色发文机关标志、发文字号、红色分隔线（★）、黑体标题、仿宋三号正文、
右对齐落款与成文日期。

<p align="center">
<img src="examples/qa/gongwen-01.png" width="300" alt="gongwen 红头文件"/>
</p>

换肤 = 一行命令：`imprint paper.md --theme wine`；**不指定也会智能换肤**——自动分析内容气质选主题并说明理由（如周报自动用 `graphite`，论文自动用 `academic`）。

## 为什么是 Imprint

大多数 Markdown→PDF 工具（pandoc 默认、md2pdf 系、Chrome 打印）只是"把文字倒进页面"。Imprint 的三个差异点：

- **中文印刷级**——严格按《中文排版需求》：避头尾禁则、首行缩进 2 字符、中英文混排字距、孤行寡行控制
- **设计系统即主题**——每套主题是一组 DTCG 设计令牌（色板/字体配对/间距/装饰），换肤 = 换一行
- **印刷级质检报告**——每个 PDF 生成后自动评分 0–100，检查文本可选、字体子集嵌入、标点违规、目录页码、Tagged PDF 标记，证据可查

## 快速开始

```bash
pip install imprint-pdf
# 图表支持（可选）
pip install imprint-pdf[charts]
# MCP server（可选，Agent 一句话出报告）
pip install imprint-pdf[mcp]

imprint paper.md -o paper.pdf
imprint paper.md --theme sepia --compress
# 从模板起稿（报告/书籍/简历/技术文档/信函）
imprint --new report -o my_report.md
# 启动 MCP server（stdio），供 Claude Code / Cursor / DeepSeek Harness 等接入
imprint-mcp
```

输出结尾是一张质检报告：

```
印刷级质检报告
==============================================
 ✓ 文本可选              15.0/15.0   平均每页 722 字符
 ✓ 字体子集嵌入            15.0/15.0   5/5 字体已嵌入
 ✓ 元数据完整              3.0/3.0    标题「印记」
 ✓ 标点避头尾             15.0/15.0   0 违规
 ✓ 孤行寡行               9.0/9.0    0 处
 ✓ 目录页码              15.0/15.0   核对 15 条
 ✓ 页码存在               2.0/2.0    8/9 页含页码
 ✓ Tagged PDF 标记          3.0/3.0    Tagged PDF
 ✓ 主题字体生效             3.0/3.0    命中 songti
 ✓ 主题对比度              5.0/5.0    正文 17.0:1 …
 ✓ 缺字检测               5.0/5.0    无缺字回退
 ✓ 内容溢出               5.0/5.0    无内容越界
 ✓ 图片清晰度              5.0/5.0    全部达标
 ----------------------------------------------
 总分 100.0/100 · 等级 A+ · 9 页
```

## 特性

- **封面 + 目录**：frontmatter 里的 `title / author / date` 自动生成封面，标题自动生成可点击目录（页码精确）
- **智能换肤**：不指定主题时，按标题/关键词/正文信号自动推荐（含理由）；显式指定优先
- **主题系统**：24 套主题（见下方画廊）——现代杂志 / 学术书卷 / 北欧极简 / 护眼纸色 / 报纸头版 / 柔和粉彩 / 纯黑白 / 玉石绿 / 咖啡暖棕 / 海洋蓝 / 薰衣草紫 / 樱粉 / 松林绿 / 勃艮第酒红 / 石墨灰 / 深夜蓝纸（暗色）/ 珊瑚橙 / 琥珀金 / 薄荷青 / 沙漠沙色 / **极简（minimal）** / **线装书（ink，宣纸+印章红）** / **红头公文（gongwen）** / **IEEE 英文论文（ieee）**，自定义主题 = 一个 JSON 文件
- **GitHub 风格提示框**：`> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!IMPORTANT]` / `[!CAUTION]` 自动渲染为印刷级彩色提示卡，见 `examples/alerts.md`
- **Mermaid 图表**：` ```mermaid ` 代码块自动渲染为矢量图（中文正常、无限缩放），未装引擎时优雅回退代码块，见 `examples/charts.md`
- **数学公式**：`$行内公式$` / `$$块级公式$$` 渲染为矢量 SVG（matplotlib mathtext，无数学字体依赖），见 `examples/math.md`
- **模板系统**：`imprint --new report|book|resume|techdoc|letter|paper|gongwen|ieee` 一键起稿，模板自带对应排版气质（石墨灰报告 / 米黄书稿 / 等宽简历 / 海洋蓝技术文档 / 薰衣草信函 / 双栏学术论文 / 红头公文 / IEEE 英文论文）
- **图片压缩**：`--compress` 自动降采样超大图并重编码（实测 11.7MB → 1.4MB）
- **字体体检**：生成前自动检查主题字体本机是否可用，缺失时明确警告
- **中文规范**：避头尾禁则、首行缩进、中英文混排、英文段落自动连字
- **表格跨页**：表头自动重复、行不截断
- **代码高亮**：Pygments 着色、整体换页不截断
- **缺字检测**：渲染后扫描 LastResort/notdef 回退（豆腐块），脚注、箭头等符号缺字自动暴露
- **带标签 PDF**：默认请求 WeasyPrint PDF/UA-1 输出模式；完整无障碍合规仍需验证
- **AI 原生**：CLI 一行命令；内置 MCP server（`pip install "imprint-pdf[mcp]"` → `imprint-mcp`），实际工具名为 `render_markdown`、`list_themes_tool`、`validate_pdf_tool`、`new_document_tool`。Docker 与 Glama 前置步骤见[容器接入说明](docs/mcp-container.md)。
- **对比度合规**：按主题色板计算 WCAG 对比度比值（正文 ≥7:1、小字 ≥4.5:1、装饰 ≥3:1）

## 能力边界

Imprint 组合了 Markdown 排版、主题与启发式检查。其他工具的能力依版本和插件配置而异；本项目没有受控竞品测试，不作绝对优劣比较。

## 文档

- [完美 PDF 标准](docs/完美PDF标准.md)——"完美"的定义与验收门槛
- [极致借鉴清单](docs/极致借鉴清单_技术选型_20260819.md)——每个环节的社区选型与实测结论
- [项目故事 · 从草稿到成品](docs/skill-report.md)——为什么做、怎么做到极致（[成品 PDF](https://263311487-ux.github.io/imprint-pdf/skill-report.pdf)）
- [为什么需要质检门（0-100 分）](docs/why-quality-gate.md)——质检不是炫技，是文档的 CI

## 路线图

- 更多主题（24 套已上线：minimal / ink / gongwen / ieee 等）
- npm 分发 `npx imprint-pdf`（已上线）
- 双栏 / 学术模板（已上线）
- [x] PyPI 发布（注册表版本与源码可能不同）
- 更多双栏模板（IEEE / 公文 / 病历等）

## Related tools

- [**falsify**](https://github.com/263311487-ux/falsify) — the scientific thinking protocol for AI agents. Before you typeset the perfect PDF, let falsify check the conclusion it presents: hypothesis → falsify → evidence → calibrated verdict.
- [**dsh-verify**](https://github.com/263311487-ux/dsh-verify) — browser-verified delivery for agent-built apps: real-browser tests that catch broken output a judge cannot see.

One-command installs: `npx skills add 263311487-ux/falsify` · `npx dsh-verify` · `npx imprint-pdf`

## License

MIT
