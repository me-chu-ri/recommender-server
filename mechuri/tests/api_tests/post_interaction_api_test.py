from django.test import TestCase, Client
import json


client = Client()


class PostInteractionAPITest(TestCase):
    def setUp(self):
        self.request_data = {
            'targetId': 'uuid',
            'menuId': 'id',
            'rating': 1,
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
            'possibility': 34.4,
            'menu': {
                'name': '초밥',
                'nutrient': {
                    'energy': 134.0,
                    'cabs': 14.4,
                    'prot': 4.3,
                    'fat': 23.6,
                    'sug': 13.1,
                    'nat': 31.2
                }
            }
        }

    def test_personal_interaction(self):
        res = client.post('/model/v1/menu/personal', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)

    def test_group_interaction(self):
        res = client.post('/model/v1/menu/group', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)
