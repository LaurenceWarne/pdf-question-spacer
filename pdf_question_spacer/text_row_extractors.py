from typing import Callable

import numpy as np


class RowExtraction():
    """Encapsulates the result of a row extraction on an image."""

    def __init__(self, rows: np.array, row_indices: np.array):
        self._rows = rows
        self._row_indices = row_indices

    @property
    def rows(self) -> np.array:
        """
        Return a nested numpy array consisting of rows of text in
        the image.
        """
        return self._rows

    @property
    def row_indices(self) -> np.array:
        return self._row_indices


class TextRowExtractor():

    def __init__(self, pixel_predicate=lambda arr: arr == 0):
        self._pixel_predicate = pixel_predicate

    @property
    def pixel_predicate(self) -> Callable[[np.array], np.array]:
        return self._pixel_predicate

    @pixel_predicate.setter
    def pixel_predicate(self, pixel_predicate):
        self._pixel_predicate = pixel_predicate

    def extract(self, image: np.array) -> RowExtraction:
        row_contains_black = np.any(self._pixel_predicate(image), axis=1)
        runs = find_runs(1, row_contains_black)
        return RowExtraction(
            # can't apply np.fromiter to 2d arrays
            np.array([image[slice(*run)] for run in runs]),
            runs
        )


# credit:
# https://stackoverflow.com/questions/31544129/extract-separate-non-zero-blocks-from-array
def find_runs(value, a):
    # Create an array that is 1 where a is `value`, and pad each end with
    # an extra 0.
    isvalue = np.concatenate(([0], np.equal(a, value).view(np.int8), [0]))
    absdiff = np.abs(np.diff(isvalue))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges
