import argparse
import re

import numpy as np
import cv2
from pdf2image import convert_from_path

from .text_row_extractors import TextRowExtractor
from .text_row_filters import RowFilter, TextMatcher, InteractiveMatcher
from .whitespace_inserter import WhitespaceInserter, ImagePager


QUESTION_REGEX = "^(\()?(([\dvi]+)|([a-z]))[\.\)]"


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
        help="""Number of lines of whitespace to add per match (in pixels),
        default is 400
        """,
        type=int,
        default=400
    )

    parser.add_argument(
        "-i",
        "--interactive",
        help="""Instead of matching lines using a regular expression, show
        each region to the user and allow them to decide whether to add
        whitespace or not (overrides most other options)
        """,
        action="store_true"
    )
    parser.add_argument(
        "-pl",
        "--preview-length",
        help="""In interactive mode, for every shown region, show the previous
        <n> regions concatenated (where possible) where n is the value passed
        to this argument, default is 5. Has no effect if --interactive is not
        chosen
        """,
        type=int,
        default=5
    )

    parser.add_argument(
        "-r",
        "--regexes",
        nargs="+",
        help="""Match lines with these regular expressions, in addition
        to the default regex which matches lines which appear to be the start
        of questions""",
        default=[],
    )
    parser.add_argument(
        "-ir",
        "--ignore-default-regex",
        help="""Do not use the default regex which matches lines which appear
        to be the start of questions. To use this option you must also use
        the --regexes option""",
        action="store_true"
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
        help="Skip first regular expression match",
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="""Show the text extracted from the pdf regions, along with the
        corresponging region in a matplotlib figure (not functional in
        interactive mode)""",
        action="store_true"
    )
    parser.add_argument(
        "--dpi",
        help="""The image quality, default is 400. This is passed directly
        to pdf2image.convert_from_path(), also note using large values
        will take longer and may cause crashes!""",
        type=int,
        default=400
    )
    return parser.parse_args()


def main():

    # Parse args
    args = parse_args()

    print("Opening pdf as images...")
    pil_images = convert_from_path(args.infile, dpi=args.dpi)

    print("Concatenating images...")
    numpy_images = [np.array(im_part.convert("L")) for im_part in pil_images]
    img = cv2.vconcat(numpy_images)

    print("Extracting rows of text from image...")
    extractor = TextRowExtractor()
    extraction = extractor.extract(img)

    args.regexes += [] if args.ignore_default_regex else [QUESTION_REGEX]
    if (args.interactive):
        print("Launching interactive mode...")
        matcher = InteractiveMatcher(extraction, args.preview_length)
    else:
        print("Filtering extracted rows by specified regular expression...")
        matcher = TextMatcher.from_array(img, args.regexes)
    row_filter = RowFilter(matcher)
    filtered_extraction = row_filter.filter_extraction(extraction)

    print("Inserting whitespace...")
    wspace_inserter = WhitespaceInserter(args.whitespace_length)
    img, shifted_regions = wspace_inserter.insert_whitespace(
        img,
        filtered_extraction.row_indices[args.skip_first:],
        extraction.row_indices,
        args.colour
    )

    print("Creating pdf pages...")
    pager = ImagePager(numpy_images[0].shape[0])
    pages = pager.organize_pages(
        img, shifted_regions, args.colour
    )

    for index, page in enumerate(pages):
        cv2.imwrite("out{index}.png".format(index=index), page)

    if (args.debug and not args.interactive):
        import matplotlib.pyplot as plt
        for index, row in enumerate(extraction.rows):
            plt.imshow(row, cmap="gray")
            extracted = matcher.matches[index]
            plt.title(
                """
                EXTRACTED TEXT: '{extracted_text}'
                AMENDED TEXT: '{amended_text}'
                """.format(
                    extracted_text=extracted[0], amended_text=extracted[1]
                )
            )
            plt.title(
                "MATCHES A REGEX: {does_match}".format(
                    does_match=str(any(map(
                        lambda regex: re.match(regex, extracted[1]),
                        args.regexes
                    )))
                ),
                loc="right"
            )
            plt.show()


if __name__ == "__main__":
    main()
