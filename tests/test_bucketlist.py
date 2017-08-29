import json
from tests.test_user import BaseTestCase


class Bucketlist(BaseTestCase):
    def test_creates_new_bucketlist_with_valid_token(self):
        """Tests for new bucketlists successfully created when a valid token is used"""
        token = self.app.post('/auth/login', data=json.dumps(dict(
            name='testuser',
            password='testpass'
        )),
                              content_type='application/json')

        data = json.loads(token.data.decode())
        user_token = data['token']

        testadd = self.app.post('/bucketlist', headers=dict(
            user_token=[user_token]), data=json.dumps(dict(
                name='World Tour',
                owner_id=1
            )),
                                content_type='application/json')
        self.assertIn(b"bucketlist added successfully", testadd.data)

    def test_gets_bucketlist_for_the_user(self):
        """
        Tests that names of bucketlists for a certain user are fetched
        """
        token = self.app.post('/auth/login', data=json.dumps(dict(
            name='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        user_token = data['token']
        response = self.app.get('/bucketlist/1', headers=dict(
            user_token=[user_token]))

        self.assertIn(b"testbucket", response.data)
    def test_error_on_bucketlist_creation_with_invalid_token(self):
        """ Tests for creation of bucketlists with invalid tokens"""
        data = {
            'name': 'World Tour'
        }
        response = self.app.post(
            '/bucketlist', data=json.dumps(data),
            headers=dict(user_token="wrongtoken"))
        self.assertIn('Token is invalid', response.data)

    def test_error_on_bucketlist_creation_with_missing_token(self):
        """ Tests for creation of bucketlists without  tokens"""
        data = {
            'name': 'World Tour'
        }
        response = self.app.post(
            '/bucketlist', data=json.dumps(data))
        self.assertIn('Token is missing', response.data)

    def test_delete_bucketlist__successfully(self):
        """Tests for deletion of bucketlist successfully"""
        token = self.app.post('/auth/login', data=json.dumps(dict(
            name='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        user_token = data['token']

        response = self.app.delete('/bucketlist/1', headers=dict(
            user_token=[user_token]))
        self.assertIn(b'You have deleted a bucketlist successfully', response.data)
    


    
