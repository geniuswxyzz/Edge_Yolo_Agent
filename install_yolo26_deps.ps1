$ErrorActionPreference = "Stop"

$python = "D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe"

if (-not (Test-Path $python)) {
    throw "Yolo26 python.exe not found: $python"
}

& $python -m pip install streamlit pytest
& $python -c "import ultralytics, streamlit, pytest, cv2, pandas, numpy, PIL; print('Yolo26 dependencies ready')"
