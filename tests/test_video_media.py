from pathlib import Path

import cv2
from PIL import Image


MEDIA_DIR = Path("data/video_media")


def test_video_media_images_are_readable():
    for filename in ["restricted_area_worker.jpg", "warehouse_fire_risk.png"]:
        path = MEDIA_DIR / filename
        assert path.exists(), filename
        with Image.open(path) as image:
            assert image.width >= 320
            assert image.height >= 240


def test_video_media_mp4_is_readable():
    path = MEDIA_DIR / "restricted_area_demo.mp4"
    assert path.exists()

    capture = cv2.VideoCapture(str(path))
    try:
        assert capture.isOpened()
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        assert frame_count >= 10
        assert width >= 320
        assert height >= 240
    finally:
        capture.release()
