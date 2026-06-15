import pandas as pd

from edge_yolo_agent.fault_agent import analyze_sensor_frame, build_fault_report


def test_analyze_sensor_frame_returns_high_risk_for_hot_vibrating_device():
    frame = pd.DataFrame(
        {
            "timestamp": ["2026-06-13 10:00", "2026-06-13 10:01", "2026-06-13 10:02"],
            "temperature": [70.0, 82.0, 88.0],
            "current": [8.2, 9.1, 9.7],
            "vibration": [2.1, 3.8, 4.4],
        }
    )

    result = analyze_sensor_frame(frame)

    assert result["risk_level"] == "high"
    assert "温度持续偏高" in result["reasons"]
    assert "振动异常" in result["reasons"]


def test_analyze_sensor_frame_returns_low_risk_for_normal_device():
    frame = pd.DataFrame(
        {
            "timestamp": ["2026-06-13 10:00", "2026-06-13 10:01"],
            "temperature": [42.0, 43.5],
            "current": [5.0, 5.2],
            "vibration": [1.1, 1.0],
        }
    )

    result = analyze_sensor_frame(frame)

    assert result["risk_level"] == "low"
    assert result["reasons"] == ["设备运行指标处于正常范围"]


def test_build_fault_report_includes_maintenance_advice():
    analysis = {
        "risk_level": "medium",
        "score": 45,
        "reasons": ["电流波动偏大"],
        "advice": ["检查负载变化和接线端子状态"],
    }

    report = build_fault_report(analysis)

    assert "medium" in report
    assert "电流波动偏大" in report
    assert "检查负载变化" in report
