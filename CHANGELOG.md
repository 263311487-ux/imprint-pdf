# Changelog

## [0.13.0] - 2026-08-20

### Fixed
- npx 一键安装稳健性：自动安装引擎失败时自动重试；新增清华镜像源（国内用户）；GitHub 源兜底改用 HTTP/1.1 规避 HTTP2 framing 网络错误
All notable changes to Imprint are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is SemVer.

## [0.11.0] - 2026-08-19

### Added
- IEEE 风格英文双栏论文模板：`imprint --new ieee` + `ieee` 主题（Times 10pt 紧凑双栏 + IEEE 蓝 #00629B）；frontmatter `lang: en` 自动切换 `<html lang>`（PDF/UA 语言标签更准确）
- 验证器字体匹配规范化：PDF 字体名带子集前缀+连字符（`ESSOFH+Times-New-Roman,`），多词提示（Times New Roman）此前匹配失败 → 统一去非字母数字后子串匹配；`theme-font-hint` 现在对多词字体名也生效
- 智能换肤新增 IEEE 信号（ieee / index terms / conference paper 等）

## [0.10.0] - 2026-08-19

### Added
- 党政机关公文模板：`imprint --new gongwen` + frontmatter `layout: gongwen` — GB/T 9704 红头版式（红色发文机关标志 30pt、发文字号、红色分隔线含 ★、无封面无目录、主送机关顶格、右对齐落款）；新增 `gongwen` 主题（仿宋三号正文 16pt、黑体标题、标准公文页边距）；智能换肤新增公文信号（通知/决定/批复/请示/印发/红头/人民政府 等）
- `:::addressee`（主送机关）与 `:::signature`（落款）容器，双栏版之后第二套排版语言
- 修复：layout CSS 曾以 `{{ }}` 输出（tinycss2 恰好容忍）；版头此前用 h1 会被「首个 h1 加 first」规则写成双 class 导致红色/字号失效，改用 `<p>` 规避

## [0.9.0] - 2026-08-19

### Added
- 双栏学术论文模板：`imprint --new paper` + frontmatter `layout: two-column` — 摘要/关键词通栏（`:::abstract` / `:::keywords` 容器），正文双栏，标题不落页尾、表格不跨栏、行内公式用 U+2060+nowrap 防断行
- 验证器目录页码校验改读 PDF 书签（outline），比全文检索更准（不再被正文里的同名词误导）
- 行首禁则检测豁免「公式图形 + 标点」合法行（pdfplumber 提取不到矢量公式文字导致的误报）

## [0.8.0] - 2026-08-19

### Added
- 双栏学术论文模板：`imprint --new paper` + frontmatter `layout: two-column` — 摘要/关键词通栏（`:::abstract` / `:::keywords` 容器），正文双栏，标题不落页尾、表格不跨栏、行内公式用 U+2060+nowrap 防断行；验证器目录校验改读 PDF 书签（更准），行首禁则检测自动豁免「公式图形 + 标点」合法行
- npm 发布：`npx imprint-pdf` 一行命令体验（自动安装 Python 引擎，PyPI→GitHub 兜底）；包内提供 `imprint` / `imprint-pdf` 两个 bin
- 主题：新增 minimal（极简：白纸黑字留白）与 ink（线装书：宣纸米色 + 印章朱红）；主题清单改为动态扫描，新增主题无需改代码；智能换肤支持新主题信号（古籍/线装/文言 → ink，留白/克制 → minimal）
- MCP server：`imprint-mcp`（stdio）暴露 4 个工具（render_markdown / list_themes / validate_pdf / new_document），AI Agent 一句话出印刷级 PDF；依赖 `pip install imprint-pdf[mcp]`
- 数学公式：`$行内公式$` / `$$块级公式$$` 经 matplotlib mathtext 渲染为矢量 SVG，无数学字体依赖，见 `examples/math.md`
- 模板系统：`imprint --new report|book|resume|techdoc|letter` 一键起稿，`--list-templates` 列出模板
- 质检新增 3 项（共 14 项，100 分制）：缺字检测（LastResort/notdef 回退）、内容溢出、图片清晰度（<150 DPI 警告）
- 脚注返回箭头改用 U+2191（原 U+21A9+FE0E 在 CJK 字体内缺失，会触发 Pango LastResort 回退 = 豆腐块）

### Changed
- 质检分数重分配：文本可选 15 / 字体 15 / 标点 15 / 目录 15 / 孤行 9 / 元数据 3 / 主题字体 3 / PDF-UA 3 / 页码 2 / 对比度 5 / 缺字 5 / 溢出 5 / 图片 DPI 5
- `--list-templates` 改为动态读取模板目录

## [0.7.0] - 2026-08-18

### Added
- 20 套设计系统主题（DTCG tokens，全部通过 WCAG 对比度 + 印刷级质检）
- GitHub 风格提示框（NOTE/TIP/WARNING/IMPORTANT/CAUTION）
- Mermaid 图表（纯 Python 渲染，零 Node 依赖，未装引擎时优雅回退）
- 图片压缩 `--compress`（降采样 + 重编码）
- 字体体检（生成前检查主题字体本机可用性）
- 智能换肤（按内容气质自动推荐主题并说明理由）
- PDF 书签 / PDF-UA 无障碍标签默认开启

### Changed
- 质检报告升级为 0–100 分制，逐项证据可查
