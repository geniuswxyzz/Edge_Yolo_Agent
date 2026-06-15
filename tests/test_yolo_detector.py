from edge_yolo_agent.yolo_detector import DetectionResult, YoloDetector, format_detections


def test_format_detections_converts_result_objects_to_dicts():
    results = [
        DetectionResult(label="person", confidence=0.9123, box=[1, 2, 3, 4]),
        DetectionResult(label="fire", confidence=0.801, box=[5, 6, 7, 8]),
    ]

    formatted = format_detections(results)

    assert formatted == [
        {"label": "person", "confidence": 0.91, "box": [1, 2, 3, 4]},
        {"label": "fire", "confidence": 0.8, "box": [5, 6, 7, 8]},
    ]


def test_detector_reports_missing_weights_for_external_python(monkeypatch):
    monkeypatch.setenv("EDGE_YOLO_PYTHON", "D:/WorkSoftware/Anaconda3/envs/Yolo26/python.exe")

    detector = YoloDetector("models/not-exist.pt")

    assert detector.available is False
    assert "未找到 YOLO 权重文件" in detector.error
