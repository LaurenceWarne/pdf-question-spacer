"""
This module handles the selection of image regions, the second stage of
processing.
"""

import re
from typing import Callable, Any, Sequence, Tuple

import numpy as np
import matplotlib.pyplot as plt
from nptyping import Array
import pytesseract
from fuzzywuzzy import process

from .text_row_extractors import RowExtraction


def pad_then_extract(
        image: Array[Array[Any]],
        image_to_text_func: Callable[
            [Array[Array[Any]]], str
        ] = pytesseract.image_to_string,
        pad_amount: int = 50,
        whitespace_element: Any = 255
):
    whitespace_line = np.repeat(whitespace_element, image.shape[1])
    whitespace_line = np.array(whitespace_line, dtype=np.uint8)
    padded_array = np.concatenate((
        [whitespace_line] * pad_amount,
        image,
        [whitespace_line] * pad_amount
    ))
    return image_to_text_func(padded_array)


class RowFilter:
    """
    Filters regions from some RowExtraction by extracting text and applying
    some predicate.
    """

    def __init__(
            self,
            region_predicate: Callable[
                [Array[Array[Any]]], bool
            ] = pytesseract.image_to_string
    ):
        self._region_predicate = region_predicate

    @property
    def region_predicate(self) -> Callable[[Array[Array[Any]]], str]:
        return self._region_predicate

    @region_predicate.setter
    def region_predicate(
            self,
            region_predicate: Callable[[Array[Array[Any]]], str]
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
            if (self._region_predicate(row)):
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
                [Array[Array[Any]]], str
            ] = pad_then_extract
    ):
        self._image_to_text_func = image_to_text_func  # For testing
        self._known_lines = known_lines
        self._matches = []  # Store matches for convenience
        self._regexes = regexes

    def __call__(self, row: [Array[Array[Any]]]) -> bool:
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
    def image_to_text_func(self) -> Callable[[Array[Array[Any]]], str]:
        return self._image_to_text_func

    @image_to_text_func.setter
    def image_to_text_func(
            self,
            image_to_text_func: Callable[[Array[Array[Any]]], str]
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
    def from_array(cls, image_as_array: Array[Array[Any]]) -> "TextMatcher":
        extraction = pytesseract.image_to_string(image_as_array)
        lines_of_text = str(extraction).splitlines()
        return cls(lines_of_text)


class InteractiveMatcher:
    """
    Class which allows users to select regions to add whitespace to by showing
    them the regions.
    """

    def __init__(self, all_rows: RowExtraction):
        self._all_rows = all_rows

    def __call__(self, row: [Array[Array[Any]]]) -> bool:
        """
        Show the region to the user in a matplotlib figure and let them choose
        whether to accept the region or not via a keypress.
        """
        plt.subplot(2, 1, 1)
        plt.title(
            """
            Current Region, input (y/n) to input whitespace (before region)
            """
        )
        plt.imshow(row, cmap="gray")

        all_rows = self._all_rows.row_indices
        if (self._all_rows.index(row) < len(all_rows)):
            next_row = self._all_rows[all_rows.index(row) + 1]
            plt.subplot(2, 1, 2)
            plt.title("Next Region")
            plt.imshow(next_row, cmap="gray")

        # Wait for keypress
