"""
This module contains classes handling the first stage of processing the pdf:
extracting rows of text.
"""

from dataclasses import dataclass

from typing import Callable, Any

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class RowExtraction:
    """
    Encapsulates the result of a row-wise extraction from an image of
    sub-images ('regions') usually satisfying some predicate.

    This class holds the start and end indices of the regions with respect to
    the original image along with the actual regions themselves.
    """
    # NumPy does not support the annotating of array shapes as of 1.21, this
    # is expected to change in the future though (see PEP 646).
    rows: npt.NDArray
    row_indices: npt.NDArray


class TextRowExtractor:
    """
    Extract indices representing the start and end points of rows ('regions')
    matching some predicate.
    """

    def __init__(
            self,
            pixel_predicate: Callable[
                npt.NDArray, npt.NDArray
            ] = lambda arr: arr == 0
    ):
        self._pixel_predicate = pixel_predicate

    @property
    def pixel_predicate(self) -> Callable[
            [npt.NDArray], npt.NDArray
    ]:
        return self._pixel_predicate

    @pixel_predicate.setter
    def pixel_predicate(
            self,
            pixel_predicate: Callable[[npt.NDArray], npt.NDArray]
    ):
        self._pixel_predicate = pixel_predicate

    def extract(self, image: npt.NDArray) -> RowExtraction:
        """
        Extract 'regions' from an image matching this objects predicate.
        """
        row_contains_black = np.any(self._pixel_predicate(image), axis=1)
        runs = find_runs(1, row_contains_black)
        return RowExtraction(
            # can't apply np.fromiter to 2d arrays
            np.array([image[slice(*run)] for run in runs]),
            runs
        )


# credit:
# https://stackoverflow.com/questions/31544129/extract-separate-non-zero-blocks-from-array
def find_runs(value: Any, a: npt.NDArray) -> npt.NDArray:
    """inclusive-exclusive"""
    # Create an array that is 1 where a is `value`, and pad each end with
    # an extra 0.
    isvalue = np.concatenate(([0], np.equal(a, value).view(np.int8), [0]))
    absdiff = np.abs(np.diff(isvalue))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges
