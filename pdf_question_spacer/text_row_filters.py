"""
This module handles the selection of image regions, the second stage of
processing.
"""

import re
from typing import Callable, Any, Sequence, Tuple

import numpy as np
import numpy.typing as npt
import cv2
import matplotlib.pyplot as plt
import pytesseract
from fuzzywuzzy import process

from .text_row_extractors import RowExtraction


def pad_array(
        image: npt.NDArray,
        pad_amount: int = 50,
        whitespace_element: Any = 255
):
    whitespace_line = np.repeat(whitespace_element, image.shape[1])
    whitespace_line = np.array(whitespace_line, dtype=np.uint8)
    return np.concatenate((
        [whitespace_line] * pad_amount,
        image,
        [whitespace_line] * pad_amount
    ))


def pad_then_extract(
        image: npt.NDArray,
        image_to_text_func: Callable[
            [npt.NDArray], str
        ] = pytesseract.image_to_string,
        pad_amount: int = 50,
        whitespace_element: Any = 255
):
    return image_to_text_func(pad_array(image, pad_amount, whitespace_element))


class RowFilter:
    """
    Filters regions from some RowExtraction by extracting text and applying
    some predicate.
    """

    def __init__(
            self,
            region_predicate: Callable[
                [npt.NDArray], bool
            ]
    ):
        self._region_predicate = region_predicate

    @property
    def region_predicate(self) -> Callable[[npt.NDArray], str]:
        return self._region_predicate

    @region_predicate.setter
    def region_predicate(
            self,
            region_predicate: Callable[[npt.NDArray], str]
    ):
        self._region_predicate = region_predicate

    def filter_extraction(
            self, extraction_obj: RowExtraction) -> RowExtraction:
        """
        Return a RowExtraction obj with rows taken from the passed
        RowExtraction obj, and matching the regular expression held by
        this object.
        """
        matching_indices = []
        for index, row in enumerate(extraction_obj.rows):
            if (self._region_predicate(row, index)):
                matching_indices.append(index)
        return RowExtraction(
            extraction_obj.rows[matching_indices],
            extraction_obj.row_indices[matching_indices]
        )


class TextMatcher:
    """
    Uses fuzzywuzzy to match a text from a passed image (in the form of a numpy
    array) to a string from a set of predefined strings.
    """

    def __init__(
            self,
            known_lines: Sequence[str],
            regexes: Sequence[str],
            image_to_text_func: Callable[
                [npt.NDArray], str
            ] = pad_then_extract
    ):
        self._known_lines = known_lines
        self._regexes = regexes
        self._matches = []  # Store matches for convenience
        self._image_to_text_func = image_to_text_func  # For testing

    def __call__(self, row: [npt.NDArray], index: int) -> bool:
        """
        Extract the text from a numpy array representing an image and test
        the best match to that string from this objects known_lines attribute
        using Levenshtein distance against this objects regexes attribute.
        """
        row_text = self._image_to_text_func(row)
        if (row_text):  # '' gives annoying fuzzywuzzy warnings
            match = process.extractOne(row_text, self._known_lines)
            self._matches.append((row_text, match[0]))
            return any(
                map(lambda regex: re.match(regex, match[0]), self._regexes)
            )
        else:
            self._matches.append((row_text, "<NO MATCH FOUND>"))
            return False

    @property
    def regexes(self) -> str:
        return self._regexes

    @regexes.setter
    def regexes(self, regexes: str):
        self._regexes = regexes

    @property
    def image_to_text_func(self) -> Callable[[npt.NDArray], str]:
        return self._image_to_text_func

    @image_to_text_func.setter
    def image_to_text_func(
            self,
            image_to_text_func: Callable[[npt.NDArray], str],
    ):
        self._image_to_text_func = image_to_text_func

    @property
    def known_lines(self) -> Sequence[str]:
        return self._known_lines

    @property
    def matches(self) -> Sequence[Tuple[str, str]]:
        return self._matches

    @known_lines.setter
    def known_lines(self, known_lines: Sequence[str]):
        self._known_lines = known_lines

    @classmethod
    def from_array(
            cls,
            image_as_array: npt.NDArray,
            regexes,
            image_to_text_func: Callable[
                [npt.NDArray], str
            ] = pad_then_extract

    ) -> "TextMatcher":
        extraction = pytesseract.image_to_string(image_as_array)
        lines_of_text = str(extraction).splitlines()
        return cls(lines_of_text, regexes, image_to_text_func)


class InteractiveMatcher:
    """
    Class which allows users to select regions to add whitespace to by showing
    them the regions.
    """

    def __init__(
            self,
            all_rows: RowExtraction,
            previous_regions_preview: int = 5,
            show_previous_regions: bool = True
    ):
        self._all_rows = all_rows
        self._previous_regions_preview = previous_regions_preview
        self._show_previous_regions = show_previous_regions
        self._button_press = "n"

    def __call__(self, row: [npt.NDArray], index: int) -> bool:
        """
        Show the region to the user in a matplotlib figure and let them choose
        whether to accept the region or not via a keypress.
        """
        # First of all show the preview if appropriate
        show_preview = self._show_previous_regions and index != 0
        if (show_preview):
            self.show_preview(index)

        plt.subplot(2, 1, 2 if show_preview else 1)
        plt.title("Current Region", fontweight="bold")
        plt.xlabel("Input (y/n) to add whitespace before the region")
        plt.connect('key_press_event', self.key_pressed)
        plt.imshow(row, cmap="gray")

        # Wait for keypress
        plt.waitforbuttonpress()
        plt.close()
        if (self._button_press == "y"):
            return True
        else:
            return False

    def show_preview(self, row_index: int):
        preview_length = min(self._previous_regions_preview, row_index)
        preview_slice = slice(row_index - preview_length, row_index)
        preview = cv2.vconcat([
            pad_array(region, pad_amount=20)
            for region in self._all_rows.rows[preview_slice]
        ])

        plt.subplot(2, 1, 1)
        plt.title("Previous Regions", fontweight="bold")
        plt.imshow(preview, cmap="gray")

    def key_pressed(self, event):
        self._button_press = event.key

    @property
    def previous_regions_preview(self) -> int:
        return self._previous_regions_preview

    @previous_regions_preview.setter
    def regexes(self, previous_regions_preview: int):
        self._previous_regions_preview = previous_regions_preview

    @property
    def all_rows(self) -> RowExtraction:
        return self._all_rows

    @property
    def show_previous_regions(self) -> bool:
        return self._show_previous_regions
