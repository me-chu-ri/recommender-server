from django.test import TestCase
import numpy as np
import random as rd

from recommenders.models import EASEr


class EASErTest(TestCase):
    def setUp(self):
        users = 10000
        items = 500

        self.datas: np.ndarray = np.zeros((users, items))
        for i in range(users):
            rng = rd.randint(20, 30)
            indices = [rd.randint(0, items - 1) for _ in range(rng)]
            for j in indices:
                self.datas[i][j] = rd.random()

    def test_EASEr(self):
        model = EASEr()

        model.fit(self.datas)
        res = model.predict(self.datas[0])

        self.assertEquals(res.shape, (self.datas.shape[1],))
