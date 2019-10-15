import numpy as np
import cv2
import matplotlib.pyplot as plt
from wand.image import Image

from .text_row_extractors import TextRowExtractor
from .text_row_filters import RowFilter
from .whitespace_inserter import WhitespaceInserter, ImagePager


def space_pdf(filename, skip_first=True):

    print("Opening pdf as images...")
    all_images = []
    with Image(filename=filename, resolution=150) as images:
        for single_image in images.sequence:
            with Image(single_image) as i:
                im = cv2.imdecode(
                    np.asarray(bytearray(i.make_blob("png")), dtype=np.uint8),
                    cv2.IMREAD_GRAYSCALE
                )
                all_images.append(im)

        print("Concatenating images...")
        img = np.concatenate(all_images)

        print("Extracting rows of text from image...")
        extractor = TextRowExtractor()
        extraction = extractor.extract(img)
        row_filter = RowFilter("^[\duvil]+[\.\)]")        

        print("Filtering extracted rows by specified regular expression...")
        filtered_extraction = row_filter.filter_extraction(extraction)

        print("Inserting whitespace")
        wspace_inserter = WhitespaceInserter(200)
        img, shifted_regions = wspace_inserter.insert_whitespace(
            img,
            filtered_extraction.row_indices[skip_first:],
            extraction.row_indices,
            255
        )

        print("Creating pdf pages")
        pager = ImagePager(im.shape[0])
        pages = pager.organize_pages(
            img, shifted_regions, 255
        )

        for index, page in enumerate(pages):
            cv2.imwrite("out{}.png".format(index), page)
