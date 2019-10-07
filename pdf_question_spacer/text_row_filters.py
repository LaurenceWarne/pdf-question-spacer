import re

import pytesseract

from .text_row_extractors import RowExtraction


class RowFilter():

    def __init__(self, regex: str):
        self._regex = regex

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, regex: str):
        self._regex = regex

    def filter(self, extraction_obj: RowExtraction) -> RowExtraction:
        """
        Return a RowExtraction obj with rows taken from the passed
        RowExtraction obj, and matching the regular expression held by
        this object.
        """
        matching_indices = []
        for index, row in enumerate(extraction_obj.rows):
            text = pytesseract.image_to_string(row).strip()
            if (re.match(self._regex, text)):
                matching_indices.append(index)
        return RowExtraction(
            extraction_obj.rows[matching_indices],
            extraction_obj.row_indices[matching_indices]
        )
