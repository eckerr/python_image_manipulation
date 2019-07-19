"""

  Created by Ed and Zack on 1/22/2019
 """
from unittest import TestCase
import numpy as np

from code.create_normal_map import (
                                    convert_array_to_float,
                                    invert_image,
                                    central_dif_cols,
                                    central_dif_rows,
                                    convert_signed_channel_to_image,
                                    convert_signed_channels_to_uint8_channels,
                                    convert_unsigned_channel_to_image,
                                    create_array_of_3_channels,
                                    normalize_float_array,
                                    read_image_to_gray,
                                    remove_bias,
                                    )


class TestNormal(TestCase):

    def test_add_channels(self):
        print("add_channels - not implemented and not used yet")

    def test_balance_norms(self):
        print("balance_norms - not implemented yet")
        pass

    def test_build_normal_image(self):
        print("build_normal_image - not implemented yet")
        self.fail("continue from here")
        pass

    def test_central_dif_cols(self):
        begin_array = np.array([[10, 20, 30],
                                [20, 30, 40],
                                [30, 40, 50]], dtype=np.float32)

        end_array = np.array([[-5.0, 10.0, -5.0],
                              [-5.0, 10.0, -5.0],
                              [-5.0, 10.0, -5.0]], dtype=np.float32)

        out_array = central_dif_cols(begin_array)

        self.assertAlmostEqual(out_array[0][0], end_array[0][0], 1, 'first row, first value should match')
        self.assertAlmostEqual(out_array[0][1], end_array[0][1], 1, 'first row, second value should match')
        self.assertAlmostEqual(out_array[0][2], end_array[0][2], 1, 'first row, third value should match')
        self.assertAlmostEqual(out_array[1][0], end_array[1][0], 1, 'second row, first value should match')
        self.assertAlmostEqual(out_array[1][1], end_array[1][1], 1, 'second row, second value should match')
        self.assertAlmostEqual(out_array[1][2], end_array[1][2], 1, 'second row, third value should match')
        self.assertAlmostEqual(out_array[2][0], end_array[2][0], 1, 'third row, first value should match')
        self.assertAlmostEqual(out_array[2][1], end_array[2][1], 1, 'third row, second value should match')
        self.assertAlmostEqual(out_array[2][2], end_array[2][2], 1, 'third row, third value should match')

    def test_central_dif_rows(self):
        begin_array = np.array([[10, 20, 30],
                                [20, 30, 40],
                                [30, 40, 50]], dtype=np.float32)

        end_array = np.array([[-5.0, -5.0, -5.0],
                              [10.0, 10.0, 10.0],
                              [-5.0, -5.0, -5.0]], dtype=np.float32)

        out_array = central_dif_rows(begin_array)

        self.assertAlmostEqual(out_array[0][0], end_array[0][0], 1, 'first row, first value should match')
        self.assertAlmostEqual(out_array[0][1], end_array[0][1], 1, 'first row, second value should match')
        self.assertAlmostEqual(out_array[0][2], end_array[0][2], 1, 'first row, third value should match')
        self.assertAlmostEqual(out_array[1][0], end_array[1][0], 1, 'second row, first value should match')
        self.assertAlmostEqual(out_array[1][1], end_array[1][1], 1, 'second row, second value should match')
        self.assertAlmostEqual(out_array[1][2], end_array[1][2], 1, 'second row, third value should match')
        self.assertAlmostEqual(out_array[2][0], end_array[2][0], 1, 'third row, first value should match')
        self.assertAlmostEqual(out_array[2][1], end_array[2][1], 1, 'third row, second value should match')
        self.assertAlmostEqual(out_array[2][2], end_array[2][2], 1, 'third row, third value should match')

    def test_convert_array_to_float(self):
        test_array = np.array([[10, 20, 30, 40, 50],
                               [20, 30, 40, 50, 60],
                               [30, 40, 50, 60, 70],
                               [70, 60, 50, 40, 30],
                               [60, 50, 40, 20, 30]], dtype=np.uint8)
        expected_dtype = np.dtype('float32')
        float_array = convert_array_to_float(test_array)
        self.assertEqual(float_array.dtype, expected_dtype, 'array type should be float')

    def test_convert_signed_channels_to_uint8_channels(self):
        float_channel = np.array([[-64, 121],
                                  [127, -12]], dtype=np.float32)
        three_channels = list([float_channel, float_channel, float_channel])
        new_channels = convert_signed_channels_to_uint8_channels(three_channels)
        self.assertEqual(len(new_channels), 3, 'should return 3 channels')
        self.assertGreaterEqual(new_channels[0].min(), 0, 'should contain no negative numbers')

    def test_convert_signed_channel_to_image(self):
        float_channel = np.array([[-64, 121],
                                  [127, -12]], dtype=np.float32)
        converted_channel = convert_signed_channel_to_image(float_channel)
        self.assertEqual(converted_channel.dtype, np.dtype('uint8'))

    def test_convert_unsigned_channel_to_image(self):
        float_channel = np.array([[0, 1],
                                  [0.5, 0.25]], dtype=np.float32)
        out_channel = np.array([[0, 255],
                                [127, 63]], dtype=np.uint8)
        converted_channel = convert_unsigned_channel_to_image(float_channel)
        self.assertEqual(converted_channel[0][0], out_channel[0][0], 'first row, first value')
        self.assertEqual(converted_channel[0][1], out_channel[0][1], 'first row, second value')
        self.assertEqual(converted_channel[1][0], out_channel[1][0], 'second row, first value')
        self.assertEqual(converted_channel[1][1], out_channel[1][1], 'second row, second value')

    def test_create_array_of_3_channels(self):
        new_array = create_array_of_3_channels((1280, 720))
        self.assertEqual(len(new_array), 3, 'should have 3 channels')
        self.assertEqual(type(new_array), type(list()), 'should be a list')

    def test_create_black_window(self):
        print("create_black_window - not implemented or used yet")
        pass

    def test_display_channel_list(self):
        print("display_channel_list - not implemented yet")
        pass

    def test_display_grayscale(self):
        print("display_grayscale - not implemented yet")
        pass

    def test_display_normal_image(self):
        print("display_normal_image - not implemented yet")
        pass

    def test_invert_image(self):
        test_array = np.array([[0, 255, 127],
                               [255, 127, 64],
                               [64, 0, 255]])

        computed = invert_image(test_array)
        self.assertEqual(computed[0][0], 255, 'first row, first value should be inverted')
        self.assertEqual(computed[0][1], 0, 'first row, second value should be inverted')
        self.assertEqual(computed[0][2], 128, 'first row, third value should be inverted')
        self.assertEqual(computed[1][0], 0, 'second row, first value should be inverted')
        self.assertEqual(computed[1][1], 128, 'second row, second value should be inverted')
        self.assertEqual(computed[1][2], 191, 'second row, third value should be inverted')
        self.assertEqual(computed[2][0], 191, 'third row, first value should be inverted')
        self.assertEqual(computed[2][1], 255, 'third row, second value should be inverted')
        self.assertEqual(computed[2][2], 0, 'third row, third value should be inverted')

    def test_normalize_float_array(self):
        small_test_array = np.array([[0, 255],
                                     [128, 128]], dtype=np.float32)
        normalized_array = normalize_float_array(small_test_array)
        self.assertAlmostEqual(normalized_array[0, 0], 0.0, 1, 'should be 0')
        self.assertAlmostEqual(normalized_array[0, 1], 1.0, 1, 'should be 1')
        self.assertAlmostEqual(normalized_array[1, 0], 0.5, 1, 'should be .5')
        self.assertAlmostEqual(normalized_array[1, 1], 0.5, 1, 'should be .5')
        self.assertAlmostEqual(normalized_array.min(), 0.0, 1, 'none lower than zero')
        self.assertAlmostEqual(normalized_array.max(), 1, 1, 'none higher than 1')

    def test_process_image(self):
        print("process_image - not implemented yet")
        pass

    def test_read_image_to_gray(self):
        filename = '.\\images\\qb.png'
        img = read_image_to_gray(filename)
        self.assertEqual(len(img.shape), 2, 'should only be one channel')

    def test_rebalance_all(self):
        print("rebalance_all - not implemented yet")
        pass

    def test_rebalance_norms(self):
        print("rebalance_norms - not implemented yet")
        pass

    def test_remove_bias(self):
        float_channel = np.array([[-64, 121],
                                  [127, -12]], dtype=np.float32)
        median_removed = np.array([[-107.0, 78.0],
                                  [84.0, -55.0]], dtype=np.float32)
        unbiased = remove_bias(float_channel)
        self.assertAlmostEqual(unbiased[0][0], median_removed[0][0], 1, 'first row, first value')
        self.assertAlmostEqual(unbiased[0][1], median_removed[0][1], 1, 'first row, second value')
        self.assertAlmostEqual(unbiased[1][0], median_removed[1][0], 1, 'second row, first value')
        self.assertAlmostEqual(unbiased[1][1], median_removed[1][1], 1, 'second row, second value')

    def test_rescale_x_y(self):
        print("rescale_x_y - not implemented yet")
        pass

    def test_rework_channels(self):
        print("rework_channels - not implemented yet")
        pass

    def test_scale_callback(self):
        print("scale_callback - not implemented yet")
        pass

