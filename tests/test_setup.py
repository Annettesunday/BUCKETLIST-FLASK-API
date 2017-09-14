import unittest
from app import app, db, config
from app.models import User, Bucketlist, BucketlistItem
from werkzeug.security import generate_password_hash


class BaseTestCase(unittest.TestCase):
    """Tests for setup"""
    def setUp(self):
        """sets up moc data for tests"""
        self.app = app.test_client()
        app.config.from_object(config.TestingConfig)
        db.create_all()
        db.session.add(User(name='testuser', email='testuser@testuser.com', password=generate_password_hash(
            'testpass', method='sha256')))
        db.session.add(Bucketlist(name='testbucket', owner_id=1))
        db.session.add(Bucketlist(name='testbucket2', owner_id=1))
        db.session.add(BucketlistItem(description='itemname', bucketlist_id=2))
        db.session.commit()


    def tearDown(self):
        """Clears all data upon tests completion"""
        db.session.remove()
        db.drop_all()


class TokenTests(BaseTestCase):
    """Tests for token"""
    def test_invalidtoken_fails(self):
        '''Invalid token does not work'''
        response = self.app.get('/bucketlist/', headers=dict(
        user_token=['wrongtoken']))
        self.assertIn('Token is invalid', response.data)

    def test_tokenmissing_fails(self):
        """Token missing fails"""
        response = self.app.get('/bucketlist/')
        self.assertIn('Token is missing', response.data)

if __name__ == '__main__':
    unittest.main()