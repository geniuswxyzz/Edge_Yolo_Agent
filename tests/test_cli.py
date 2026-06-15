import json
import subprocess
import sys
from pathlib import Path


def test_cli_sample_fault_outputs_report():
    result = subprocess.run(
        [sys.executable, "-m", "edge_yolo_agent.cli", "sample-fault"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "工业设备故障预测 Agent 报告" in result.stdout
    assert "风险等级" in result.stdout


def test_cli_events_from_detections_json():
    detections_path = Path(".test_tmp") / "detections.json"
    detections_path.parent.mkdir(exist_ok=True)
    detections_path.write_text(
        json.dumps([{"label": "person", "confidence": 0.93, "box": [1, 2, 3, 4]}]),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "edge_yolo_agent.cli",
            "events-from-json",
            str(detections_path),
            "--scene",
            "restricted_area",
            "--source",
            "demo.json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "边缘 AI 视频分析智能体告警报告" in result.stdout
    assert "人员闯入" in result.stdout
    assert "0.93" in result.stdout


def test_cli_events_from_json_accepts_utf8_bom():
    detections_path = Path(".test_tmp") / "detections_bom.json"
    detections_path.parent.mkdir(exist_ok=True)
    detections_path.write_text(
        "\ufeff" + json.dumps([{"label": "fire", "confidence": 0.88, "box": [1, 2, 3, 4]}]),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "edge_yolo_agent.cli",
            "events-from-json",
            str(detections_path),
            "--scene",
            "warehouse",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "烟火风险" in result.stdout


def test_cli_fault_from_csv_outputs_report():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "edge_yolo_agent.cli",
            "fault-from-csv",
            "data/fault_cases/sensor_fault_high.csv",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "工业设备故障预测 Agent 报告" in result.stdout
    assert "风险等级：high" in result.stdout
