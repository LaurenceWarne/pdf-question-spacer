import numpy as np

from .text_row_extractors import TextRowExtractor


class CharacterExtractor():

    def __init__(self, pixel_predicate=lambda arr: arr == 0):
        self.pixel_predicate = pixel_predicate
        self._text_row_extractor = TextRowExtractor(pixel_predicate)
        pass

    def extract(self, image):
        """
        Yield characters (each as a numpy array) detected in the specified
        image.
        """
        image_transpose = np.transpose(image)
        chars_transposed = self._text_row_extractor.extract(image_transpose)
        for transposed_char in chars_transposed:
            char = transposed_char.transpose()
            # Trim whitespace image top and bottom
            char_boolean = np.any(char == 0, axis=1)
            first_nonempty_row = np.argmax(char_boolean)
            last_nonempty_row = np.argmax(char_boolean[::-1])
            crop = min(first_nonempty_row, last_nonempty_row)
            yield char if crop == 0 else char[crop:-crop]
