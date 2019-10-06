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
            # Trim whitespace top and bottom
            yield char
