---
title: An Effective Approach to the Title of Your Paper
subtitle: IEEE-style two-column paper
author: First Author, Second Author, Third Author
date: 2026-08-19
theme: ieee
layout: two-column
lang: en
theme-font-hint: Times New Roman
keywords: component; formatting; style; styling; insert
---

:::abstract
**Abstract** — This template provides a quick start for writing an IEEE-style
two-column paper with Imprint. State the problem, the proposed method, and the
key results in 150–250 words. The abstract and index terms span both columns;
the body flows in two columns below.
:::

:::keywords
**Index Terms** — component; formatting; style; styling; insert
:::

# I. Introduction

Introduce the research problem, its importance, and the contributions of this
paper. Cite related work with bracket numbers, e.g., as in [1].

# II. Proposed Method

## A. Problem Formulation

Define the problem mathematically. Inline math $E=mc^2$ and display math are
supported:

$$
\mathcal{L}(\theta)=\frac{1}{n}\sum_{i=1}^{n}\ell\big(f(x_i;\theta),y_i\big)
$$

## B. Algorithm

```python
def train(model, data, epochs):
    for epoch in range(epochs):
        for x, y in data:
            loss = model.fit(x, y)
    return model
```

# III. Experiments

Table \ref{tab:results} summarizes the results on two public benchmarks.

| Dataset | Metric | Ours |
| --- | ---: | ---: |
| Dataset-A | Accuracy | 0.912 |
| Dataset-B | F1 | 0.874 |

# IV. Conclusion

Summarize the contributions and outline future work.

# References

[1] A. Author and B. Author, "Paper title," *Journal Name*, vol. 12, no. 3, pp. 45–60, 2024.
[2] C. Author, *Book Title*. City: Publisher, 2023.
