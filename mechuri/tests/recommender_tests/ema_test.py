from django.test import TestCase

from recommenders.models import EMA


class EMATest(TestCase):
    def setUp(self):
        self.beta = 0.7

    def test_ema_adjusting_first_theta(self):
        model = EMA(self.beta)

        v0 = 0
        t1 = 1
        v1 = model.update(v0, t1, is_t1=True)

        self.assertEquals(v1, t1)

    def test_ema_update(self):
        model = EMA(self.beta)

        v1 = 0
        t2 = 1
        v2 = model.update(v1, t2)

        self.assertEquals(v2, 0.3)  # 0 * 0.7 + 1 * 0.3
