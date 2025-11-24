from app import app
import unittest
import json
from models import db, Application

class ApplicationTestCase(unittest.TestCase):
    """测试"加入我们"功能的API端点"""

    def setUp(self):
        """设置测试环境"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
        self.client = app.test_client()
        
        # 创建测试数据库
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """清理测试环境"""
        with app.app_context():
            db.drop_all()
    
    def test_submit_application(self):
        """测试提交申请表单"""
        # 准备测试数据
        test_data = {
            'name': '张三',
            'student_id': '2021001',
            'email': 'zhangsan@example.com',
            'phone': '13800138000',
            'major': '计算机科学与技术',
            'grade': '大三',
            'position': '开发工程师',
            'interests': ['脑机接口', '人工智能'],
            'skills': ['Python', 'Flask', 'SQL'],
            'team_preference': '算法组',
            'experience': '曾参与过机器学习相关项目',
            'reason': '对脑机接口技术很感兴趣',
            'available_time': '周一至周五晚上，周末全天',
            'github_url': 'https://github.com/zhangsan',
            'other_info': '有一定的项目经验'
        }
        
        # 发送POST请求
        response = self.client.post(
            '/api/apply',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # 验证响应
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['success'], True)
        self.assertIn('申请表提交成功', response.json['message'])
        
        # 验证数据库中是否有数据
        with app.app_context():
            application = Application.query.first()
            self.assertIsNotNone(application)
            self.assertEqual(application.name, '张三')
            self.assertEqual(application.position, '开发工程师')
            self.assertEqual(application.status, 'pending')
    
    def test_submit_application_missing_required_fields(self):
        """测试缺少必填字段的情况"""
        # 缺少position字段
        test_data = {
            'name': '李四',
            'student_id': '2021002',
            'email': 'lisi@example.com',
            'phone': '13900139000',
            'major': '电子工程'
        }
        
        # 发送POST请求
        response = self.client.post(
            '/api/apply',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # 验证响应
        self.assertEqual(response.status_code, 400)
        self.assertIn('position 为必填字段', response.json['error'])
    
    def test_get_applications(self):
        """测试获取申请列表"""
        # 先添加测试数据
        with app.app_context():
            # 添加两条不同状态的申请
            app1 = Application(
                name='王五',
                student_id='2021003',
                email='wangwu@example.com',
                phone='13700137000',
                major='软件工程',
                position='UI设计师',
                status='pending'
            )
            app2 = Application(
                name='赵六',
                student_id='2021004',
                email='zhaoliu@example.com',
                phone='13600136000',
                major='数据科学',
                position='算法工程师',
                status='approved'
            )
            db.session.add_all([app1, app2])
            db.session.commit()
        
        # 获取所有申请
        response = self.client.get('/api/applications')
        self.assertEqual(response.status_code, 200)
        applications = response.json['applications']
        self.assertEqual(len(applications), 2)
        
        # 按状态筛选
        response = self.client.get('/api/applications?status=pending')
        self.assertEqual(response.status_code, 200)
        pending_applications = response.json['applications']
        self.assertEqual(len(pending_applications), 1)
        self.assertEqual(pending_applications[0]['status'], 'pending')
    
    def test_get_application_detail(self):
        """测试获取申请详情"""
        # 先添加测试数据
        with app.app_context():
            application = Application(
                name='孙七',
                student_id='2021005',
                email='sunqi@example.com',
                phone='13500135000',
                major='计算机科学',
                grade='大四',
                position='前端工程师',
                interests='前端开发,React,Vue',
                skills='JavaScript,HTML,CSS,React',
                status='pending'
            )
            db.session.add(application)
            db.session.commit()
            app_id = application.id
        
        # 获取详情
        response = self.client.get(f'/api/applications/{app_id}')
        self.assertEqual(response.status_code, 200)
        app_data = response.json
        self.assertEqual(app_data['name'], '孙七')
        self.assertEqual(app_data['position'], '前端工程师')
        self.assertIsInstance(app_data['interests'], list)
        self.assertIsInstance(app_data['skills'], list)
    
    def test_update_application(self):
        """测试更新申请状态"""
        # 先添加测试数据
        with app.app_context():
            application = Application(
                name='周八',
                student_id='2021006',
                email='zhouba@example.com',
                phone='13400134000',
                major='电子信息工程',
                position='后端工程师',
                status='pending'
            )
            db.session.add(application)
            db.session.commit()
            app_id = application.id
        
        # 更新状态
        update_data = {
            'status': 'approved',
            'interview_status': 'completed',
            'interview_notes': '面试表现优秀，技术基础扎实'
        }
        
        response = self.client.put(
            f'/api/applications/{app_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        
        # 验证数据库中的更新
        with app.app_context():
            updated_app = Application.query.get(app_id)
            self.assertEqual(updated_app.status, 'approved')
            self.assertEqual(updated_app.interview_status, 'completed')
            self.assertEqual(updated_app.interview_notes, '面试表现优秀，技术基础扎实')

if __name__ == '__main__':
    unittest.main()