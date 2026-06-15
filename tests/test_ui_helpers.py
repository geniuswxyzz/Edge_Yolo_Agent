from edge_yolo_agent.ui_helpers import build_detection_cache_key, build_image_detection_cache_key


def test_detection_cache_key_changes_when_detection_inputs_change():
    base = build_detection_cache_key(b"image", "demo.jpg", "models/yolov8n.pt", 0.25)

    assert build_detection_cache_key(b"other", "demo.jpg", "models/yolov8n.pt", 0.25) != base
    assert build_detection_cache_key(b"image", "other.jpg", "models/yolov8n.pt", 0.25) != base
    assert build_detection_cache_key(b"image", "demo.jpg", "custom.pt", 0.25) != base
    assert build_detection_cache_key(b"image", "demo.jpg", "models/yolov8n.pt", 0.5) != base


def test_detection_cache_key_changes_when_monitoring_type_changes():
    restricted_area_key = build_detection_cache_key(
        b"image", "demo.jpg", "models/yolov8n.pt", 0.25, "restricted_area"
    )
    warehouse_key = build_detection_cache_key(b"image", "demo.jpg", "models/yolov8n.pt", 0.25, "warehouse")

    assert warehouse_key != restricted_area_key


def test_image_detection_cache_key_requires_monitoring_type():
    restricted_area_key = build_image_detection_cache_key(
        b"image", "demo.jpg", "models/yolov8n.pt", 0.25, "restricted_area"
    )
    warehouse_key = build_image_detection_cache_key(b"image", "demo.jpg", "models/yolov8n.pt", 0.25, "warehouse")

    assert warehouse_key != restricted_area_key
