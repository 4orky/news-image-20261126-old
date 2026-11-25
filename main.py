#!/usr/bin/env python3
"""news-image-20261126: place the entry image at /output/entry.png.

The front page itself is drawn by render.py (Pillow, render time)
and shipped in this repository as entry.png. This entrypoint only
copies those exact bytes, using nothing but the standard library,
so it runs with no network and every run writes the same file.
It refuses to write anything that is not a PNG within the
bounty's limits (at most 1 MiB, at most 1024 by 1024 pixels).
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                      "entry.png")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def check_png(data):
    """Exit non-zero unless data is a PNG inside the bounty limits."""
    if len(data) > MAX_BYTES:
        sys.exit("error: entry.png is %d bytes, over the 1 MiB cap"
                 % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        sys.exit("error: entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit("error: entry.png is %dx%d, over the 1024x1024 cap"
                 % (width, height))
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        sys.exit("error: entry.png is missing from the repository")
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    width, height = check_png(data)
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(data)
    with open(TARGET, "rb") as handle:
        written = handle.read()
    if sha256_hex(written) != sha256_hex(data):
        sys.exit("error: written bytes differ from entry.png")
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (TARGET, len(data), width, height, sha256_hex(data)))


if __name__ == "__main__":
    main()
