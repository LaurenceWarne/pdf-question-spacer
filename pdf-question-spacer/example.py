import sys

import numpy as np
import matplotlib.pyplot as plt
import cv2


# credit:
# https://stackoverflow.com/questions/31544129/extract-separate-non-zero-blocks-from-array
def find_runs(value, a):
    # Create an array that is 1 where a is `value`, and pad each end with an extra 0.
    isvalue = np.concatenate(([0], np.equal(a, value).view(np.int8), [0]))
    absdiff = np.abs(np.diff(isvalue))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges


def main():
    im = cv2.imread(sys.argv[1])
    gscale_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # array which says if a given pixel row has any non-empty pixel in it
    row_contains_black = np.any(gscale_im == 0, axis=1)
    runs = find_runs(1, row_contains_black)
    plt.imshow(gscale_im[slice(*runs[0])], cmap="gray")
    plt.show()


if __name__ == "__main__":
    main()
