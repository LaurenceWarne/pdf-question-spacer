"""
This module contains classes used for inserting whitespace into the appropriate
places in the pdf, the last stage of processing.
"""
from typing import Any, Tuple
import numpy as np
import numpy.typing as npt


class WhitespaceInserter:
    """Inserts whitespace into numpy array images."""

    def __init__(self, whitespace_length: int, add_before_region: bool = True):
        self.whitespace_length = whitespace_length
        self.add_before_region = add_before_region

    def insert_whitespace(
            self,
            img: npt.NDArray,
            target_region_indices: npt.NDArray,
            all_region_indices: npt.NDArray,
            whitespace_element: Any
    ) -> Tuple[npt.NDArray, npt.NDArray]:
        """
        Insert whitespace into an image (a 2d numpy array) inbetween the
        regions of the image specified by 'target_region_indices'. Return
        the image with whitespace added along with the shifted regions.
        """
        whitespace_line = np.repeat(whitespace_element, img.shape[1])
        for index, (start, end) in enumerate(target_region_indices):
            if (self.add_before_region):
                slice_point = start + index * self.whitespace_length
            else:
                slice_point = end + index * self.whitespace_length + 1
            img = pad_array(
                img, slice_point, whitespace_line, self.whitespace_length
            )
            all_region_indices = add_to_regions_above(
                slice_point, all_region_indices, self.whitespace_length
            )
        return (img, all_region_indices)


class ImagePager:
    """
    Breaks image arrays into multiple arrays ('pages') in such a way that
    no text is cut in half.
    """

    def __init__(self, page_pixel_length: int):
        self.page_pixel_length = page_pixel_length

    def pad_regions_spanning_pages(
            self,
            img: npt.NDArray,
            regions: npt.NDArray,
            whitespace_element: Any
    ) -> npt.NDArray:
        """
        Add lines of whitespace before regions that would otherwise span
        multiple pages. The new padded image array is then returned.
        """
        region_pages = regions // self.page_pixel_length
        overflowing_regions = regions[region_pages[:, 0] != region_pages[:, 1]]
        whitespace_line = np.repeat(whitespace_element, img.shape[1])
        if (overflowing_regions.size != 0):
            region_start = overflowing_regions[0, 0]
            pad_amount = inv_mod(region_start, self.page_pixel_length)
            img = pad_array(img, region_start, whitespace_line, pad_amount)
            regions = add_to_regions_above(region_start, regions, pad_amount)
            return self.pad_regions_spanning_pages(
                img, regions, whitespace_element
            )
        else:
            return img

    def split_into_pages(
            self,
            img: npt.NDArray,
            regions: npt.NDArray,
            whitespace_element: Any
    ) -> npt.NDArray:
        """
        Return an array of image arrays, with padding added to the last array
        so that all arrays are of the same shape.
        """
        end_padding = inv_mod(img.shape[0], self.page_pixel_length)
        if (end_padding):
            whitespace_line = np.repeat(whitespace_element, img.shape[1])
            img = np.concatenate((img, [whitespace_line] * end_padding))
        return np.array(np.array_split(
            img, img.shape[0] / self.page_pixel_length
        ))

    def organize_pages(
            self,
            img: npt.NDArray,
            regions: npt.NDArray,
            whitespace_element: Any
    ) -> npt.NDArray:
        """
        Returns an array of images (as arrays of size corresponding to
        page_pixel_length) such that none of the regions of the image specified
        by the parameter 'regions' span more than one page.
        Whitespace corresponding to the 'whitespace' parameter is added as
        appropriate.

        Is a wrapper around pad_regions_spanning_pages() and split_into_pages()
        """
        shifted_img = self.pad_regions_spanning_pages(
            img, regions, whitespace_element
        )
        return self.split_into_pages(
            shifted_img, regions, whitespace_element
        )


def inv_mod(dividend: int, divisor: int):
    """
    Return the additive inverse of 'dividend' wrt to modulo divisor arithmetic,
    0 <= return < divisor.
    """
    return (divisor - (dividend % divisor)) % divisor


def pad_array(
        array: npt.NDArray,
        index: int,
        pad_element: Any,
        amount: int
) -> npt.NDArray:
    """
    Add 'amount' sets of 'pad_element' to the specified array at the index
    specified by 'index'.
    """
    return np.concatenate((
        array[:index],
        [pad_element] * amount,
        array[index:]
    ))


def add_to_regions_above(
        cut_off: int,
        regions: npt.NDArray,
        amount: int,
        include_equality: bool = True
):
    if (include_equality):
        shifted_arr = (regions[:, 0] >= cut_off) * amount
    else:
        shifted_arr = (regions[:, 0] > cut_off) * amount
    return regions + shifted_arr.reshape(len(regions), 1)
