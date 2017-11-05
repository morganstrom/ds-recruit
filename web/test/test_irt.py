import irt
import unittest
import numpy as np

class TestIrtMethods(unittest.TestCase):

    def test_quadrature_points(self):
        theta = irt.quadrature_points(10)
        self.assertEqual(theta[0], -4.)
        self.assertAlmostEqual(theta[5], 0.4444, 4)
        self.assertEqual(theta[9], 4.)

    def test_quadrature_weights(self):
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, 0, 1)
        self.assertAlmostEqual(theta_w[0], 0.00013, 5)
        self.assertAlmostEqual(theta_w[5], 0.36142, 5)
        self.assertAlmostEqual(theta_w[9], 0.00013, 5)

    def test_p_correct(self):
        self.assertEqual(irt.p_correct(0, 1, 0), 0.5)
        self.assertEqual(irt.p_correct(2, 1, 2), 0.5)
        self.assertEqual(irt.p_correct(2, 1, 1), 1. / (1 + np.exp(-1)))

    def test_likelihood(self):
        theta = irt.quadrature_points(10)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])
        L = irt.likelihood(theta, a, b, x)
        self.assertAlmostEqual(L[0], 0.0030369, 5)
        self.assertAlmostEqual(L[5], 0.1178053, 5)
        self.assertAlmostEqual(L[9], 0.0000586, 5)

    def test_eap(self):
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, 0, 1)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])
        L = irt.likelihood(theta, a, b, x)
        theta_hat = irt.eap(theta, L, theta_w)
        self.assertAlmostEqual(theta_hat, -0.2271, 4)

    def test_eap_psd(self):
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, 0, 1)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])
        L = irt.likelihood(theta, a, b, x)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)
        self.assertAlmostEqual(theta_psd, 0.7291, 4)

    def test_successive_responses(self):
        # Step 1
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, 0, 1)
        L = irt.likelihood(theta, 1., -2.155, 1)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)

        # Step 2
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, theta_hat, theta_psd)
        L = irt.likelihood(theta, 1., -0.245, 1)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)

        # Step 3
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, theta_hat, theta_psd)
        L = irt.likelihood(theta, 1., 0.206, 0)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)

        # Step 4
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, theta_hat, theta_psd)
        L = irt.likelihood(theta, 1., 0.984, 0)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)

        # Step 5
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, theta_hat, theta_psd)
        L = irt.likelihood(theta, 1., 1.211, 0)
        theta_hat = irt.eap(theta, L, theta_w)
        theta_psd = irt.eap_psd(theta_hat, theta, L, theta_w)

        self.assertAlmostEqual(theta_hat, -0.23, 2)  # Similar to above, not identical..
        self.assertAlmostEqual(theta_psd, 0.74, 2)   # Similar to above, not identical..





if __name__ == '__main__':
    unittest.main()
