import argparse
import re

import numpy as np
import cv2
from wand.image import Image

from .text_row_extractors import TextRowExtractor
from .text_row_filters import RowFilter, TextMatcher
from .whitespace_inserter import WhitespaceInserter, ImagePager


def parse_args():
    description = """
    Add whitespace to sections of pdfs and output the resulting images as pngs.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "infile",
        help="name of pdf to add whitespace to",
    )
    parser.add_argument(
        "whitespace_length",
        help="""number of lines of whitespace to add per match (in pixels),
        default is 400
        """,
        type=int,
        default=400
    )
    parser.add_argument(
        "-r",
        "--regex",
        help="""match lines with this regular expression. The default regex
        matches lines which appear to be the start of questions""",
        default="^(\()?(([\dvi]+)|([a-z]))[\.\)]",
    )
    parser.add_argument(
        "-c",
        "--colour",
        help="Colour of the whitespace, default 255 (white)",
        default=255
    )
    parser.add_argument(
        "-s1",
        "--skip-first",
        help="skip first regular expression match",
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="""Output the text extracted from the pdf, along with the
        corresponging region in a matplotlib figure""",
        action="store_true"
    )
    return parser.parse_args()


def main():

    # Parse args
    args = parse_args()

    print("Opening pdf as images...")
    all_images = []
    with Image(filename=args.infile, resolution=150) as images:
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
        row_filter = RowFilter(args.regex, TextMatcher.from_file(args.infile))

        print("Filtering extracted rows by specified regular expression...")
        filtered_extraction = row_filter.filter_extraction(extraction)

        print("Inserting whitespace")
        wspace_inserter = WhitespaceInserter(args.whitespace_length)
        img, shifted_regions = wspace_inserter.insert_whitespace(
            img,
            filtered_extraction.row_indices[args.skip_first:],
            extraction.row_indices,
            args.colour
        )

        print("Creating pdf pages")
        pager = ImagePager(im.shape[0])
        pages = pager.organize_pages(
            img, shifted_regions, args.colour
        )

        for index, page in enumerate(pages):
            cv2.imwrite("out{}.png".format(index), page)

        if (args.debug):
            import matplotlib.pyplot as plt
            for index, row in enumerate(extraction.rows):
                plt.imshow(row)
                extracted = row_filter.most_recent_extracted_rows[index]
                plt.title("EXTRACTED TEXT: " + extracted)
                plt.title(
                    "MATCHES REGEX: " +
                    str(bool(re.match(args.regex, extracted))),
                    loc="right"
                )
                plt.show()


if __name__ == "__main__":
    main()
