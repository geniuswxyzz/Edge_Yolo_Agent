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

默认权重按监控类型切换：

```text
限制区域人员闯入 -> D:\作业\大模型作业\edge_yolo_agent_project\models\yolov8n.pt
仓库火情监控     -> D:\作业\大模型作业\edge_yolo_agent_project\models\fire_smoke.pt
车间安全帽检查   -> D:\作业\大模型作业\edge_yolo_agent_project\models\safety_helmet.pt
```

仓库不提交 `.pt` 权重文件，`models/` 为空是正常的。选择“限制区域人员闯入”时，程序会让 Ultralytics 在首次真实检测时自动下载 `yolov8n.pt`；选择“仓库火情监控”或“车间安全帽检查”时，需要先放入对应的专用训练权重。如果勾选“手动指定权重路径”，请先把对应 `.pt` 文件放到该路径。

自动下载发生在上传图片或视频并开始 YOLO 检测时，不是在网页刚打开时。下载源是 GitHub 上的 Ultralytics assets；如果当前网络或代理无法连接 GitHub，网页会提示自动下载失败。此时可手动下载 `yolov8n.pt` 并放到上面的限制区域默认路径。
