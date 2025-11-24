from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Application, ContactMessage, Newsletter, Event
from dotenv import load_dotenv
import os
from datetime import datetime

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./bciai_club.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 初始化数据库
db.init_app(app)

# 数据库初始化将在应用启动时进行


@app.route('/api/apply', methods=['POST'])
def submit_application():
    """处理"加入我们"申请表单提交"""
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['name', 'student_id', 'email', 'phone', 'major', 'position']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} 为必填字段'}), 400
        
        # 处理兴趣方向（列表转字符串）
        interests = ','.join(data.get('interests', [])) if isinstance(data.get('interests'), list) else data.get('interests', '')
        
        # 处理技术技能（列表转字符串）
        skills = ','.join(data.get('skills', [])) if isinstance(data.get('skills'), list) else data.get('skills', '')
        
        # 创建申请记录
        application = Application(
            name=data['name'],
            student_id=data['student_id'],
            email=data['email'],
            phone=data['phone'],
            major=data['major'],
            grade=data.get('grade', ''),
            position=data['position'],
            interests=interests,
            skills=skills,
            team_preference=data.get('team_preference', ''),
            experience=data.get('experience', ''),
            reason=data.get('reason', ''),
            available_time=data.get('available_time', ''),
            github_url=data.get('github_url', ''),
            other_info=data.get('other_info', '')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '申请表提交成功！我们将尽快联系您安排面试。'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交失败：{str(e)}'}), 500


@app.route('/api/applications', methods=['GET'])
def get_applications():
    """获取申请列表（管理员功能）"""
    try:
        # 支持按状态筛选
        status = request.args.get('status')
        query = Application.query
        
        if status:
            query = query.filter_by(status=status)
        
        # 按创建时间降序排列
        applications = query.order_by(Application.created_at.desc()).all()
        
        applications_list = []
        for app in applications:
            applications_list.append({
                'id': app.id,
                'name': app.name,
                'position': app.position,
                'major': app.major,
                'email': app.email,
                'phone': app.phone,
                'status': app.status,
                'interview_status': app.interview_status,
                'created_at': app.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'applications': applications_list}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取申请列表失败：{str(e)}'}), 500


@app.route('/api/applications/<int:application_id>', methods=['GET'])
def get_application_detail(application_id):
    """获取申请详情（管理员功能）"""
    try:
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': '申请不存在'}), 404
        
        return jsonify({
            'id': application.id,
            'name': application.name,
            'student_id': application.student_id,
            'email': application.email,
            'phone': application.phone,
            'major': application.major,
            'grade': application.grade,
            'position': application.position,
            'interests': application.interests.split(',') if application.interests else [],
            'skills': application.skills.split(',') if application.skills else [],
            'team_preference': application.team_preference,
            'experience': application.experience,
            'reason': application.reason,
            'available_time': application.available_time,
            'github_url': application.github_url,
            'other_info': application.other_info,
            'status': application.status,
            'interview_status': application.interview_status,
            'interview_notes': application.interview_notes,
            'created_at': application.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取申请详情失败：{str(e)}'}), 500


@app.route('/api/applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    """更新申请状态（管理员功能）"""
    try:
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': '申请不存在'}), 404
        
        data = request.json
        
        # 更新申请状态
        if 'status' in data:
            application.status = data['status']
        
        # 更新面试状态
        if 'interview_status' in data:
            application.interview_status = data['interview_status']
        
        # 更新面试备注
        if 'interview_notes' in data:
            application.interview_notes = data['interview_notes']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '申请状态更新成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新申请状态失败：{str(e)}'}), 500


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """处理联系表单提交"""
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['contact-name', 'contact-email', 'contact-subject', 'contact-message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} 为必填字段'}), 400
        
        # 创建联系消息记录
        contact = ContactMessage(
            contact_name=data['contact-name'],
            contact_email=data['contact-email'],
            contact_subject=data['contact-subject'],
            contact_message=data['contact-message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '消息发送成功！我们将尽快回复您。'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'发送失败：{str(e)}'}), 500


@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    """处理通讯订阅"""
    try:
        data = request.json
        
        # 验证邮箱
        if not data.get('email'):
            return jsonify({'error': '邮箱地址为必填字段'}), 400
        
        # 检查是否已订阅
        existing = Newsletter.query.filter_by(email=data['email']).first()
        if existing:
            if not existing.is_active:
                # 重新激活
                existing.is_active = True
                existing.subscribed_at = datetime.utcnow()
                db.session.commit()
                return jsonify({'success': True, 'message': '您已成功重新订阅通讯！'}), 200
            else:
                return jsonify({'error': '您已经订阅过通讯了！'}), 400
        
        # 创建新的订阅记录
        newsletter = Newsletter(email=data['email'])
        db.session.add(newsletter)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '订阅成功！您将收到我们的最新动态。'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'订阅失败：{str(e)}'}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """获取活动列表"""
    try:
        events = Event.query.order_by(Event.date).all()
        
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d %H:%M'),
                'location': event.location
            })
        
        return jsonify({'events': events_list}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取活动失败：{str(e)}'}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    try:
        # 获取统计信息
        total_applications = Application.query.count()
        total_contacts = ContactMessage.query.count()
        total_subscribers = Newsletter.query.filter_by(is_active=True).count()
        total_events = Event.query.count()
        
        # 获取申请状态分布
        pending_applications = Application.query.filter_by(status='pending').count()
        approved_applications = Application.query.filter_by(status='approved').count()
        
        # 获取论文统计数据（模拟数据）
        paper_stats = [
            {'year': '2020', 'count': 2},
            {'year': '2021', 'count': 3},
            {'year': '2022', 'count': 4},
            {'year': '2025', 'count': 12}
        ]
        
        # 获取研究领域分布（模拟数据）
        research_areas = [
            {'area': '脑机接口', 'percentage': 35},
            {'area': '人工智能', 'percentage': 25},
            {'area': '神经科学', 'percentage': 20},
            {'area': '医疗应用', 'percentage': 15},
            {'area': '其他', 'percentage': 5}
        ]
        
        return jsonify({
            'total_applications': total_applications,
            'total_contacts': total_contacts,
            'total_subscribers': total_subscribers,
            'total_events': total_events,
            'application_status': {
                'pending': pending_applications,
                'approved': approved_applications,
                'rejected': total_applications - pending_applications - approved_applications
            },
            'paper_stats': paper_stats,
            'research_areas': research_areas
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取统计数据失败：{str(e)}'}), 500


@app.route('/', methods=['GET'])
def index():
    """根路径"""
    return jsonify({'message': 'SAU脑机与人工智能俱乐部后端API服务正在运行！'}), 200


# 主程序入口
if __name__ == '__main__':
    # 确保数据库已创建
    with app.app_context():
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
    
    # 获取端口，默认为5000
    port = int(os.getenv('PORT', 5000))
    print("后端服务启动中...")
    print(f"访问地址: http://localhost:{port}")
    print(f"API文档地址: http://localhost:{port}/api")
    print("按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=port, debug=True)