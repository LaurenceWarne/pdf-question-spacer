import re
from typing import Callable, Any

from nptyping import Array
import pytesseract

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

    @property
    def regex(self) -> str:
        return self._regex

    @regex.setter
    def regex(self, regex: str):
        self._regex = regex

    @property
    def image_to_text_func(self) -> Callable[[Array[Array[Any]]], str]:
        return self._image_to_text_func

    @regex.setter
    def regex(self, image_to_text_func: Callable[[Array[Array[Any]]], str]):
        self._image_to_text_func = image_to_text_func

    def filter_extraction(
            self, extraction_obj: RowExtraction) -> RowExtraction:
        """
        Return a RowExtraction obj with rows taken from the passed
        RowExtraction obj, and matching the regular expression held by
        this object.
        """
        matching_indices = []
        for index, row in enumerate(extraction_obj.rows):
            text = self._image_to_text_func(row).strip()
            if (re.match(self._regex, text)):
                matching_indices.append(index)
        return RowExtraction(
            extraction_obj.rows[matching_indices],
            extraction_obj.row_indices[matching_indices]
        )
