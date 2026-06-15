from pathlib import Path

import cv2
import numpy as np

from edge_yolo_agent.video_pipeline import extract_sample_frames, merge_frame_events


def _write_tiny_video(path: Path, frame_count: int = 6) -> None:
    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        5,
        (32, 32),
    )
    for index in range(frame_count):
        frame = np.full((32, 32, 3), index * 20, dtype=np.uint8)
        writer.write(frame)
    writer.release()


def test_extract_sample_frames_reads_limited_evenly_spaced_frames():
    temp_dir = Path(".test_tmp")
    temp_dir.mkdir(exist_ok=True)
    video_path = temp_dir / "demo.mp4"
    _write_tiny_video(video_path, frame_count=6)

    frames = extract_sample_frames(video_path, every_n_frames=2, max_frames=2)

    assert len(frames) == 2
    assert frames[0].frame_index == 0
    assert frames[1].frame_index == 2
    assert frames[0].image.size == (32, 32)


def test_merge_frame_events_keeps_highest_risk_and_total_evidence():
    frame_events = [
        [{"type": "未发现明显异常", "level": "low", "evidence_count": 0, "max_confidence": 0.0, "suggestion": "继续巡检。"}],
        [{"type": "人员闯入", "level": "high", "evidence_count": 1, "max_confidence": 0.82, "suggestion": "立即核查。"}],
        [{"type": "人员闯入", "level": "high", "evidence_count": 2, "max_confidence": 0.91, "suggestion": "立即核查。"}],
    ]

    merged = merge_frame_events(frame_events)

    assert merged[0]["type"] == "人员闯入"
    assert merged[0]["evidence_count"] == 3
    assert merged[0]["max_confidence"] == 0.91
