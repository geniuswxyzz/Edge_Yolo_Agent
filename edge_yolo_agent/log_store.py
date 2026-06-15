from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def append_event_log(path: str | Path, source_name: str, events: list[dict]) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "source": source_name,
        "events": events,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_event_logs(path: str | Path) -> list[dict]:
    log_path = Path(path)
    if not log_path.exists():
        return []
    return [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
