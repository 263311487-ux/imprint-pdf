"""Content-driven theme recommendation: pick a theme from what the document says.

Frontmatter title/subtitle/description/keywords weigh double; body text is
sampled for cheap scoring. Explicit frontmatter `theme` always wins. Falls
back to `modern` when no signal is strong enough.
"""

from __future__ import annotations

import re
from typing import Any

# theme -> (keyword phrase, weight). Longer/more specific phrases weigh more.
SIGNALS: dict[str, list[tuple[str, int]]] = {
    "academic": [
        ("学位论文", 3), ("学术论文", 3), ("学报", 2), ("文献综述", 2),
        ("论文", 2), ("学术", 2), ("研究", 1), ("课题", 1), ("thesis", 2), ("paper", 1),
    ],
    "newspaper": [
        ("新闻", 2), ("快讯", 2), ("头条", 2), ("简报", 2), ("要闻", 2),
        ("公告", 1), ("速览", 1), ("通稿", 1),
    ],
    "sepia": [
        ("散文", 3), ("随笔", 3), ("小说", 2), ("连载", 2), ("札记", 2),
        ("杂记", 2), ("夜读", 1), ("故事", 1),
    ],
    "wine": [
        ("历史", 2), ("古典", 2), ("国学", 2), ("古籍", 2), ("庄重", 1),
        ("经典", 1), ("传统", 1),
    ],
    "graphite": [
        ("周报", 3), ("月报", 3), ("工作报告", 2), ("汇报", 2), ("公文", 2),
        ("纪要", 2), ("复盘", 1), ("总结", 1), ("会议", 1),
    ],
    "gongwen": [
        ("通知", 3), ("决定", 3), ("批复", 3), ("请示", 3), ("通报", 3),
        ("意见", 2), ("印发", 2), ("发文", 2), ("红头", 3), ("人民政府", 3),
        ("公文", 3), ("党政机关", 3), ("贯彻落实", 2), ("主送", 2), ("成文日期", 2),
    ],
    "ocean": [
        ("量化", 2), ("金融", 2), ("投资", 2), ("财报", 2), ("市场", 1),
        ("数据", 1), ("科技", 1), ("工程", 1), ("技术", 1),
    ],
    "jade": [
        ("健康", 2), ("养生", 2), ("中医", 2), ("环保", 2), ("自然", 1),
        ("生态", 1),
    ],
    "mint": [
        ("教程", 3), ("入门", 3), ("使用说明", 2), ("指南", 2), ("新手", 2),
        ("教学", 2),
    ],
    "nord": [
        ("极简", 3), ("北欧", 3), ("设计", 2), ("美学", 2), ("品牌", 1),
    ],
    "coral": [
        ("创意", 2), ("活力", 2), ("年轻", 2), ("活动", 1), ("发布", 1),
    ],
    "coffee": [
        ("咖啡", 3), ("美食", 2), ("生活", 1), ("日常", 1),
    ],
    "lavender": [
        ("文艺", 2), ("温柔", 2), ("诗歌", 2), ("书信", 2), ("诗", 1),
    ],
    "rose": [
        ("生活方式", 2), ("美妆", 2), ("女性", 2), ("情感", 1),
    ],
    "pine": [
        ("森林", 3), ("户外", 2), ("生态", 2), ("自然", 1), ("环保", 1),
    ],
    "minimal": [
        ("少即是多", 3), ("留白", 3), ("克制", 2), ("极简", 2), ("朴素", 2),
        ("简洁", 1),
    ],
    "ink": [
        ("线装", 3), ("文言", 3), ("碑帖", 3), ("书法", 3), ("古籍", 3),
        ("典籍", 3), ("印谱", 3), ("国学", 2), ("篆刻", 3), ("诗词", 2),
    ],
}

_STRIP = re.compile(r"[\s，。、；：？！「」『』（）()【】\[\]·—…,.:;!?\"'`~]")


def _clean(text: str) -> str:
    return _STRIP.sub("", (text or "").lower())


def _hits(text: str, signals: list[tuple[str, int]]) -> tuple[int, str]:
    hay = _clean(text)
    total = 0
    best_phrase, best_ph = "", 0
    for phrase, weight in signals:
        ph = _clean(phrase)
        if not ph:
            continue
        count = hay.count(ph)
        if count:
            total += count * weight
            if count * weight > best_ph:
                best_ph = count * weight
                best_phrase = phrase
    return total, best_phrase


def recommend_theme(meta: dict[str, Any], body_text: str) -> tuple[str, str]:
    """Return (theme, reason). Explicit theme wins; otherwise signals decide."""
    explicit = (meta.get("theme") or "").strip().lower()
    if explicit:
        return explicit, "frontmatter 显式指定"

    heavy = " ".join(
        str(meta.get(k) or "") for k in ("title", "subtitle", "description", "keywords")
    )
    light = body_text[:4000]

    best_theme, best_score, best_phrase = "modern", 0, ""
    for theme, signals in SIGNALS.items():
        h_score, h_phrase = _hits(heavy, signals)
        l_score, l_phrase = _hits(light, signals)
        score = h_score * 2 + l_score
        if score > best_score:
            best_theme, best_score, best_phrase = theme, score, h_phrase or l_phrase

    if best_score == 0:
        return "modern", "未检测到明显内容信号，使用默认主题"
    return best_theme, f"内容含「{best_phrase}」等信号，自动匹配 {best_theme} 气质"
