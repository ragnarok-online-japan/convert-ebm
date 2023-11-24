#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2023 MINETA "m10i" Hiroki & Ragnarok Online Japan デベロッパー

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import os
import re
import zlib


parser = argparse.ArgumentParser(description='Convert Ragnarok ebm to image')

parser.add_argument("ebmfile",
                    action="store",
                    default=None,
                    type=str,
                    help="Ragnarok ebm file")

args = parser.parse_args()

def main(args):
    raw_image: bytes = None

    with open(args.ebmfile, mode="rb") as fp:
        raw_image = zlib.decompress(fp.read())

    if len(raw_image) == 0:
        return

    basename_without_ext: str = os.path.splitext(os.path.basename(args.ebmfile))[0]
    dirname: str = os.path.dirname(args.ebmfile)

    ext: str = "bin"
    if bool(re.match(b"^\x42\x4d", raw_image[:2])):
        ext = "bmp"
    elif bool(re.match(b"^\x47\x49\x46\x38", raw_image[:4])):
        ext = "gif"

    filename = os.path.join(dirname, f"{basename_without_ext}.{ext}")
    with open(filename, mode="wb") as fp:
        fp.write(raw_image)

if __name__ == "__main__":
    main(args)
