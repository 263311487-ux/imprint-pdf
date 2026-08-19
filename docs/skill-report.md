---
title: Imprint PDF Skill 使用报告
subtitle: 本地技能能力白皮书
author: Imprint 排版实验室
date: 2026-08-19
keywords: Imprint, Skill, PDF, 报告
theme: academic
---

# 技能是什么

Imprint PDF Skill 把「生成出版社级中文 PDF」的完整能力固化成本地技能：任何 Codex 会话里，只要提出排版 PDF 的需求，就会自动加载它，按固化好的最佳实践直接产出成品。

> [!IMPORTANT]
> 本报告的验收标准与技能一致：质检必须 100/100 · A+ 才算完成。

# 技能结构

技能位于 `~/.codex/skills/imprint-pdf/`，由三个文件构成，职责分层：

| 文件 | 职责 |
|---|---|
| `SKILL.md` | 精简入口：固定环境、标准流程、硬性规则 |
| `references/themes.md` | 20 套主题的气质对照表与选择技巧 |
| `references/workflow.md` | 质检 11 项修复表、常见坑、OCR 验证法 |

设计原则：入口只保留「会改变决策的信息」，细节全部下沉到按需加载的参考文档。

# 能力清单

技能背后是完整的 Imprint 产品能力：

- **20 套主题**：色相谱全覆盖，从学术书卷到深夜蓝纸暗色系
- **印刷级质检**：0–100 分 11 项检查，含 WCAG 对比度、标点禁则、孤行寡行
- **特色语法**：GitHub 提示框、mermaid 矢量图表、跨页表格
- **工程能力**：图片压缩、字体缺失警告、PDF/UA 无障碍

# 验证证据

技能通过两层验证：

1. 官方校验器 `quick_validate.py` 输出 `Skill is valid!`
2. 真实演练：模拟「古典庄重周报」请求 → 自动映射 `wine` 主题 → 渲染 **100/100** → OCR 复核封面坐标、提示框标签、表格数据全部正确

# 使用方式

触发后按四步走：写 Markdown（frontmatter 决定封面目录）→ 按气质词选主题 → 渲染 → 读到 100 分交付。

```mermaid
graph LR
    A[需求] --> B[写 Markdown]
    B --> C[选主题]
    C --> D[渲染 + 质检]
    D --> E[100 分交付]
    D -- 未达标 --> C
```

# 价值与边界

> [!TIP]
> 换肤只需换一个 `--theme` 参数，正文和结构完全不变；拿不准主题时用 `modern`。

边界：技能只管「生成与排版」。读取、提取、编辑已有 PDF 属于 pdf 技能的范围，不混用。
