#!/usr/bin/env python
import sys

import pikepdf


def get_isbn(filename):
    try:
        book = pikepdf.Pdf.open(filename)
        for k, v in book.docinfo.items():
            print(f"{k=}{v=}")
    except Exception as error:
        print(error, sys.stderr)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_isbn(filename))
