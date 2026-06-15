from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from edge_yolo_agent.event_agent import build_event_report, evaluate_events
from edge_yolo_agent.fault_agent import analyze_sensor_frame, build_fault_report, sample_sensor_data


def sample_fault_command() -> str:
    analysis = analyze_sensor_frame(sample_sensor_data())
    return build_fault_report(analysis)


def events_from_json_command(path: Path, scene: str, source: str) -> str:
    detections = json.loads(path.read_text(encoding="utf-8-sig"))
    events = evaluate_events(detections, scene=scene)
    return build_event_report(events, source_name=source)


def fault_from_csv_command(path: Path) -> str:
    frame = pd.read_csv(path)
    analysis = analyze_sensor_frame(frame)
    return build_fault_report(analysis)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Edge YOLO Agent command line tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sample-fault", help="Run built-in industrial fault prediction demo")

    events_parser = subparsers.add_parser("events-from-json", help="Build an event report from YOLO detections JSON")
    events_parser.add_argument("path", type=Path)
    events_parser.add_argument("--scene", default="restricted_area")
    events_parser.add_argument("--source", default="detections.json")

    fault_parser = subparsers.add_parser("fault-from-csv", help="Build a fault prediction report from sensor CSV")
    fault_parser.add_argument("path", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "sample-fault":
        print(sample_fault_command())
        return 0
    if args.command == "events-from-json":
        print(events_from_json_command(args.path, scene=args.scene, source=args.source))
        return 0
    if args.command == "fault-from-csv":
        print(fault_from_csv_command(args.path))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
