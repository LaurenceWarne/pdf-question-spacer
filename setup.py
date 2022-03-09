from setuptools import setup, find_packages


setup(
    name="pdf-question-spacer",
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True,
    python_requires='>=3.7',
    url="https://github.com/LaurenceWarne/pdf-question-spacer",
    scripts=['bin/space-pdf-interactive'],
    entry_points={
        "console_scripts":
        [
            "space-pdf=pdf_question_spacer.space_pdf:main",
        ],
    },
    version="1.0.2",
    author="Laurence Warne",
    license="MIT",
    install_requires=[
        "numpy==1.21.0",
        "opencv-python",
        "pytesseract",
        "fuzzywuzzy",
        "matplotlib",
        "python-Levenshtein",
        "pdf2image",
        "Pillow"
    ],
    zip_safe=False
)
