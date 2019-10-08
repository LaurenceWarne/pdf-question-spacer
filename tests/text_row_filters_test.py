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
        row_filter = RowFilter("^Question", ImageToText())
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(3, len(extraction.rows))
        self.assertEqual(3, len(extraction.row_indices))

    def test_empty_extraction_returned_on_no_matching_rows(self):
        row_filter = RowFilter("^Question", lambda im: "Not a question")
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(0, len(extraction.rows))
        self.assertEqual(0, len(extraction.row_indices))


class ImageToText():

    def __init__(self):
        self.count = -1

    def __call__(self, img):
        self.count += 1
        return "Answer" if self.count % 2 else "Question"
