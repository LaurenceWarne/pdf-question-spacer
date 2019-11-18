from unittest import TestCase

import numpy as np

from pdf_question_spacer.text_row_filters import RowFilter
from pdf_question_spacer.text_row_extractors import RowExtraction


class TestRowFilter(TestCase):

    def setUp(self):
        # Create test image
        image_rows = np.array([np.ones((512, 32)) for i in range(5)])
        indices = np.array([(i * 32, (i + 1) * 32) for i in range(5)])
        self.extraction = RowExtraction(image_rows, indices)

    def test_can_filter_odd_rows_from_test_image(self):
        text_extractor = ImageToText(["Question", "Answer"])
        row_filter = RowFilter(["^Question"], text_extractor)
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(3, len(extraction.rows))
        self.assertEqual(3, len(extraction.row_indices))

    def test_empty_extraction_returned_on_no_matching_rows(self):
        row_filter = RowFilter(["^Question"], lambda im: "Not a question")
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(0, len(extraction.rows))
        self.assertEqual(0, len(extraction.row_indices))

    def test_can_filter_rows_matching_exactly_one_regex(self):
        text_extractor = ImageToText(["Question", "Answer", "Discussion"])
        row_filter = RowFilter(["^Question", "^Answer"], text_extractor)
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(4, len(extraction.rows))
        self.assertEqual(4, len(extraction.row_indices))

    def test_can_filter_rows_matching_both_passed_regexes(self):
        text_extractor = ImageToText(["Question", "Answer"])
        row_filter = RowFilter(["^Quest", "ion$"], text_extractor)
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(3, len(extraction.rows))
        self.assertEqual(3, len(extraction.row_indices))


class ImageToText():

    def __init__(self, text_set):
        self._count = -1
        self._text_set = text_set

    def __call__(self, img):
        self._count += 1
        return self._text_set[self._count % len(self._text_set)]
