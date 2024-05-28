from django.test import TestCase
import numpy as np
import random as rd

from recommenders.models import KNN


class KNNTest(TestCase):
    def setUp(self):
        self.classes = [item for item in range(10)]
        self.x = [[rd.random(), rd.random(), rd.random()] for _ in range(10000)]
        self.y = [rd.randint(0, len(self.classes) - 1) for _ in range(10000)]

    def test_KNN(self):
        model = KNN(k_value=10, dim=3)

        model.fit(np.array(self.x), np.array(self.y))

        res = model.predict(np.array([rd.random(), rd.random(), rd.random()]))

        total_cnt = 0
        for item in res:
            self.assertIn(item[0], self.classes)
            total_cnt += item[1]

        self.assertEqual(total_cnt, len(self.classes))
