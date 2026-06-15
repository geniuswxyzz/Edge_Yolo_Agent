from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
from PIL import Image


RISK_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}


@dataclass(frozen=True)
class SampledFrame:
    frame_index: int
    image: Image.Image


def extract_sample_frames(
    video_path: str | Path,
    every_n_frames: int = 30,
    max_frames: int = 8,
) -> list[SampledFrame]:
    if every_n_frames < 1:
        raise ValueError("every_n_frames must be >= 1")
    if max_frames < 1:
        raise ValueError("max_frames must be >= 1")

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError(f"无法打开视频文件：{video_path}")

    frames: list[SampledFrame] = []
    frame_index = 0
    try:
        while len(frames) < max_frames:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_index % every_n_frames == 0:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(SampledFrame(frame_index=frame_index, image=Image.fromarray(rgb)))
            frame_index += 1
    finally:
        capture.release()

    return frames


def merge_frame_events(frame_events: list[list[dict]]) -> list[dict]:
    merged: dict[str, dict] = {}
    for events in frame_events:
        for event in events:
            event_type = event["type"]
            if event_type == "未发现明显异常" and len(frame_events) > 1:
                continue
            current = merged.get(event_type)
            if current is None:
                merged[event_type] = dict(event)
                continue
            current["evidence_count"] += int(event.get("evidence_count", 0))
            current["max_confidence"] = max(
                float(current.get("max_confidence", 0.0)),
                float(event.get("max_confidence", 0.0)),
            )
            if RISK_RANK.get(event.get("level", "low"), 0) > RISK_RANK.get(current.get("level", "low"), 0):
                current["level"] = event["level"]
                current["suggestion"] = event["suggestion"]

    if not merged:
        return [
            {
                "type": "未发现明显异常",
                "level": "low",
                "evidence_count": 0,
                "max_confidence": 0.0,
                "suggestion": "继续保持巡检，可适当降低告警频率。",
            }
        ]

    return sorted(merged.values(), key=lambda item: RISK_RANK.get(item.get("level", "low"), 0), reverse=True)
