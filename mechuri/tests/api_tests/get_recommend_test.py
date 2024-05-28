import json

from django.test import TestCase, Client


client = Client()


class GetRecommendTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_recommend(self):
        # client.get('/api/endpoint', data=json.dumps({'data': 'aa'}), content_type='application/json')
        pass
