from edge_yolo_agent.event_agent import build_event_report, evaluate_events


def test_evaluate_events_flags_person_intrusion():
    detections = [
        {"label": "person", "confidence": 0.86, "box": [10, 20, 120, 220]},
        {"label": "chair", "confidence": 0.72, "box": [130, 80, 210, 220]},
    ]

    events = evaluate_events(detections, scene="restricted_area")

    assert events[0]["type"] == "人员闯入"
    assert events[0]["level"] == "high"
    assert events[0]["evidence_count"] == 1


def test_evaluate_events_flags_fire_risk_from_yolo_labels():
    detections = [{"label": "fire", "confidence": 0.91, "box": [1, 2, 3, 4]}]

    events = evaluate_events(detections, scene="warehouse")

    assert events[0]["type"] == "烟火风险"
    assert events[0]["level"] == "critical"


def test_warehouse_fire_scene_prioritizes_fire_over_person():
    detections = [
        {"label": "person", "confidence": 0.86, "box": [10, 20, 120, 220]},
        {"label": "smoke", "confidence": 0.9, "box": [130, 80, 210, 220]},
    ]

    events = evaluate_events(detections, scene="warehouse")

    assert events[0]["type"] == "烟火风险"
    assert all(event["type"] != "人员闯入" for event in events)


def test_workshop_no_helmet_scene_prioritizes_helmet_missing_over_intrusion():
    detections = [{"label": "person", "confidence": 0.86, "box": [10, 20, 120, 220]}]

    events = evaluate_events(detections, scene="workshop")

    assert events[0]["type"] == "安全帽缺失"
    assert all(event["type"] != "人员闯入" for event in events)


def test_build_event_report_contains_actionable_chinese_summary():
    events = [
        {
            "type": "人员闯入",
            "level": "high",
            "evidence_count": 2,
            "max_confidence": 0.88,
            "suggestion": "立即核查限制区域并通知现场人员。",
        }
    ]

    report = build_event_report(events, source_name="demo.mp4")

    assert "demo.mp4" in report
    assert "人员闯入" in report
    assert "0.88" in report
    assert "立即核查限制区域" in report
