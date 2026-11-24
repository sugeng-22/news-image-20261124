#!/usr/bin/env python3
"""Entry program: copy the bundled infographic to /output/entry.png.

Standard library only, no network, fully deterministic: the same input
bytes always produce the same output bytes. The image itself is rendered
from scratch by generate.py (Pillow) from the bundled hero illustration.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
