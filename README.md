# Imprint · 印记

> **Markdown 进，出版社级 PDF 出，自带 0–100 印刷级质检报告。**

[English](README.en.md) · [简体中文](README.md)

Imprint 是一个 AI 原生的中文印刷级 PDF 生成器。它把 Markdown 当成草稿，把 PDF 当成成品——按出版物的标准排版：宋体正文、黑体标题、首行缩进、标点避头尾、目录页码精确、表格跨页重复表头、代码不截断。生成之后，机器自动给这份 PDF 打分：**0–100 印刷级评分，逐项给出证据**。

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/imprint-pdf.svg">
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/imprint-pdf.svg">
  <img alt="License" src="https://img.shields.io/pypi/l/imprint-pdf.svg">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/imprint-pdf.svg">
  <img alt="CI" src="https://github.com/263311487-ux/imprint-pdf/actions/workflows/ci.yml/badge.svg">
  <img alt="Stars" src="https://img.shields.io/github/stars/263311487-ux/imprint-pdf">
</p>

![封面](examples/qa/sample-01.png)

![目录](examples/qa/sample-02.png)

![正文](examples/qa/sample-04.png)

![提示框](examples/qa/alerts-03.png)

![mermaid 流程图](examples/qa/charts-03.png)

## 主题画廊（20 套 · 全部通过印刷级质检）

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

换肤 = 一行命令：`imprint paper.md --theme wine`；**不指定也会智能换肤**——自动分析内容气质选主题并说明理由（如周报自动用 `graphite`，论文自动用 `academic`）。

## 为什么是 Imprint

大多数 Markdown→PDF 工具（pandoc 默认、md2pdf 系、Chrome 打印）只是"把文字倒进页面"。Imprint 的三个差异点：

- **中文印刷级**——严格按《中文排版需求》：避头尾禁则、首行缩进 2 字符、中英文混排字距、孤行寡行控制
- **设计系统即主题**——每套主题是一组 DTCG 设计令牌（色板/字体配对/间距/装饰），换肤 = 换一行
- **印刷级质检报告**——每个 PDF 生成后自动评分 0–100，检查文本可选、字体子集嵌入、标点违规、目录页码、PDF/UA 无障碍标签，证据可查

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
 ✓ PDF/UA 标签          3.0/3.0    Tagged PDF
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
- **主题系统**：20 套主题（见下方画廊）——现代杂志 / 学术书卷 / 北欧极简 / 护眼纸色 / 报纸头版 / 柔和粉彩 / 纯黑白 / 玉石绿 / 咖啡暖棕 / 海洋蓝 / 薰衣草紫 / 樱粉 / 松林绿 / 勃艮第酒红 / 石墨灰 / 深夜蓝纸（暗色）/ 珊瑚橙 / 琥珀金 / 薄荷青 / 沙漠沙色，自定义主题 = 一个 JSON 文件
- **GitHub 风格提示框**：`> [!NOTE]` / `[!TIP]` / `[!WARNING]` / `[!IMPORTANT]` / `[!CAUTION]` 自动渲染为印刷级彩色提示卡，见 `examples/alerts.md`
- **Mermaid 图表**：` ```mermaid ` 代码块自动渲染为矢量图（中文正常、无限缩放），未装引擎时优雅回退代码块，见 `examples/charts.md`
- **数学公式**：`$行内公式$` / `$$块级公式$$` 渲染为矢量 SVG（matplotlib mathtext，无数学字体依赖），见 `examples/math.md`
- **模板系统**：`imprint --new report|book|resume|techdoc|letter` 一键起稿，模板自带对应排版气质（石墨灰报告 / 米黄书稿 / 等宽简历 / 海洋蓝技术文档 / 薰衣草信函）
- **图片压缩**：`--compress` 自动降采样超大图并重编码（实测 11.7MB → 1.4MB）
- **字体体检**：生成前自动检查主题字体本机是否可用，缺失时明确警告
- **中文规范**：避头尾禁则、首行缩进、中英文混排、英文段落自动连字
- **表格跨页**：表头自动重复、行不截断
- **代码高亮**：Pygments 着色、整体换页不截断
- **缺字检测**：渲染后扫描 LastResort/notdef 回退（豆腐块），脚注、箭头等符号缺字自动暴露
- **PDF/UA**：默认输出无障碍标签版
- **AI 原生**：CLI 一行命令；内置 MCP server（`imprint-mcp`），Agent 一句话出报告（tools: render_markdown / list_themes / validate_pdf / new_document）
- **对比度合规**：每套主题自动通过 WCAG 印刷检查（正文 ≥7:1、小字 ≥4.5:1、装饰 ≥3:1）

## 对比

| | pandoc 默认 | Chrome 打印 | Imprint |
|---|---|---|---|
| 中文印刷级 | 弱 | 弱 | **按规范** |
| 设计系统主题 | 无 | 无 | **DTCG tokens** |
| 质检报告 0–100 | 无 | 无 | **自带** |
| 数学公式 | 插件级 | 无 | **矢量内嵌** |
| 模板起稿 | 无 | 无 | **5 套内置** |
| WCAG 对比度检查 | 无 | 无 | **内置** |
| PDF/UA 无障碍 | 手动 | 无 | **默认** |

## 文档

- [完美 PDF 标准](docs/完美PDF标准.md)——"完美"的定义与验收门槛
- [极致借鉴清单](docs/极致借鉴清单_技术选型_20260819.md)——每个环节的社区选型与实测结论

## 路线图

- 更多主题：minimal / ink（线装书）
- npm 分发 `npx imprint`
- 双栏 / 学术模板增强

## License

MIT
