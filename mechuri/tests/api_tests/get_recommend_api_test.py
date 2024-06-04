from django.test import TestCase, Client
import json


client = Client()


class GetRecommendAPITest(TestCase):
    def setUp(self):
        self.request_data = {
            "targetId": 'uuid',
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
            'probability': 34.4,
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

    def test_personal_recommend(self):
        res = client.get('/model/v1/menu/personal', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)

    def test_group_recommend(self):
        res = client.get('/model/v1/menu/group', data=json.dumps(self.request_data), content_type='application/json')
        self.assertEqual(res, self.response_data)
