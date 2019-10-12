from unittest import TestCase

import numpy as np

from pdf_question_spacer.whitespace_inserter import (
    WhitespaceInserter, ImagePager
)


class TestWhitespaceInsert(TestCase):

    def setUp(self):
        self.inserter = WhitespaceInserter(2, True)
        self.pager = ImagePager(4)

    def test_whitespace_inserted_correctly_for_one_region(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [1, 3]  # inclusive-exclusive range
        ])
        img, _ = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [0, 0, 0, 0],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]),
            img
        )

    def test_region_indices_shifted_correctly_for_one_region(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [1, 3]
        ])
        _, shifted_regions = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [3, 5]
            ]),
            shifted_regions
        )

    def test_no_whitespace_added_if_regions_empty(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ])
        regions = np.array([])
        img, _ = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )
        np.testing.assert_array_equal(
            arr, img
        )

    def test_whitespace_inserted_correctly_for_one_region_at_array_end(self):
        arr = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ])
        regions = np.array([
            [2, 4]
        ])
        img, _ = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ]),
            img
        )

    def test_whitespace_inserted_correctly_for_one_region_at_array_start(self):
        arr = np.array([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [0, 2]
        ])
        img, _ = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]),
            img
        )

    def test_whitespace_inserted_correctly_for_multiple_regions(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],     
        ])
        target_regions = np.array([
            [1, 3], [5, 6]
        ])
        all_regions = np.array([
            [1, 3], [5, 6]
        ])
        img, _ = self.inserter.insert_whitespace(
            arr, target_regions, all_regions, 2
        )
        np.testing.assert_array_equal(
            np.array([
                [0, 0, 0, 0],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [2, 2, 2, 2],
                [2, 2, 2, 2],
                [1, 1, 1, 1],                
            ]),
            img
        )

    def test_region_indices_shifted_correctly_for_multiple_regions(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1]
        ])
        regions = np.array([
            [1, 3], [5, 6]
        ])
        _, shifted_regions = self.inserter.insert_whitespace(
            arr, regions, regions, 2
        )
        np.testing.assert_array_equal(
            np.array([
                [3, 5], [9, 10]
            ]),
            shifted_regions
        )

    def test_region_indices_shifted_correctly_with_non_target_indices(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        all_regions = np.array([
            [1, 3], [4, 5]
        ])
        regions = np.array([
            [1, 3]
        ])
        _, shifted_regions = self.inserter.insert_whitespace(
            arr, regions, all_regions, 2
        )
        np.testing.assert_array_equal(
            np.array([
                [3, 5], [6, 7]
            ]),
            shifted_regions
        )

    def test_region_indices_shifted_correctly_with_non_target_index_before_target_index(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        all_regions = np.array([
            [0, 1], [1, 3]
        ])
        regions = np.array([
            [1, 3]
        ])
        _, shifted_regions = self.inserter.insert_whitespace(
            arr, regions, all_regions, 2
        )
        np.testing.assert_array_equal(
            np.array([
                [0, 1], [3, 5]
            ]),
            shifted_regions
        )

    def test_no_whitespace_added_if_regions_dont_span_pages(self):
        arr = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            # Page 2
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [1, 3], [5, 6]
        ])
        pages = self.pager.organize_pages(
            arr, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0]],
                # Page 2
                [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
            ]),
            pages
        )

    def test_whitespace_added_one_region_spans_page(self):
        arr = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            # Page 2
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [1, 3], [3, 5]
        ])
        pages = self.pager.organize_pages(
            arr, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [2, 2, 2, 2]],
                # Page 2
                [[1, 1, 1, 1],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],
                # Page 3
                [[0, 0, 0, 0],
                 [2, 2, 2, 2],
                 [2, 2, 2, 2],
                 [2, 2, 2, 2]]
            ]),
            pages
        )

    def test_whitespace_added_multiple_regions_span_page(self):
        arr = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            # Page 2
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            # Page 3
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        regions = np.array([
            [1, 2], [3, 5], [6, 9]
        ])
        pages = self.pager.organize_pages(
            arr, regions, 2
        )

        np.testing.assert_array_equal(
            np.array([
                [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [2, 2, 2, 2]],
                # Page 2
                [[1, 1, 1, 1],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [2, 2, 2, 2]],
                # Page 3
                [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],
                # Page 4
                [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [2, 2, 2, 2],
                 [2, 2, 2, 2]],
            ]),
            pages
        )
