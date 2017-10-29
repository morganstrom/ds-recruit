import irt
import unittest
import numpy as np

class TestIrtMethods(unittest.TestCase):

    def test_quadrature_points(self):
        obs = irt.quadrature_points(10)
        exp = np.array([1.33830226e-04,   3.15601632e-03,   3.37736510e-02,
                        1.64010075e-01,   3.61423830e-01,   3.61423830e-01,
                        1.64010075e-01,   3.37736510e-02,   3.15601632e-03,
                        1.33830226e-04])
        self.assertEqual(obs, exp)


