from django.test import TestCase, Client
from django.urls import reverse
from .models import FrontendUser

class FrontendUserModelTests(TestCase):
    def setUp(self):
        # 在使用之前，初始化测试客户端
        self.client = Client()

    def test_register_user_success(self):
        # 模拟发送一个有效的注册请求
        url = reverse('users:register')  # 确保使用适当的 URL 名称
        data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': '123456',
            'gender': 'M',
            'grade': 'G3',
            'desc': 'This is a test user',
        }

        # 发送 POST 请求
        response = self.client.post(url, data, format='json')

        # 断言用户被成功创建
        print(f'用户成功创建返回数据：{response.json()}')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(FrontendUser.objects.filter(username=data['username']).exists())


    def test_register_user_missing_field(self):
        # 模拟发送一个缺少字段的请求
        url = reverse('users:register')
        data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            # 密码缺失
            'gender': 'M',
        }

        response = self.client.post(url, data, format='json')
        # 断言返回 400 错误
        self.assertEqual(response.status_code, 400)
        print(f'密码缺失返回错误：{response.json()}')

    def test_register_user_duplicate(self):
        # 首先注册一个用户
        self.client.post(reverse('users:register'), {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': '123456',
            'gender': 'M',
            'grade': 'G3'
        })

        # 尝试注册相同的用户
        response = self.client.post(reverse('users:register'), {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': '123456',
            'gender': 'M',
            'grade': 'G3'
        })

        # 检查返回的状态码
        self.assertEqual(response.status_code, 400)
        print(f'相同用户返回错误：{response.json()}')

    def test_login_user_success(self):
        # 模拟发送一个有效的注册请求
        url = reverse('users:register')  # 确保使用适当的 URL 名称
        data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': '123456',
            'gender': 'M',
            'grade': 'G3',
            'desc': 'This is a test user',
        }

        # 发送 POST 请求
        response = self.client.post(url, data, format='json')
        # 模拟登录这个账号
        url = reverse('users:login')
        data = {
            'username': 'TestUser',
            'password': '123456',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_refresh_token_success(self):
        # 模拟发送一个有效的注册请求
        url = reverse('users:register')  # 确保使用适当的 URL 名称
        data = {
            'username': 'TestUser',
            'email': 'testuser@example.com',
            'password': '123456',
            'gender': 'M',
            'grade': 'G3',
            'desc': 'This is a test user',
        }

        # 发送 POST 请求
        response = self.client.post(url, data, format='json')
        refresh_token = response.json().get('refresh_token')
        url = reverse('users:token_refresh')
        data2 = {
            'refresh': refresh_token,
        }
        response = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, 200)
        print(response.json())

