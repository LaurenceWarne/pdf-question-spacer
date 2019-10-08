from typing import Callable, Tuple

from nptyping import Array
import numpy as np


class RowExtraction():
    """
    Encapsulates the result of a row-wise extraction from an image
    of sub-images satisfying some predicate.
    """

    def __init__(
            self, rows: Array[Array],
            row_indices: Array[Tuple[int, int]]
    ):
        self._rows = rows
        self._row_indices = row_indices

    @property
    def rows(self) -> Array[Array]:
        """
        Return a nested numpy array denoting rows of text in the image.
        """
        return self._rows

    @property
    def row_indices(self) -> Array[Tuple[int, int]]:
        return self._row_indices


class TextRowExtractor():

    def __init__(self, pixel_predicate=lambda arr: arr == 0):
        self._pixel_predicate = pixel_predicate

    @property
    def pixel_predicate(self) -> Callable[[Array[Array]], Array[Array[bool]]]:
        return self._pixel_predicate

    @pixel_predicate.setter
    def pixel_predicate(
            self,
            pixel_predicate: Callable[[Array[Array]], Array[Array[bool]]]
    ):
        self._pixel_predicate = pixel_predicate

    def extract(self, image: Array[Array]) -> RowExtraction:
        row_contains_black = np.any(self._pixel_predicate(image), axis=1)
        runs = find_runs(1, row_contains_black)
        return RowExtraction(
            # can't apply np.fromiter to 2d arrays
            np.array([image[slice(*run)] for run in runs]),
            runs
        )


# credit:
# https://stackoverflow.com/questions/31544129/extract-separate-non-zero-blocks-from-array
def find_runs(value, a) -> Array[Tuple[int, int]]:
    # Create an array that is 1 where a is `value`, and pad each end with
    # an extra 0.
    isvalue = np.concatenate(([0], np.equal(a, value).view(np.int8), [0]))
    absdiff = np.abs(np.diff(isvalue))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges
