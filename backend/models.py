from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库实例
db = SQLAlchemy()


class Application(db.Model):
    """申请表模型 - 用于"加入我们"功能"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20), nullable=True)  # 年级
    position = db.Column(db.String(100), nullable=False)  # 申请职位
    interests = db.Column(db.String(200), nullable=True)  # 存储为逗号分隔的字符串
    skills = db.Column(db.String(300), nullable=True)  # 技术技能，存储为逗号分隔的字符串
    team_preference = db.Column(db.String(100), nullable=True)  # 团队偏好
    experience = db.Column(db.Text, nullable=True)
    reason = db.Column(db.Text, nullable=True)
    available_time = db.Column(db.Text, nullable=True)  # 可参与时间
    github_url = db.Column(db.String(200), nullable=True)  # GitHub链接
    other_info = db.Column(db.Text, nullable=True)  # 其他信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    interview_status = db.Column(db.String(20), default='not_scheduled')  # 面试状态：not_scheduled, scheduled, completed
    interview_notes = db.Column(db.Text, nullable=True)  # 面试备注

    def __repr__(self):
        return f'<Application {self.name} - {self.position}>'


class ContactMessage(db.Model):
    """联系消息模型"""
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_subject = db.Column(db.String(200), nullable=False)
    contact_message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage {self.contact_subject}>'


class Newsletter(db.Model):
    """订阅通讯模型"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Newsletter {self.email}>'


class Event(db.Model):
    """活动模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.title}>'