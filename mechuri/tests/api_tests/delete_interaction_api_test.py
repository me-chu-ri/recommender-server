from django.test import TestCase, Client
import json


client = Client()


class DeleteInteractionAPITest(TestCase):
    def setUp(self):
        self.request_data = {
            'targetId': 'uuid'
        }

        self.response_data = {
            'succeed': True
        }

    def test_personal_delete(self):
        res = client.post('/model/v1/menu/personal', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)

    def test_group_delete(self):
        res = client.post('/model/v1/menu/group', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)
