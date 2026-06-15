import os
import sys
from pathlib import Path

from edge_yolo_agent.pycharm_launcher import build_streamlit_command, build_streamlit_env


def test_build_streamlit_command_uses_current_python_and_app_path():
    command = build_streamlit_command(Path("app.py"), port=8600)

    assert command[:4] == [sys.executable, "-m", "streamlit", "run"]
    assert command[4] == "app.py"
    assert "--server.port" in command
    assert "8600" in command
    assert "--server.headless" in command
    assert "true" in command


def test_build_streamlit_env_defaults_edge_yolo_python_to_current_interpreter(monkeypatch):
    monkeypatch.delenv("EDGE_YOLO_PYTHON", raising=False)

    env = build_streamlit_env()

    assert env["EDGE_YOLO_PYTHON"] == sys.executable
    assert env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] == "false"
    assert env["STREAMLIT_SERVER_HEADLESS"] == "true"
    assert os.environ.get("EDGE_YOLO_PYTHON") is None
