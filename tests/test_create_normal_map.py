"""

  Created by Ed on 1/22/2019
 """
from unittest import TestCase
import numpy as np


from create_normal_map import read_image_to_gray
from create_normal_map import convert_array_to_float
from create_normal_map import normalize_float_array
from create_normal_map import array_to_prev_next
from create_normal_map import calculate_prev_next_slopes
from create_normal_map import calculate_slope_at_points
from create_normal_map import create_BGR_panels
from create_normal_map import normalize_unit_vectors
from create_normal_map import convert_to_image
from create_normal_map import display_grayscales
from create_normal_map import build_normal_image
from create_normal_map import display_normal_image


class TestNormal(TestCase):
    def test_read_image_to_gray(self):
        filename = 'brick.jpg'
        img = read_image_to_gray(filename)
        self.assertEqual(len(img.shape), 2, 'should only be one channel')

    def test_convert_array_to_float(self):
        test_array = np.array([[10, 20, 30, 40, 50], [20, 30, 40, 50, 60], [30, 40, 50, 60, 70], [70, 60, 50, 40, 30],
                               [60, 50, 40, 20, 30]], dtype=np.uint8)
        expected_dtype = np.dtype('float64')
        float_array = convert_array_to_float(test_array)
        self.assertEqual(float_array.dtype, expected_dtype, 'array type should be float')

    def test_normalize_float_array(self):
        small_test_array = np.array([[0, 255], [128, 128]], dtype=np.float64)
        normalized_array = normalize_float_array(small_test_array)
        expected_array = np.array([[0., 1.], [0.50196078, 0.50196078]])
        self.assertAlmostEqual(normalized_array[0, 0], 0.0, 1, 'should be 0')
        self.assertAlmostEqual(normalized_array[0, 1], 1.0, 1, 'should be 1')
        self.assertAlmostEqual(normalized_array[1, 0], 0.5, 1, 'should be .5')
        self.assertAlmostEqual(normalized_array[1, 1], 0.5, 1, 'should be .5')
        self.assertAlmostEqual(normalized_array.min(), 0.0, 1, 'no lower than zero')
        self.assertAlmostEqual(normalized_array.max(), 1, 1, 'none higher than 1')

    def test_array_to_prev_next_rows(self):
        axis = 0
        prev_next = array_to_prev_next(test_array, axis)
        self.assertAlmostEqual(prev_next[0][0, 0], 60.0, 1, 'should be 60')
        self.assertAlmostEqual(prev_next[0][1, 0], 10.0, 1, 'should be 10')
        self.assertAlmostEqual(prev_next[1][0, 0], 20.0, 1, 'should be 20')
        self.assertAlmostEqual(prev_next[1][1, 0], 30.0, 1, 'should be 30')

    def test_array_to_prev_next_cols(self):
        test_array = np.array(
            [[10.0, 20.0, 30.0, 40.0, 50.0], [20.0, 30.0, 40.0, 50.0, 60.0], [30.0, 40.0, 50.0, 60.0, 70.0],
             [70.0, 60.0, 50.0, 40.0, 30.0],
             [60.0, 50.0, 40.0, 20.0, 30.0]], dtype=np.float64)
        axis = 1
        prev_next = array_to_prev_next(test_array, axis)
        self.assertAlmostEqual(prev_next[0][0, 0], 50.0, 1, 'should be 50')
        self.assertAlmostEqual(prev_next[0][0, 1], 10.0, 1, 'should be 10')
        self.assertAlmostEqual(prev_next[1][0, 0], 20.0, 1, 'should be 20')
        self.assertAlmostEqual(prev_next[1][0, 1], 30.0, 1, 'should be 30')

    def test_calculate_slope_at_points(self):
        self.fail()

    def test_create_BGR_panels(self):
        self.fail()

    def test_normalize_unit_vectors(self):
        self.fail()

    def test_convert_to_image(self):
        self.fail()

    def test_display_grayscales(self):
        self.fail()

    def build_normal_image(self):
        self.fail()

    def test_display_normal_image(self):
        self.fail()
