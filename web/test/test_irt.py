import irt
import unittest
import numpy as np


class TestIrtMethods(unittest.TestCase):

    def test_quadrature_points(self):
        theta = irt.quadrature_points(10)

        self.assertEqual(theta[0], -4.)
        self.assertAlmostEqual(theta[1], -3.1111, 4)
        self.assertAlmostEqual(theta[2], -2.2222, 4)
        self.assertAlmostEqual(theta[3], -1.3333, 4)
        self.assertAlmostEqual(theta[4], -0.4444, 4)
        self.assertAlmostEqual(theta[5], 0.4444, 4)
        self.assertAlmostEqual(theta[6], 1.3333, 4)
        self.assertAlmostEqual(theta[7], 2.2222, 4)
        self.assertAlmostEqual(theta[8], 3.1111, 4)
        self.assertEqual(theta[9], 4.)

    def test_quadrature_weights(self):
        theta = irt.quadrature_points(10)
        theta_w = irt.quadrature_weights(theta, 0, 1)
        prior = irt.normalize_pmf(theta_w)

        self.assertAlmostEqual(prior[0], 0.00012, 4)
        self.assertAlmostEqual(prior[1], 0.00281, 4)
        self.assertAlmostEqual(prior[2], 0.03002, 4)
        self.assertAlmostEqual(prior[3], 0.14580, 4)
        self.assertAlmostEqual(prior[4], 0.32130, 4)
        self.assertAlmostEqual(prior[5], 0.32130, 4)
        self.assertAlmostEqual(prior[6], 0.14580, 4)
        self.assertAlmostEqual(prior[7], 0.03002, 4)
        self.assertAlmostEqual(prior[8], 0.00281, 4)
        self.assertAlmostEqual(prior[9], 0.00012, 4)

    def test_p_correct(self):
        self.assertEqual(irt.p_correct(0, 1, 0), 0.5)
        self.assertEqual(irt.p_correct(2, 1, 2), 0.5)
        self.assertEqual(irt.p_correct(2, 1, 1), 1. / (1 + np.exp(-1)))

    def test_likelihood(self):
        theta = irt.quadrature_points(10)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])
        like = irt.likelihood(theta, a, b, x)

        self.assertAlmostEqual(like[0], 0.0030369, 4)
        self.assertAlmostEqual(like[1], 0.0140101, 4)
        self.assertAlmostEqual(like[2], 0.0502904, 4)
        self.assertAlmostEqual(like[3], 0.1216368, 4)
        self.assertAlmostEqual(like[4], 0.1697289, 4)
        self.assertAlmostEqual(like[5], 0.1178053, 4)
        self.assertAlmostEqual(like[6], 0.0382276, 4)
        self.assertAlmostEqual(like[7], 0.0064165, 4)
        self.assertAlmostEqual(like[8], 0.0006914, 4)
        self.assertAlmostEqual(like[9], 0.0000586, 4)


    def test_eap_psd(self):
        theta = irt.quadrature_points(10)
        prior = irt.quadrature_weights(theta, 0, 1)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])
        like = irt.likelihood(theta, a, b, x)
        theta_hat = irt.eap(theta, like, prior)
        theta_psd = irt.eap_psd(theta_hat, theta, like, prior)

        self.assertAlmostEqual(theta_hat, -0.2271, 4)
        self.assertAlmostEqual(theta_psd, 0.7291, 4)

    def test_successive_estimation(self):
        theta = irt.quadrature_points(10)
        prior = irt.quadrature_weights(theta, 0, 1)
        a = np.repeat(1.0, 5)
        b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
        x = np.array([1, 1, 0, 0, 0])

        for i in range(5):
            like = irt.likelihood(theta, a[i], b[i], x[i])
            theta_hat = irt.eap(theta, like, prior)
            theta_psd = irt.eap_psd(theta_hat, theta, like, prior)
            # print("Iteration " + str(i) + " EAP: " + str(theta_hat))
            # print("Iteration " + str(i) + " PSD: " + str(theta_psd))
            # posterior = irt.quadrature_weights(theta, theta_hat, theta_psd)
            posterior = prior * like
            prior = irt.normalize_pmf(posterior)

        self.assertAlmostEqual(theta_hat, -0.2271, 4)
        self.assertAlmostEqual(theta_psd, 0.7291, 4)


if __name__ == '__main__':
    unittest.main()
