from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_streamlit_command(app_path: Path, port: int = 8501) -> list[str]:
    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]


def build_streamlit_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("EDGE_YOLO_PYTHON", sys.executable)
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    return env


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PyCharm launcher for the Edge YOLO Agent Streamlit app")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args(argv)

    app_path = PROJECT_ROOT / "app.py"
    command = build_streamlit_command(app_path, port=args.port)
    completed = subprocess.run(command, cwd=PROJECT_ROOT, env=build_streamlit_env(), check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
