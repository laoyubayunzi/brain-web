from flask import Flask
from models import db, Application
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./bciai_club.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 测试数据库连接
with app.app_context():
    try:
        # 检查数据库连接
        db.create_all()
        print("✅ 数据库连接成功！DATABASE_URL配置正确。")
        print(f"当前数据库URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"数据库类型: SQLite")
        print(f"数据库文件位置: ./bciai_club.db (实际存储在instance目录下)")
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
