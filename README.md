# 边缘 AI 视频分析与故障预测 Agent

这是一个满足课程设计选题的基础可演示项目，包含两个部分：

1. **边缘 AI 视频分析智能体**：上传图片或视频，使用 YOLO 检测目标，根据检测结果触发安全事件，并生成中文告警报告。
2. **工业设备故障预测 Agent**：读取传感器时序数据，判断温度、电流、振动异常，输出风险等级、原因解释和维修建议。

## 目录结构

```text
edge_yolo_agent_project/
  app.py
  edge_yolo_agent/
    event_agent.py
    fault_agent.py
    log_store.py
    yolo_detector.py
  data/
    sample_sensor.csv
    safety_knowledge.md
  models/
    .gitkeep
  tests/
  requirements.txt
```

## 运行方法

```bash
cd edge_yolo_agent_project
pip install -r requirements.txt
streamlit run app.py
```

## PyCharm 运行

本项目已提供 PyCharm 友好入口：

```text
main.py
```

在 PyCharm 中打开 `edge_yolo_agent_project`，选择解释器：

```text
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe
```

然后直接运行 `main.py`，或使用运行配置 `Run Edge YOLO Agent`。详细步骤见：

```text
PYCHARM_RUN.md
```

当前机器已发现可用 YOLO 环境：

```powershell
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe
```

该环境包含 `ultralytics`，但未安装 `streamlit`。如果不想改动这个环境，可以用当前有 `streamlit` 的 Python 启动页面，并让 YOLO 检测通过 `EDGE_YOLO_PYTHON` 调用 `Yolo26`：

```powershell
cd "D:\作业\大模型作业\edge_yolo_agent_project"
$env:EDGE_YOLO_PYTHON = "D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe"
python -m streamlit run app.py
```

如果你愿意把 `streamlit` 安装进 `Yolo26`，也可以直接运行：

```powershell
cd "D:\作业\大模型作业\edge_yolo_agent_project"
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe -m pip install streamlit
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe -m streamlit run app.py
```

YOLO 权重默认读取：

```text
models/yolov8n.pt
```

如果本机没有 `ultralytics` 或没有权重文件，页面会给出提示。下载或复制 `yolov8n.pt` 到 `models/` 后即可进行真实 YOLO 检测。

页面支持两类输入：

- 图片：直接检测并生成单张图片告警报告。
- 视频：将视频保存到 `.streamlit_tmp/`，按设定间隔抽帧，逐帧调用 YOLO，最后汇总为视频级事件报告。

## 测试

```bash
cd edge_yolo_agent_project
python -m pytest -q
```

## 命令行演示

无需打开网页，也可以快速展示两个 Agent 的核心输出：

```powershell
cd "D:\作业\大模型作业\edge_yolo_agent_project"
.\run_demo.ps1
```

也可以分别运行：

```powershell
python -m edge_yolo_agent.cli sample-fault
python -m edge_yolo_agent.cli events-from-json data\video_cases\detections_restricted_intrusion.json --scene restricted_area --source restricted_intrusion_demo
python -m edge_yolo_agent.cli events-from-json data\video_cases\detections_fire_risk.json --scene warehouse --source fire_risk_demo
python -m edge_yolo_agent.cli fault-from-csv data\fault_cases\sensor_fault_high.csv
```

## 测试数据

本地测试数据位于：

```text
data/
```

包含：

- `video_cases/detections_restricted_intrusion.json`：限制区域人员闯入，属于视频安全分析。
- `video_cases/detections_fire_risk.json`：烟火风险，属于视频安全分析。
- `video_cases/detections_workshop_no_helmet.json`：车间人员未佩戴安全帽，属于视频安全分析，不属于故障预测。
- `video_cases/detections_normal.json`：无明显异常。
- `fault_cases/sensor_normal.csv`：正常设备运行数据。
- `fault_cases/sensor_warning.csv`：中风险设备数据。
- `fault_cases/sensor_fault_high.csv`：高风险设备故障数据。
- `image_sources.md`：检索到的参考图片来源链接。

这些 JSON 可直接用于 `events-from-json` 命令，CSV 可在 Streamlit 的故障预测页面上传。

当前测试覆盖：

- YOLO 检测结果格式化
- 人员闯入、烟火风险、安全帽缺失等事件规则
- 中文 Agent 告警报告生成
- 工业设备故障风险判断和维修建议生成

## 与选题要求的对应关系

| 选题要求 | 项目实现 |
| --- | --- |
| 视频输入 | Streamlit 上传图片或视频，视频按间隔抽帧分析 |
| 目标检测 | `YoloDetector` 调用 ultralytics YOLO |
| 事件判断 | `evaluate_events` 根据检测结果触发安全事件 |
| Agent 报告生成 | `build_event_report` 生成中文告警报告 |
| 日志展示 | `event_logs.jsonl` 记录并在页面展示 |
| 故障预测 Agent | `fault_agent.py` 分析传感器数据并生成维修建议 |

## 后续可扩展方向

- 将视频抽帧扩展为后台任务，支持长视频进度条和结果缓存。
- 使用自训练安全帽、烟火数据集权重替换通用 YOLO 权重。
- 将 `data/safety_knowledge.md` 接入 RAG，让报告引用安全规范。
- 将事件日志保存到 SQLite，支持按时间、事件类型和风险等级检索。
