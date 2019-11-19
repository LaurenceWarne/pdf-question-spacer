# pdf-question-spacer

## Intro

pdf-question-spacer is a tool used to add whitespace to pdfs. It allows for the addition of whitespace to sections of a pdf matching a regular expression, whilst also ensuring page breaks do not cut off shifted text.

For example with the command:

```
space-pdf sample.pdf 300  # Defaults to spacing lines starting with numbers
```

we can transform sample.pdf:

![Image before script](https://i.imgur.com/cFI1aQIl.jpg)

into:

![Image after script](https://i.imgur.com/WmypxoVl.png)

More specifically, if ```R``` is a vertical region whose text matches the specified regular expression, then the specified amount of whitespace (300 in our case) is added *above* ```R```.

## Installation

```
python3 setup.py install --user
```

[ImageMagick](https://imagemagick.org/index.php) and [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) are also required.

## Usage

```
usage: space-pdf [-h] [-r REGEXES [REGEXES ...]] [-ir] [-c COLOUR] [-s1] [-d]
                 [--dpi DPI]
                 infile whitespace_length

Add whitespace to sections of pdfs and output the resulting images as pngs.

positional arguments:
  infile                name of pdf to add whitespace to
  whitespace_length     Number of lines of whitespace to add per match (in
                        pixels), default is 400

optional arguments:
  -h, --help            show this help message and exit
  -r REGEXES [REGEXES ...], --regexes REGEXES [REGEXES ...]
                        Match lines with these regular expressions, in
                        addition to the default regex which matches lines
                        which appear to be the start of questions
  -ir, --ignore-default-regex
                        Do not use the default regex which matches lines which
                        appear to be the start of questions. To use this
                        option you must also use the --regexes option
  -c COLOUR, --colour COLOUR
                        Colour of the whitespace, default 255 (white)
  -s1, --skip-first     Skip first regular expression match
  -d, --debug           Show the text extracted from the pdf regions, along
                        with the corresponging region in a matplotlib figure
  --dpi DPI             The image quality, default is 400. This is passed
                        directly to pdf2image.convert_from_path(), also note
                        using large values will take longer and may cause
                        crashes!
```

png files will then be created in the working directory and can be converted to a pdf. For example using ImageMagick:

```
convert out* -page A4 my-new-pdf.pdf
```

## Limitations

Currently only outputs images in greyscale.
