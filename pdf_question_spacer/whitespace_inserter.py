from typing import Any

import numpy as np
from nptyping import Array


class WhitespaceInserter():

    def __init__(self, whitespace_length: int, add_before_region: bool = True):
        self.whitespace_length = whitespace_length
        self.add_before_region = add_before_region

    def insert_whitespace(
            self,
            img: Array[Array[Any]],
            target_break_indices: Array[Array[int, ..., 2]],
            all_break_indices: Array[Array[int, ..., 2]],
            whitespace_element: Any
    ):
        whitespace_line = np.repeat(whitespace_element, img.shape[1])
        for index, (start, end) in enumerate(all_break_indices):
            if (self.add_before_region):
                slice_point = start + index * self.whitespace_length
            else:
                slice_point = end + index * self.whitespace_length + 1
            img = pad_array(
                img, slice_point, whitespace_line, self.whitespace_length
            )


class ImagePager():

    def __init__(self, page_pixel_length):
        self.page_pixel_length = page_pixel_length

    def organize_pages(self, img, regions, whitespace_element):
        region_pages = regions // self.page_pixel_length
        overflowing_regions = regions[region_pages[:, 0] == region_pages[:, 1]]
        if (any(overflowing_regions)):
            region_start = overflowing_regions[0, 0]
            pad_amount = self.page_pixel_length - region_start
            img = pad_array(img, region_start, pad_amount)
            overflowing_regions = overflowing_regions[1:]
            regions = np.where(img < region_start, img, img + pad_amount)
            return self.organize_pages(img, regions, whitespace_element)
        else:
            return np.split(img, self.page_pixel_length)


def pad_array(array, index, pad_element, amount):
    return np.concatenate(
        array[:index],
        [pad_element] * amount,
        array[index:]
    )
