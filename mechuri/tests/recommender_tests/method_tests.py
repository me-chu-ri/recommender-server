from django.test import TestCase
import numpy as np

from recommenders.methods import Normalizers, L1Norm, L2Norm
from recommenders.ensembles import Ensembler


class MethodTests(TestCase):
    def setUp(self):
        self.datas = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        pass

    def test_min_max_normalizers(self):
        res = Normalizers.min_max_normalization(self.datas)

        for item in res:
            self.assertGreaterEqual(item, 0)
            self.assertLessEqual(item, 1)

    def test_min_max_specified_normalizers(self):
        res = Normalizers.min_max_specified_normalization(self.datas, -10, 10)

        for item in res:
            self.assertGreaterEqual(item, 0)
            self.assertLessEqual(item, 1)

    def test_standardizer(self):
        res = Normalizers.standardize(self.datas)

        self.assertAlmostEqual(res.mean(), 0)

    def test_l1_norm(self):
        res = L1Norm().execute(np.array(self.datas), np.array(self.datas + 1))

        self.assertEqual(res, 10)

    def test_l2_norm(self):
        res = L2Norm().execute(np.array(self.datas), np.array(self.datas + 1))

        self.assertEqual(res, np.sqrt(len(self.datas)))

    def test_basic_ensembler(self):
        res = Ensembler.basic(np.array([0.9, 0.3]))

        self.assertEqual(res, 0.27)

    def test_weighted_ensembler(self):
        res = Ensembler.weighted_sum(np.array([0.9, 0.3]), np.array([0.7, 0.3]))

        self.assertEqual(res, 0.72)  # 0.9 * 0.7 + 0.3 * 0.3
