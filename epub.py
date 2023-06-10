#!/usr/bin/env python
import sys

from ebooklib import epub


def get_isbn(filename):
    try:
        book = epub.read_epub(filename)
        return book.metadata["http://purl.org/dc/elements/1.1/"]["identifier"][0][0]
    except Exception as error:
        print(error, sys.stderr)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_isbn(filename))
