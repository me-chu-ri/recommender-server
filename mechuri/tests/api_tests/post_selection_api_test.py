from django.test import TestCase, Client
import json


client = Client()


class PostSelectionAPITest(TestCase):
    def setUp(self):
        self.request_data = {
            'targetId': 'uuid',
            'menuId': 'id',
            'weather': {
                'temp': 15.4,
                'precip': 20,
                'humid': 30
            },
            'location': {
                'lat': 37.255432,
                'long': 127.23562
            }
        }

        self.response_data = {
            'succeed': True
        }

    def test_personal_selection(self):
        res = client.post('/model/v1/menu/select/personal', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)

    def test_group_selection(self):
        res = client.post('/model/v1/menu/select/group', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)
