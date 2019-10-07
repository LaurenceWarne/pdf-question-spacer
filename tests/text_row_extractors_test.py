from unittest import TestCase

import numpy as np

from pdf_question_spacer.text_row_extractors import TextRowExtractor


class TestRowExtractor(TestCase):

    def setUp(self):
        pass

    def test_can_extract_one_row(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        # Assert region correct
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[0]
        )
        self.assertEqual(1, len(extracted_regions.rows))

    def test_can_extract_one_row_at_start(self):
        arr = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        # Assert region correct
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[0]
        )
        # Assert no more regions found
        self.assertEqual(1, len(extracted_regions.rows))

    def test_can_extract_one_row_at_end(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        # Assert region correct
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[0]
        )
        self.assertEqual(1, len(extracted_regions.rows))

    def test_can_extract_multiple_regions(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        # Assert region correct
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[0]
        )
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[1]
        )
        # Assert two regions found in total
        self.assertEqual(2, len(extracted_regions.rows))

    def test_can_extract_region_not_all_target(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        # Assert region correct
        np.testing.assert_array_equal(
            np.array(
                [[1, 0, 1, 1, 0, 0]],
                dtype=np.bool),
            extracted_regions.rows[0]
        )
        self.assertEqual(1, len(extracted_regions.rows))

    def test_extract_returns_nothing_on_no_valid_rows(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        self.assertEqual(0, len(extracted_regions.rows))
