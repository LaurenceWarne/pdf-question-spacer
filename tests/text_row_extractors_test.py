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
            next(extracted_regions)
        )
        # Assert no more regions found
        self.assertIs(None, next(extracted_regions, None))

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
            next(extracted_regions)
        )
        # Assert no more regions found
        self.assertIs(None, next(extracted_regions, None))

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
            next(extracted_regions)
        )
        # Assert no more regions found
        self.assertIs(None, next(extracted_regions, None))

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
            next(extracted_regions)
        )
        np.testing.assert_array_equal(
            np.array(
                [[0, 0, 0, 0, 0, 0]],
                dtype=np.bool),
            next(extracted_regions)
        )
        # Assert no more regions found
        self.assertIs(None, next(extracted_regions, None))

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
            next(extracted_regions)
        )
        # Assert no more regions found
        self.assertIs(None, next(extracted_regions, None))

    def test_extract_returns_nothing_on_no_valid_rows(self):
        arr = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ], dtype=np.bool)
        extractor = TextRowExtractor()
        extracted_regions = extractor.extract(arr)
        self.assertIs(None, next(extracted_regions, None))
