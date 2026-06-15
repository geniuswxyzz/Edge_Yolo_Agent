from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = ROOT / "data" / "video_media"


def _font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def _draw_worker_scene(path: Path) -> None:
    image = Image.new("RGB", (960, 540), "#f3f6f8")
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 390, 960, 540], fill="#c8d2dc")
    draw.rectangle([70, 80, 890, 390], outline="#8a97a4", width=5)
    draw.line([70, 300, 890, 300], fill="#e2b400", width=8)
    draw.text((86, 92), "RESTRICTED AREA", fill="#25313b", font=_font(30))
    draw.text((86, 315), "Safety camera test frame", fill="#25313b", font=_font(24))

    # Worker with hard hat.
    draw.ellipse([410, 145, 510, 245], fill="#f2c19b", outline="#333333", width=3)
    draw.pieslice([395, 120, 525, 205], 180, 360, fill="#ffd33d", outline="#333333", width=3)
    draw.rectangle([430, 245, 490, 365], fill="#2f80ed", outline="#333333", width=3)
    draw.line([430, 275, 365, 330], fill="#333333", width=8)
    draw.line([490, 275, 555, 330], fill="#333333", width=8)
    draw.line([445, 365, 425, 460], fill="#333333", width=8)
    draw.line([475, 365, 505, 460], fill="#333333", width=8)

    image.save(path, quality=92)


def _draw_fire_scene(path: Path) -> None:
    image = Image.new("RGB", (960, 540), "#202833")
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 385, 960, 540], fill="#3d4652")
    draw.rectangle([90, 120, 250, 385], fill="#586474", outline="#9ca7b3", width=3)
    draw.rectangle([710, 110, 860, 385], fill="#586474", outline="#9ca7b3", width=3)
    draw.text((80, 60), "Warehouse fire risk test frame", fill="#f7fafc", font=_font(30))

    for offset, color in [(0, "#ff4d00"), (18, "#ffb000"), (36, "#fff066")]:
        draw.polygon(
            [
                (460, 380 - offset),
                (415 + offset // 2, 300),
                (475, 210 + offset),
                (525 - offset // 2, 300),
                (520, 380 - offset),
            ],
            fill=color,
        )
    for i in range(5):
        x = 400 + i * 45
        draw.ellipse([x, 115 - i * 8, x + 130, 210 - i * 8], fill=(120, 128, 138))

    image.save(path)


def _make_demo_video(path: Path) -> None:
    width, height = 640, 360
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), 10, (width, height))
    for frame_idx in range(36):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = (245, 240, 234)
        cv2.rectangle(frame, (40, 70), (600, 290), (160, 150, 140), 3)
        cv2.putText(frame, "RESTRICTED AREA", (55, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (45, 45, 45), 2)
        cv2.line(frame, (40, 230), (600, 230), (0, 190, 230), 4)

        x = 60 + frame_idx * 12
        cv2.circle(frame, (x, 155), 28, (155, 195, 240), -1)
        cv2.ellipse(frame, (x, 135), (36, 17), 0, 180, 360, (45, 210, 255), -1)
        cv2.rectangle(frame, (x - 18, 185), (x + 18, 260), (220, 110, 40), -1)
        cv2.line(frame, (x - 14, 260), (x - 32, 320), (40, 40, 40), 5)
        cv2.line(frame, (x + 14, 260), (x + 32, 320), (40, 40, 40), 5)
        writer.write(frame)
    writer.release()


def main() -> None:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    _draw_worker_scene(MEDIA_DIR / "restricted_area_worker.jpg")
    _draw_fire_scene(MEDIA_DIR / "warehouse_fire_risk.png")
    _make_demo_video(MEDIA_DIR / "restricted_area_demo.mp4")
    (MEDIA_DIR / "README.md").write_text(
        "# 视频分析测试媒体\n\n"
        "这些文件是在本地生成的合成测试素材，用于验证上传格式和视频分析流程。\n\n"
        "- `restricted_area_worker.jpg`：限制区域人员场景，JPG。\n"
        "- `warehouse_fire_risk.png`：仓库烟火风险场景，PNG。\n"
        "- `restricted_area_demo.mp4`：限制区域人员移动场景，MP4。\n\n"
        "说明：浏览器和 PowerShell 下载外部媒体在当前会话中被安全策略阻止，因此这里使用可复现的本地合成媒体。\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
