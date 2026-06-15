from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DetectionProfile:
    label: str
    default_weights: Path
    note: str


DETECTION_PROFILES: dict[str, DetectionProfile] = {
    "restricted_area": DetectionProfile(
        label="限制区域人员闯入",
        default_weights=Path("models/yolov8n.pt"),
        note="使用通用 YOLO 权重检测 person。",
    ),
    "warehouse": DetectionProfile(
        label="仓库火情监控",
        default_weights=Path("models/fire_smoke.pt"),
        note="需要火焰/烟雾专用 YOLO 权重，输出类别建议包含 fire、smoke 或 flame。",
    ),
    "workshop": DetectionProfile(
        label="车间安全帽检查",
        default_weights=Path("models/safety_helmet.pt"),
        note="需要安全帽/PPE 专用 YOLO 权重，输出类别建议包含 helmet、hardhat 或 safety helmet。",
    ),
}


def get_profile_label(scene: str) -> str:
    return DETECTION_PROFILES[scene].label


def get_default_weights_path(scene: str) -> Path:
    return DETECTION_PROFILES[scene].default_weights


def get_profile_note(scene: str) -> str:
    return DETECTION_PROFILES[scene].note
