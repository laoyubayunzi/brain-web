import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 打印环境变量信息
print("===== 环境变量测试 =====")
database_url = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {database_url}")
print(f"类型: {type(database_url)}")

# 检查默认值
if database_url is None:
    database_url = 'sqlite:///./bciai_club.db'
    print("使用默认数据库URL")

# 验证DATABASE_URL格式
print("\n===== DATABASE_URL格式验证 =====")
print(f"格式是否正确: {'sqlite:///' in database_url}")
print(f"数据库文件: {database_url.split('///')[-1] if '///' in database_url else '未知'}")

# 正确的格式示例
print("\n===== 正确的DATABASE_URL格式示例 =====")
print("SQLite格式:")
print("1. sqlite:///./bciai_club.db  (相对路径，当前目录)")
print("2. sqlite:///bciai_club.db   (Flask默认会放在instance目录)")
print("3. sqlite:///C:/path/to/bciai_club.db  (绝对路径)")
