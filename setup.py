from setuptools import setup, find_packages


setup(
    name="pdf-question-spacer",
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True,
    python_requires='>=3.5',
    url="https://github.com/LaurenceWarne/pdf-question-spacer",
    scripts=['bin/space-pdf-interactive'],
    entry_points={
        "console_scripts":
        [
            "space-pdf=pdf_question_spacer.space_pdf:main",
        ],
    },
    version="1.0.3",
    author="Laurence Warne",
    license="MIT",
    install_requires=[
        "numpy",
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
