@echo off
cls
echo 正在启动SAU脑机与人工智能俱乐部后端服务...
echo 使用Python内置HTTP服务器，端口8000
echo. 
echo 服务将在以下地址运行：
echo http://localhost:8000
echo http://localhost:8000/api/test
echo.
echo 按 Ctrl+C 停止服务

python simple_http_server.py
