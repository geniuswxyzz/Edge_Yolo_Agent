from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-image", required=True)
    parser.add_argument("--confidence", type=float, default=0.25)
    args = parser.parse_args()

    model = YOLO(args.weights)
    result = model.predict(args.image, conf=args.confidence, verbose=False)[0]
    names = result.names
    detections = []
    for box in result.boxes:
        cls_id = int(box.cls[0])
        detections.append(
            {
                "label": str(names.get(cls_id, cls_id)),
                "confidence": round(float(box.conf[0]), 2),
                "box": [int(v) for v in box.xyxy[0].tolist()],
            }
        )

    annotated = result.plot()
    cv2.imwrite(args.out_image, annotated)
    Path(args.out_json).write_text(json.dumps(detections, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
