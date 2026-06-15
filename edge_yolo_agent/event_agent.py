from __future__ import annotations

from datetime import datetime
from typing import Iterable


FIRE_LABELS = {"fire", "smoke", "flame", "烟", "火"}
PERSON_LABELS = {"person", "people", "worker", "行人", "人员"}
HELMET_LABELS = {"helmet", "hardhat", "safety helmet", "安全帽"}


def _matching(detections: Iterable[dict], labels: set[str]) -> list[dict]:
    return [d for d in detections if str(d.get("label", "")).lower() in labels]


def _max_confidence(items: list[dict]) -> float:
    if not items:
        return 0.0
    return round(max(float(item.get("confidence", 0.0)) for item in items), 2)


def evaluate_events(detections: list[dict], scene: str = "restricted_area") -> list[dict]:
    """Convert YOLO detections into course-design safety events."""
    events: list[dict] = []
    people = _matching(detections, PERSON_LABELS)
    fires = _matching(detections, FIRE_LABELS)
    helmets = _matching(detections, HELMET_LABELS)

    if people and scene in {"restricted_area", "warehouse", "workshop"}:
        events.append(
            {
                "type": "人员闯入",
                "level": "high",
                "evidence_count": len(people),
                "max_confidence": _max_confidence(people),
                "suggestion": "立即核查限制区域并通知现场人员。",
            }
        )

    if fires:
        events.append(
            {
                "type": "烟火风险",
                "level": "critical",
                "evidence_count": len(fires),
                "max_confidence": _max_confidence(fires),
                "suggestion": "立刻联动消防检查，确认烟火来源并疏散附近人员。",
            }
        )

    if people and scene == "workshop" and not helmets:
        events.append(
            {
                "type": "安全帽缺失",
                "level": "medium",
                "evidence_count": len(people),
                "max_confidence": _max_confidence(people),
                "suggestion": "提醒作业人员佩戴安全帽，并记录违规片段。",
            }
        )

    if not events:
        events.append(
            {
                "type": "未发现明显异常",
                "level": "low",
                "evidence_count": len(detections),
                "max_confidence": _max_confidence(detections),
                "suggestion": "继续保持巡检，可适当降低告警频率。",
            }
        )

    return events


def build_event_report(events: list[dict], source_name: str = "uploaded media") -> str:
    lines = [
        "边缘 AI 视频分析智能体告警报告",
        f"数据源：{source_name}",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    for idx, event in enumerate(events, start=1):
        lines.extend(
            [
                f"{idx}. 事件类型：{event['type']}",
                f"   风险等级：{event['level']}",
                f"   证据数量：{event['evidence_count']}",
                f"   最高置信度：{event['max_confidence']:.2f}",
                f"   处置建议：{event['suggestion']}",
            ]
        )
    return "\n".join(lines)

