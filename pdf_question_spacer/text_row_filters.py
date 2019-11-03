"""
This module handles the selection of image regions, the second stage of
processing.
"""

import re
import itertools
from typing import Callable, Any, Sequence

from nptyping import Array
import pytesseract
import textract
from fuzzywuzzy import process

from .text_row_extractors import RowExtraction


class RowFilter:
    """
    Filters regions from some RowExtraction by extracting text and applying
    some predicate.
    """

    def __init__(
            self, regex: str,
            image_to_text_func: Callable[
                [Array[Array[Any]]], str
            ] = pytesseract.image_to_string
    ):
        self._regex = regex
        self._image_to_text_func = image_to_text_func
        self._most_recent_extracted_rows = []

    @property
    def regex(self) -> str:
        return self._regex

    @regex.setter
    def regex(self, regex: str):
        self._regex = regex

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
    def most_recent_extracted_rows(self) -> Sequence[str]:
        return self._most_recent_extracted_rows

    def filter_extraction(
            self, extraction_obj: RowExtraction) -> RowExtraction:
        """
        Return a RowExtraction obj with rows taken from the passed
        RowExtraction obj, and matching the regular expression held by
        this object.
        """
        self._most_recent_extracted_rows.clear()
        matching_indices = []
        for index, row in enumerate(extraction_obj.rows):
            text = self._image_to_text_func(row).strip()
            if (re.match(self._regex, text)):
                matching_indices.append(index)
            self._most_recent_extracted_rows.append(text)
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
            image_to_text_func: Callable[
                [Array[Array[Any]]], str
            ] = pytesseract.image_to_string
    ):
        self._image_to_text_func = image_to_text_func
        self._known_lines = known_lines

    def __call__(self, row: [Array[Array[Any]]]) -> str:
        """
        Extract the text from a numpy array representing an image and return
        the best match to that string from this objects known_lines attribute
        using Levenshtein distance.
        """
        row_text = self._image_to_text_func(row)
        if (row_text):  # '' gives annoying fuzzywuzzy warnings
            match = process.extractOne(row_text, self._known_lines)
            return match[0]
        else:
            return row_text

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

    @known_lines.setter
    def known_lines(self, known_lines: Sequence[str]):
        self._known_lines = known_lines

    @classmethod
    def from_file(cls, filename: str) -> "TextMatcher":
        extraction = textract.process(filename)
        lines_of_text = str(extraction).split("\\n")
        return cls(lines_of_text)
