from typing import Any

import numpy as np
from nptyping import Array


class WhitespaceInserter():

    def __init__(self, whitespace_length: int, add_before_region: bool = True):
        self.whitespace_length = whitespace_length
        self.add_before_region = add_before_region

    def glue(
            self,
            img: Array[Array[Any]],
            all_break_indices: Array[Array[int, ..., 2]],
            target_break_indices: Array[Array[int, ..., 2]],
            whitespace_element: Any
    ):
        whitespace_line = np.repeat(whitespace_element, img.shape[1])
        for index, (start, end) in enumerate(all_break_indices):
            if (self.add_before_region):
                slice_point = start + index * self.whitespace_length
            else:
                slice_point = end + index * self.whitespace_length + 1
            img = np.concatenate(
                img[:slice_point],
                np.tile(whitespace_line, (self.whitespace_length, 1)),
                img[slice_point:]
            )


class ImagePager():

    def __init__(self, page_pixel_length):
        self.page_pixel_length = page_pixel_length
