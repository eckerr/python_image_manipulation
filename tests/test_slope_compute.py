"""

  Created by Ed on 1/27/2019
 """
from unittest import TestCase
import numpy as np
from slope_math import slope_compute


class TestSlope(TestCase):
    def test_slope_compute(self):
        test_matrix = np.matrix([[3, 2], [1, 4]])
        slope_result = slope_compute(test_matrix)
        self.assertAlmostEqual(slope_result.all(), np.array([[0.0, 0.0], [0.0, 0.0]]).all(), 'zero array')