# PyCharm 运行说明

## 1. 打开项目

在 PyCharm 中打开目录：

```text
D:\作业\大模型作业\edge_yolo_agent_project
```

## 2. 选择解释器

推荐选择已有的 YOLO 环境：

```text
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe
```

该环境已确认包含 `ultralytics`、`opencv-python`、`pandas`、`numpy` 和 `Pillow`。

## 3. 安装缺失依赖

如果 PyCharm 运行时报 `No module named streamlit` 或 `No module named pytest`，在 PyCharm Terminal 中运行：

```powershell
.\install_yolo26_deps.ps1
```

等价命令：

```powershell
D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe -m pip install streamlit pytest
```

## 4. 运行方式

方式一：直接运行根目录下的：

```text
main.py
```

方式二：使用 PyCharm 右上角运行配置：

```text
Run Edge YOLO Agent
```

运行后访问：

```text
http://localhost:8501
```

## 5. YOLO 权重

默认权重路径：

```text
D:\作业\大模型作业\edge_yolo_agent_project\models\yolov8n.pt
```

把权重文件放入该目录后，图片和视频检测会调用真实 YOLO。
