---
title: 数学公式排版指南
author: Imprint
date: 2026-08-19
theme: academic
---

# 在 PDF 里写公式

Imprint 直接渲染 LaTeX 数学公式：行内公式与块级公式都输出为矢量路径，不依赖任何数学字体，印刷清晰、缩放无损。

## 行内公式

欧拉恒等式 $e^{i\pi} + 1 = 0$ 被称为数学中最美的公式。勾股定理 $a^2 + b^2 = c^2$ 同样常见，不等式 $a < b$ 与 $x \geq y$ 也正常处理。

## 块级公式

定积分：

$$
\int_0^1 x^2 \, dx = \frac{1}{3}
$$

麦克斯韦方程组（微分形式）：

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}, \qquad
\nabla \times \mathbf{B} - \frac{1}{c^2}\frac{\partial \mathbf{E}}{\partial t} = \mu_0 \mathbf{J}
$$

## 语法

行内用单美元 `$...$`，块级用双美元独占一行 `$$...$$`。公式由 matplotlib mathtext 渲染为 SVG 路径，支持常见 LaTeX 数学命令（分式、积分、求和、希腊字母、粗体、算符等）。
