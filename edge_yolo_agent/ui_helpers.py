from __future__ import annotations

from hashlib import sha256
from pathlib import Path


def build_detection_cache_key(
    media_bytes: bytes,
    media_name: str,
    weights_path: str | Path,
    confidence: float,
    *pipeline_options: object,
) -> str:
    digest = sha256(media_bytes).hexdigest()
    option_text = "|".join(str(option) for option in pipeline_options)
    return "|".join([media_name, digest, str(weights_path), f"{confidence:.4f}", option_text])


def build_image_detection_cache_key(
    media_bytes: bytes,
    media_name: str,
    weights_path: str | Path,
    confidence: float,
    scene: str,
) -> str:
    return build_detection_cache_key(media_bytes, media_name, weights_path, confidence, scene)
