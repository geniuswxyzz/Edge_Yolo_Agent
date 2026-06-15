from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {"temperature", "current", "vibration"}


def analyze_sensor_frame(frame: pd.DataFrame) -> dict:
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"传感器数据缺少字段：{', '.join(sorted(missing))}")

    score = 0
    reasons: list[str] = []
    advice: list[str] = []

    if frame["temperature"].tail(3).mean() >= 75:
        score += 35
        reasons.append("温度持续偏高")
        advice.append("检查散热系统、轴承润滑和环境通风情况")

    if frame["vibration"].max() >= 3.5:
        score += 35
        reasons.append("振动异常")
        advice.append("检查轴承磨损、转子偏心和固定螺栓松动")

    if frame["current"].max() - frame["current"].min() >= 2.0:
        score += 25
        reasons.append("电流波动偏大")
        advice.append("检查负载变化和接线端子状态")

    if not reasons:
        reasons.append("设备运行指标处于正常范围")
        advice.append("按计划巡检，保持当前维护周期")

    risk_level = "low"
    if score >= 60:
        risk_level = "high"
    elif score >= 30:
        risk_level = "medium"

    return {
        "risk_level": risk_level,
        "score": score,
        "reasons": reasons,
        "advice": advice,
    }


def build_fault_report(analysis: dict) -> str:
    reasons = "；".join(analysis["reasons"])
    advice = "；".join(analysis["advice"])
    return (
        "工业设备故障预测 Agent 报告\n"
        f"风险等级：{analysis['risk_level']}\n"
        f"风险得分：{analysis['score']}\n"
        f"异常原因：{reasons}\n"
        f"维护建议：{advice}"
    )


def sample_sensor_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": [
                "2026-06-13 10:00",
                "2026-06-13 10:01",
                "2026-06-13 10:02",
                "2026-06-13 10:03",
                "2026-06-13 10:04",
            ],
            "temperature": [55.0, 64.0, 76.0, 82.0, 86.0],
            "current": [6.2, 6.9, 8.1, 9.0, 9.5],
            "vibration": [1.2, 1.8, 2.9, 3.7, 4.2],
        }
    )

