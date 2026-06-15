import sys
from types import SimpleNamespace

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
    monkeypatch.setitem(sys.modules, "ultralytics", None)
    monkeypatch.setenv("EDGE_YOLO_PYTHON", sys.executable)

    detector = YoloDetector("models/not-exist.pt")

    assert detector.available is False
    assert "YOLO" in detector.error


def test_default_yolov8n_uses_ultralytics_auto_download_when_missing(monkeypatch):
    created_with = []

    class FakeYOLO:
        def __init__(self, weights):
            created_with.append(weights)

    monkeypatch.delenv("EDGE_YOLO_PYTHON", raising=False)
    monkeypatch.setitem(sys.modules, "ultralytics", SimpleNamespace(YOLO=FakeYOLO))

    detector = YoloDetector("models/yolov8n.pt")

    assert detector.available is True
    assert detector.error is None
    assert created_with == ["yolov8n.pt"]


def test_default_yolov8n_allows_external_python_auto_download(monkeypatch):
    monkeypatch.setitem(sys.modules, "ultralytics", None)
    monkeypatch.setenv("EDGE_YOLO_PYTHON", sys.executable)

    detector = YoloDetector("models/yolov8n.pt")

    assert detector.available is True
    assert detector.error is None


def test_default_yolov8n_reports_auto_download_failure(monkeypatch):
    class FailingYOLO:
        def __init__(self, weights):
            raise ConnectionError("Download failure for yolov8n.pt")

    monkeypatch.delenv("EDGE_YOLO_PYTHON", raising=False)
    monkeypatch.setitem(sys.modules, "ultralytics", SimpleNamespace(YOLO=FailingYOLO))

    detector = YoloDetector("models/yolov8n.pt")

    assert detector.available is False
    assert "自动下载 yolov8n.pt 失败" in detector.error
