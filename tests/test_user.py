from tests.test_setup import app, BaseTestCase
import json


class Registstration(BaseTestCase):
    def test_register_new_user_successfully(self):
        """Tests for succesful registration of new users"""
        data = {
            'name': 'name',
            'email': 'email',
            'password': 'password'
        }
        response = self.app.post(
            '/auth/register', data=json.dumps(data), follow_redirects=True,
            headers={'Content-Type': 'application/json'})

        self.assertEqual(201, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('User added successfully', response)

    def test_duplicate_user_fails(self):
        """Tests for duplicate user names """
        response = self.app.post('/auth/register', data=json.dumps(dict(
            name='testuser',
            password='123456',
            email='test@test.com'
        )),
                                 content_type='application/json')
        self.assertIn(
            b'User name already exists.Try again with a different name', response.data)

    def test_register_with_all_credentials(self):
        """Tests for registering with all credentials required"""
        response = self.app.post('/auth/register', data=json.dumps(dict(
            name='robah',
            password='robah'
            )),
                                 content_type='application/json')
        self.assertIn(b'Please provide all the credentials', response.data)


class Login(BaseTestCase):
    def test_successful_login_with_valid_credentials(self):
        """Tests for successful login of users when valid credentials are supplied"""
        response = self.app.post('/auth/login', data=json.dumps({
            'name': 'testuser',
            'password': 'testpass'
            }), follow_redirects=True,
                                 headers={'Content-Type': 'application/json'})
        self.assertIn(b'token', response.data)


    def test_user_does_not_exist_fails(self):
        """Tests for login with a user naame that doesnt exist"""
        response = self.app.post('/auth/login', data=json.dumps({
            'name': 'annette',
            'password': 'testpass'
            }),
                                 content_type='application/json')
        self.assertIn(b'User not available', response.data)

    def test_login_fails_invalid_credentials(self):
        """Tests for user login with invalid credentials"""
        response = self.app.post('/auth/login', data=json.dumps({
            'name': 'rnjane',
            'password': 'rnjane'
             }), 
                                 content_type='application/json')
        self.assertIn('User not available', response.data)


    
