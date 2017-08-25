import unittest
import context
from app.models import User, Bucketlist
from app import app, db
import json
from app import config

class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        db.session.close()
        db.drop_all()
        db.create_all()
        user = User('test', 'testpass','test@gmail.com')
        db.session.add(user)
        db.session.commit()
        self.app = app.test_client()
        self.user = user
        return self.app, self.user

    def registration(self, email, password, name):
        return self.app.post('/auth/register', data=dict(
    email=email,
    password=password,
    name=name
        ))

    def test_register_new_user(self):
        rv = self.registration('test', 'test@gmail.com', '1234')
        data = json.loads(rv.data.decode())
        self.assertEqual('user added succesfully', data['message'])

    def login(self, email, password):
        return self.app.post('/auth/login', data=dict(
            email=email,
            password=password
        ))
    def test_login(self):
        rv = self.login('test', 'testpass')
        data = json.loads(rv.data.decode())
        self.assertEqual('You have successfully logged in', data['message'])