from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

from edge_yolo_agent.event_agent import build_event_report, evaluate_events
from edge_yolo_agent.fault_agent import analyze_sensor_frame, build_fault_report, sample_sensor_data
from edge_yolo_agent.log_store import append_event_log, read_event_logs
from edge_yolo_agent.video_pipeline import extract_sample_frames, merge_frame_events
from edge_yolo_agent.yolo_detector import YoloDetector


ROOT = Path(__file__).parent
LOG_PATH = ROOT / "data" / "event_logs.jsonl"
DEFAULT_WEIGHTS = ROOT / "models" / "yolov8n.pt"
TMP_DIR = ROOT / ".streamlit_tmp"


st.set_page_config(page_title="边缘 AI 视频分析与故障预测 Agent", layout="wide")


def render_video_agent() -> None:
    st.header("边缘 AI 视频分析 Agent")
    st.caption("上传图片或视频后调用 YOLO 检测目标，再由规则 Agent 生成告警事件和中文处置建议。")

    col_config, col_result = st.columns([0.34, 0.66])
    with col_config:
        weights_path = st.text_input("YOLO 权重路径", value=str(DEFAULT_WEIGHTS))
        scene = st.selectbox("场景", ["restricted_area", "warehouse", "workshop"], index=0)
        confidence = st.slider("检测置信度", min_value=0.1, max_value=0.9, value=0.25, step=0.05)
        uploaded = st.file_uploader("上传图片或视频", type=["jpg", "jpeg", "png", "mp4", "avi", "mov"])
        every_n_frames = st.number_input("视频抽帧间隔", min_value=1, max_value=300, value=30, step=1)
        max_frames = st.number_input("视频最多分析帧数", min_value=1, max_value=30, value=8, step=1)
        st.info("若未安装 ultralytics 或没有权重文件，页面会显示原因。将 yolov8n.pt 放入 models/ 后即可实检。")

    with col_result:
        if uploaded is None:
            st.write("等待上传图片或视频。")
            return

        detector = YoloDetector(weights_path)
        if not detector.available:
            st.warning(detector.error)
            if uploaded.type.startswith("image/"):
                st.image(Image.open(uploaded), caption="原始图片", use_container_width=True)
            return

        if uploaded.type.startswith("image/"):
            image = Image.open(uploaded)
            detections, annotated = detector.detect_image(image, confidence=confidence)
            if detector.error:
                st.error(detector.error)
                st.image(image, caption="原始图片", use_container_width=True)
                return
            events = evaluate_events(detections, scene=scene)
            report = build_event_report(events, source_name=uploaded.name)
            append_event_log(LOG_PATH, uploaded.name, events)

            st.image(annotated, caption="YOLO 检测结果", use_container_width=True)
            st.subheader("检测结果")
            st.dataframe(pd.DataFrame(detections), use_container_width=True)
            st.subheader("Agent 告警报告")
            st.code(report, language="text")
            return

        TMP_DIR.mkdir(exist_ok=True)
        video_path = TMP_DIR / uploaded.name
        video_path.write_bytes(uploaded.getbuffer())
        frames = extract_sample_frames(video_path, every_n_frames=int(every_n_frames), max_frames=int(max_frames))
        if not frames:
            st.error("视频中没有读取到可分析帧。")
            return

        frame_events = []
        all_detections = []
        preview_cols = st.columns(min(len(frames), 4))
        for idx, sampled in enumerate(frames):
            detections, annotated = detector.detect_image(sampled.image, confidence=confidence)
            if detector.error:
                st.error(detector.error)
                return
            events = evaluate_events(detections, scene=scene)
            frame_events.append(events)
            for detection in detections:
                all_detections.append({"frame_index": sampled.frame_index, **detection})
            if idx < 4:
                preview_cols[idx].image(annotated, caption=f"帧 {sampled.frame_index}", use_container_width=True)

        merged_events = merge_frame_events(frame_events)
        report = build_event_report(merged_events, source_name=uploaded.name)
        append_event_log(LOG_PATH, uploaded.name, merged_events)

        st.subheader("抽帧检测结果")
        st.dataframe(pd.DataFrame(all_detections), use_container_width=True)
        st.subheader("视频事件汇总报告")
        st.code(report, language="text")


def render_fault_agent() -> None:
    st.header("工业设备故障预测 Agent")
    st.caption("上传传感器 CSV 或使用示例数据，系统根据温度、电流、振动判断故障风险并生成维修建议。")

    uploaded = st.file_uploader("上传 CSV", type=["csv"], key="sensor_csv")
    if uploaded is None:
        frame = sample_sensor_data()
        st.info("当前使用内置示例数据。")
    else:
        frame = pd.read_csv(uploaded)

    st.dataframe(frame, use_container_width=True)
    try:
        analysis = analyze_sensor_frame(frame)
    except ValueError as exc:
        st.error(str(exc))
        return

    report = build_fault_report(analysis)
    metric_cols = st.columns(3)
    metric_cols[0].metric("风险等级", analysis["risk_level"])
    metric_cols[1].metric("风险得分", analysis["score"])
    metric_cols[2].metric("异常原因数", len(analysis["reasons"]))
    st.subheader("Agent 维修建议")
    st.code(report, language="text")


def render_logs() -> None:
    st.header("事件日志")
    logs = read_event_logs(LOG_PATH)
    if not logs:
        st.write("暂无日志。上传图片并完成 YOLO 检测后会自动记录。")
        return
    st.dataframe(pd.DataFrame(logs), use_container_width=True)


st.title("边缘 AI 视频分析与故障预测 Agent")
tabs = st.tabs(["视频分析 Agent", "故障预测 Agent", "事件日志"])
with tabs[0]:
    render_video_agent()
with tabs[1]:
    render_fault_agent()
with tabs[2]:
    render_logs()
