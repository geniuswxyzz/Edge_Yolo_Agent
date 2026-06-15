import json
from pathlib import Path

import pandas as pd

from edge_yolo_agent.event_agent import evaluate_events
from edge_yolo_agent.fault_agent import analyze_sensor_frame


VIDEO_DATA_DIR = Path("data/video_cases")
FAULT_DATA_DIR = Path("data/fault_cases")


def test_detection_case_files_trigger_expected_events():
    expectations = {
        "detections_restricted_intrusion.json": "人员闯入",
        "detections_fire_risk.json": "烟火风险",
        "detections_workshop_no_helmet.json": "安全帽缺失",
        "detections_normal.json": "未发现明显异常",
    }

    for filename, expected_event in expectations.items():
        detections = json.loads((VIDEO_DATA_DIR / filename).read_text(encoding="utf-8"))
        scene = "workshop" if "workshop" in filename else "restricted_area"
        events = evaluate_events(detections, scene=scene)
        assert any(event["type"] == expected_event for event in events), filename


def test_sensor_case_files_cover_low_medium_high_risk():
    expectations = {
        "sensor_normal.csv": "low",
        "sensor_warning.csv": "medium",
        "sensor_fault_high.csv": "high",
    }

    for filename, expected_risk in expectations.items():
        frame = pd.read_csv(FAULT_DATA_DIR / filename)
        analysis = analyze_sensor_frame(frame)
        assert analysis["risk_level"] == expected_risk, filename
