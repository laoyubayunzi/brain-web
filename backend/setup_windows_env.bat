@echo off
REM SAU脑机与人工智能俱乐部网站 - Windows环境设置脚本
REM 此脚本用于在Windows系统上设置开发/测试环境

echo ====================================
echo SAU脑机与人工智能俱乐部网站Windows环境设置
echo ====================================

REM 检查Python是否已安装
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误：未找到Python。请先安装Python 3.8或更高版本。
    echo 您可以从 https://www.python.org/downloads/ 下载
    pause
    exit /b 1
)

REM 检查pip是否可用
pip --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误：未找到pip。请确保Python安装时已包含pip。
    pause
    exit /b 1
)

REM 升级pip
echo 升级pip...
pip install --upgrade pip

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt

REM 创建必要的目录
if not exist "instance" (
    echo 创建数据库目录...
    mkdir instance
)

REM 创建示例环境变量文件
if not exist ".env" (
    echo 创建环境变量文件...
    echo # 数据库配置 > .env
    echo DATABASE_URL=sqlite:///./instance/bciai_club.db >> .env
    echo. >> .env
    echo # 应用密钥 >> .env
    echo SECRET_KEY=your-secret-key-change-this-in-production >> .env
    echo. >> .env
    echo # 服务器端口 >> .env
    echo PORT=8000 >> .env
)

echo ====================================
echo Windows环境设置完成！
echo ====================================
echo 已完成的操作：
echo - 升级了pip
echo - 创建/使用了虚拟环境
echo - 安装了所有必要的依赖
echo - 创建了数据库目录
echo - 创建了示例.env配置文件
echo. 
echo 如何运行应用：
echo 1. 确保已激活虚拟环境
call echo    ^> %cd%\venv\Scripts\activate
call echo    ^> python production_start.py
call echo. 
echo 2. 或者使用批处理文件启动（如果创建了的话）
echo    ^> start_server.bat
echo. 
echo 注意：在生产环境中，请确保修改.env文件中的SECRET_KEY为安全的随机字符串。
echo ====================================

REM 保持窗口打开
pause
