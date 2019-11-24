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
        row_filter = RowFilter(RegionPredicate())
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(3, len(extraction.rows))
        self.assertEqual(3, len(extraction.row_indices))

    def test_empty_extraction_returned_on_no_matching_rows(self):
        row_filter = RowFilter(lambda region, index: False)
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(0, len(extraction.rows))
        self.assertEqual(0, len(extraction.row_indices))

    def test_all_regions_returned_when_all_rows_are_matched(self):
        row_filter = RowFilter(lambda region, index: True)
        extraction = row_filter.filter_extraction(self.extraction)
        self.assertEqual(5, len(extraction.rows))
        self.assertEqual(5, len(extraction.row_indices))


class RegionPredicate():

    def __init__(self):
        self._count = -1

    def __call__(self, img, index) -> bool:
        self._count += 1
        return self._count % 2 == 0
