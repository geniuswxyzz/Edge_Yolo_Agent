$ErrorActionPreference = "Stop"

Write-Host "== Fault Agent Demo =="
python -m edge_yolo_agent.cli sample-fault

Write-Host ""
Write-Host "== Event Agent Demo =="
python -m edge_yolo_agent.cli events-from-json data\video_cases\detections_restricted_intrusion.json --scene restricted_area --source restricted_intrusion_demo

Write-Host ""
Write-Host "== Fire Risk Demo =="
python -m edge_yolo_agent.cli events-from-json data\video_cases\detections_fire_risk.json --scene warehouse --source fire_risk_demo

Write-Host ""
Write-Host "== Fault CSV Demo =="
python -m edge_yolo_agent.cli fault-from-csv data\fault_cases\sensor_fault_high.csv

Write-Host ""
Write-Host "== Streamlit Run Command =="
Write-Host '$env:EDGE_YOLO_PYTHON = "D:\WorkSoftware\Anaconda3\envs\Yolo26\python.exe"'
Write-Host 'python -m streamlit run app.py'
