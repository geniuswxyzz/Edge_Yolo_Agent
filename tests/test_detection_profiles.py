from pathlib import Path

from edge_yolo_agent.detection_profiles import (
    DETECTION_PROFILES,
    get_default_weights_path,
    get_profile_label,
)


def test_detection_profiles_use_distinct_default_weights():
    assert get_default_weights_path("restricted_area") == Path("models/yolov8n.pt")
    assert get_default_weights_path("warehouse") == Path("models/fire_smoke.pt")
    assert get_default_weights_path("workshop") == Path("models/safety_helmet.pt")


def test_detection_profiles_expose_user_facing_labels():
    assert get_profile_label("restricted_area") == "限制区域人员闯入"
    assert get_profile_label("warehouse") == "仓库火情监控"
    assert get_profile_label("workshop") == "车间安全帽检查"


def test_detection_profile_order_matches_page_order():
    assert list(DETECTION_PROFILES) == ["restricted_area", "warehouse", "workshop"]
