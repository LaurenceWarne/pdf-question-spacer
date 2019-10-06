import numpy as np


class TextRowExtractor():

    def __init__(self, pixel_predicate=lambda arr: arr == 0):
        self.pixel_predicate = pixel_predicate

    def extract(self, image):
        row_contains_black = np.any(self.pixel_predicate(image), axis=1)
        runs = find_runs(1, row_contains_black)
        for run in runs:
            yield image[slice(*run)]


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
