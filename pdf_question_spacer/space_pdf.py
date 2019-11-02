import argparse

import numpy as np
import cv2
from wand.image import Image

from .text_row_extractors import TextRowExtractor
from .text_row_filters import RowFilter
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
        default="^[\duvil]+[\.\)]",
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
        "--debug-text",
        help="""print out text extracted from the pdf, helpful for finding
        a regex that works as text extraction is not always perfect""",
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
        row_filter = RowFilter(args.regex)

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

        if (args.debug_text):
            print("All rows found:")
            for row in row_filter.most_recent_extracted_rows:
                print(row)


if __name__ == "__main__":
    main()
