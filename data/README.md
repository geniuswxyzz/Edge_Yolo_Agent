# 数据目录说明

本目录按 Agent 功能拆分数据，避免把视频安全事件和设备故障预测混在一起。

## `video_cases/`

用于边缘 AI 视频分析智能体。JSON 文件模拟 YOLO 检测输出，适合在没有真实图片/权重时演示事件规则和 Agent 报告。

- `detections_restricted_intrusion.json`：限制区域人员闯入。
- `detections_fire_risk.json`：仓库烟火风险。
- `detections_workshop_no_helmet.json`：车间人员未佩戴安全帽。该文件属于视频安全分析，不属于设备故障预测。
- `detections_normal.json`：未发现明显异常。

## `fault_cases/`

用于工业设备故障预测 Agent。CSV 字段严格对应当前故障 Agent 的输入：`timestamp`、`temperature`、`current`、`vibration`。

- `sensor_normal.csv`：正常工况。
- `sensor_warning.csv`：温度持续偏高，中风险。
- `sensor_fault_high.csv`：温度、振动和电流均异常，高风险。

## `image_sources.md`

记录已检索到的参考图片来源。可用于报告配图或后续手动下载，但不作为程序测试依赖。
