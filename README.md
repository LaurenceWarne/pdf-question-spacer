# pdf-question-spacer

## Intro

pdf-question-spacer is a tool used to add whitespace to pdfs. 

For example with the command:

```
space-pdf sample.pdf 200  # Defaults to spacing lines starting with numbers
```

we can transform sample.pdf:

![GitHub Logo](https://i.imgur.com/eGOXNKjl.png)

into:

![GitHub Logo](https://i.imgur.com/F3mjaFsl.png)

## Installation

```
python3 setup.py install --user
```

[ImageMagick](https://imagemagick.org/index.php) and [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) are also required.

## Usage

```
usage: space-pdf [-h] [-r REGEX] [-c COLOUR] [-s1] [-d]
                 infile whitespace_length

Add whitespace to sections of pdfs and output the resulting images as pngs.

positional arguments:
  infile                name of pdf to add whitespace to
  whitespace_length     number of lines of whitespace to add per match (int pixels),
	                    default is 400

optional arguments:
  -h, --help            show this help message and exit
  -r REGEX, --regex REGEX
                        match lines with this regular expression
  -c COLOUR, --colour COLOUR
                        Colour of the whitespace, default 255 (white)
  -s1, --skip-first     skip first regular expression match
  -d, --debug-text      print out text extracted from the pdf, helpful for
                        finding a regex that works as text extraction is not
                        always perfect
```

png files will then be created in the working directory and can be converted to a pdf. For example using ImageMagick:

```
convert out* -page A4 my-new-pdf.pdf
```

## Limitations

Currently only outputs images in greyscale. There is some reduction in quality, I think due to how the images are converted from wand to opencv. PRs welcome for this.
