import json
from tests.test_user import BaseTestCase


class TestBucketListItem(BaseTestCase):
    def test_create_new_bucketlist_item(self):
        """Tests for creation of a bucketlistitem successfully"""
        token = self.app.post('/auth/login', data=json.dumps(dict(
            name='testuser',
            password='testpass'
        )),
                              content_type='application/json')

        data = json.loads(token.data.decode())
        user_token = data['token']

        response = self.app.post('/bucketlist/1/items', headers=dict(
            user_token=[user_token]), data=json.dumps(dict(
                description='Sky diving',
            )),
                                content_type='application/json')
        self.assertIn(b"bucketlistitem added successfully", response.data)

