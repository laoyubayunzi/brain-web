import os
import subprocess
import sys
import time

def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False

def run_migrations():
    """运行数据库迁移"""
    print("初始化数据库...")
    try:
        # 创建一个临时Python脚本来初始化数据库
        with open("init_db.py", "w") as f:
            f.write("""
import os
from app import app, db
from models import Application, ContactMessage, Newsletter, Event

with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 添加一些示例活动数据
    if Event.query.count() == 0:
        events = [
            Event(
                title="脑电信号处理工作坊",
                date="2024-06-15",
                location="创新实验室A区",
                description="学习脑电信号采集、预处理和特征提取的实用技巧，适合初学者和进阶研究者。"
            ),
            Event(
                title="项目成果展示会",
                date="2024-07-20",
                location="学术报告大厅",
                description="展示我们的最新研究成果和项目进展，包括脑机接口控制的智能家居系统等。"
            ),
            Event(
                title="人工智能在神经科学中的应用讲座",
                date="2024-08-10",
                location="线上直播",
                description="邀请专家讲解深度学习和机器学习在神经科学研究中的前沿应用。"
            )
        ]
        for event in events:
            db.session.add(event)
        db.session.commit()
        print("示例活动数据添加成功！")
    
    print("数据库初始化完成！")
        """)
        
        subprocess.check_call([sys.executable, "init_db.py"])
        os.remove("init_db.py")  # 删除临时文件
        print("数据库迁移完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"数据库初始化失败: {e}")
        return False

def start_server():
    """启动Flask服务器"""
    print("正在启动Flask服务器...")
    print("服务器将在 http://localhost:5000 上运行")
    print("按 Ctrl+C 停止服务器")
    
    try:
        # 设置环境变量
        os.environ["FLASK_APP"] = "app.py"
        os.environ["FLASK_ENV"] = "development"
        
        # 启动Flask服务器
        subprocess.run([sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"])
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

if __name__ == "__main__":
    print("===== SAU脑机与人工智能俱乐部后端服务 =====")
    
    # 检查并创建虚拟环境（如果不存在）
    if not os.path.exists("venv"):
        print("未找到虚拟环境，正在创建...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("虚拟环境创建成功！")
            # 重新使用虚拟环境中的Python
            if sys.platform.startswith("win"):
                venv_python = os.path.join("venv", "Scripts", "python.exe")
            else:
                venv_python = os.path.join("venv", "bin", "python")
            
            # 重新执行当前脚本使用虚拟环境
            subprocess.run([venv_python, __file__])
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"虚拟环境创建失败: {e}")
            print("将继续使用当前Python环境...")
    
    # 安装依赖
    if not install_dependencies():
        print("警告：依赖安装失败，可能会影响服务运行")
    
    # 初始化数据库
    run_migrations()
    
    # 启动服务器
    start_server()