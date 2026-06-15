from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4
from typing import Any

import cv2
import numpy as np
from PIL import Image


@dataclass(frozen=True)
class DetectionResult:
    label: str
    confidence: float
    box: list[int]


def format_detections(results: list[DetectionResult]) -> list[dict]:
    return [
        {
            "label": item.label,
            "confidence": round(float(item.confidence), 2),
            "box": item.box,
        }
        for item in results
    ]


class YoloDetector:
    def __init__(self, weights_path: str | Path = "models/yolov8n.pt"):
        self.weights_path = Path(weights_path)
        self.weights_source: str | None = None
        self.model: Any | None = None
        self.error: str | None = None
        self.external_python = os.environ.get("EDGE_YOLO_PYTHON")
        self.weights_source = self._resolve_weights_source()

        try:
            from ultralytics import YOLO
        except Exception:
            if self.external_python and Path(self.external_python).exists():
                if self.weights_source is None:
                    return
                self.error = None
                return
            self.error = "未安装 ultralytics。请运行：pip install ultralytics，或设置 EDGE_YOLO_PYTHON 指向含 ultralytics 的 python.exe"
            return

        if self.weights_source is None:
            return

        try:
            self.model = YOLO(self.weights_source)
        except Exception as exc:
            if self.weights_source == "yolov8n.pt":
                self.error = (
                    "自动下载 yolov8n.pt 失败。请检查网络是否能访问 GitHub，"
                    f"或手动下载 yolov8n.pt 放入 {self.weights_path}。原始错误：{exc}"
                )
            else:
                self.error = f"加载 YOLO 权重失败：{exc}"

    def _resolve_weights_source(self) -> str | None:
        if self.weights_path.exists():
            return str(self.weights_path)
        if self.weights_path.name == "yolov8n.pt" and self.weights_path.parent.name == "models":
            return "yolov8n.pt"
        self.error = f"未找到 YOLO 权重文件：{self.weights_path}"
        return None

    @property
    def available(self) -> bool:
        if self.model is not None:
            return True
        return bool(self.external_python and Path(self.external_python).exists() and self.weights_source is not None)

    def detect_image(self, image: Image.Image, confidence: float = 0.25) -> tuple[list[dict], Image.Image]:
        if self.model is None and self.external_python:
            return self._detect_with_external_python(image, confidence)
        if self.model is None:
            return [], image

        rgb = image.convert("RGB")
        result = self.model.predict(np.array(rgb), conf=confidence, verbose=False)[0]
        names = result.names
        detections: list[DetectionResult] = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            xyxy = [int(v) for v in box.xyxy[0].tolist()]
            detections.append(
                DetectionResult(
                    label=str(names.get(cls_id, cls_id)),
                    confidence=float(box.conf[0]),
                    box=xyxy,
                )
            )
        plotted = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
        return format_detections(detections), Image.fromarray(plotted)

    def _detect_with_external_python(self, image: Image.Image, confidence: float) -> tuple[list[dict], Image.Image]:
        if self.weights_source is None:
            self.error = f"未找到 YOLO 权重文件：{self.weights_path}"
            return [], image

        temp_dir = Path(".streamlit_tmp")
        temp_dir.mkdir(exist_ok=True)
        stem = uuid4().hex
        input_path = temp_dir / f"{stem}_input.jpg"
        json_path = temp_dir / f"{stem}_detections.json"
        out_image_path = temp_dir / f"{stem}_annotated.jpg"
        image.convert("RGB").save(input_path)

        worker_path = Path(__file__).with_name("yolo_worker.py")
        command = [
            self.external_python or sys.executable,
            str(worker_path),
            "--weights",
            self.weights_source,
            "--image",
            str(input_path),
            "--out-json",
            str(json_path),
            "--out-image",
            str(out_image_path),
            "--confidence",
            str(confidence),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if completed.returncode != 0:
            self.error = completed.stderr.strip() or completed.stdout.strip() or "外部 YOLO 进程执行失败"
            return [], image

        detections = json.loads(json_path.read_text(encoding="utf-8"))
        annotated = Image.open(out_image_path).convert("RGB")
        return detections, annotated
