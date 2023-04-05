#!/usr/bin/env python3
# SPDX-License-Identifier: MIT-0

# MIT No Attribution
#
# Copyright 2023 Alejandro "HiPhish" Sanchez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
File patcher for Anno 1503 which adds alternate resolutions to the game.  The
script reads the original game files and writes patched version into the
directory of the game.
"""

import re
import io
import argparse as ap
from pathlib import Path
from dataclasses import dataclass


def int_to_bytes(i: int) -> bytes:
    """
    Convert an integer value to its little-endian notation four-byte string.
    """
    return i.to_bytes(length=4, byteorder='little')


@dataclass
class Resolution():
    x: int
    y: int

    def __repr__(self):
        """Text representation suitable for use in in-game menu."""
        return f'{self.x}x{self.y}'

    def to_patch(self, to_preserve: bytes) -> bytes:
        """Produces a patch byte string to overwrite the original data with."""
        return int_to_bytes(self.x) + to_preserve + int_to_bytes(self.y)

    def to_regex(self) -> bytes:
        """
        Produces a regular expression to search for this resolution in the DLL.
        """
        return int_to_bytes(self.x) + b'(.{4})' + int_to_bytes(self.y)


# The old resolution we will overwrite
OLD_RES = Resolution(x=1280, y=1024)
# Resolutions which are known to work
GOOD_RESOLUTIONS = (
    Resolution(x=1280, y=800),
    Resolution(x=1366, y=768),
    Resolution(x=1400, y=1050),
    Resolution(x=1440, y=900),
    Resolution(x=1600, y=900)
)
# Encoding of the text file used by the game
ENCODING = 'latin1'


if __name__ == '__main__':
    parser = ap.ArgumentParser(
        description='''
Patches Anno 1503 files to support custom resolutions.  The script creates one
or more patched DLL files and a patched text file.  Replace the original text
file with the patched one, and try out the patched DLL files until one of them
works.  The patched files will be written to the game directory, original files
are not modified.
        ''',
        epilog=f'''The following resultions are known to work:
  - {"""
  - """.join(str(r) for r in GOOD_RESOLUTIONS)}
''',
        formatter_class=ap.RawTextHelpFormatter,
    )
    parser.add_argument(
        '-x', '--width', type=int, default=GOOD_RESOLUTIONS[-1].x,
        help=f'Target resolution width (default {GOOD_RESOLUTIONS[-1].x})')
    parser.add_argument(
        '-y', '--height', type=int, default=GOOD_RESOLUTIONS[-1].y,
        help=f'Target resolution height (default {GOOD_RESOLUTIONS[-1].y})')
    parser.add_argument(
        'path', type=str, default='.', nargs='?',
        help='Path to the game directory (default current working directory)')
    args = parser.parse_args()

    target_res = Resolution(x=args.width, y=args.height)
    game_path = Path(args.path)

    with open(game_path / 'AnnoFrame.dll', 'rb') as dll_input:
        dll = dll_input.read()

    with open(game_path / 'Texte.dat', 'rt', encoding=ENCODING) as text_input:
        text = text_input.read()

    new_text = re.sub(f'\n{OLD_RES}\n', f'\n{target_res}\n', text)

    for i, match in enumerate(re.finditer(OLD_RES.to_regex(), dll), 1):
        substitute = target_res.to_patch(match[1])
        result = dll[:match.start()] + substitute + dll[match.end():]
        with open(game_path / f'AnnoFrame_patched_{i}.dll', 'wb') as out:
            out.write(result)

    with open(game_path / 'Texte_patched.dat', 'wt', encoding=ENCODING, newline='\r\n') as output:
        output.write(new_text)


# How it works
# ============
#
# The DLL file 'AnnoFrame.dll' has the game's resolutions hard-coded in it.
# The patcher goes through the file and tries to replace the largest of these
# resolutions with our desired values.  However, the exact offset into the DLL
# file varies depending on the build of the game, so we create a different
# patched DLL for each match.  Only one of these will actually work and the
# player will have to try them out by hand.
#
# The largest original resolution is 1280 x 1024 (0x500 x 0x400 in hexadecimal
# notation).  The numbers are stored in little-endian notation and there are
# four bytes (octets) between the two values.
#
# For each match we replace the old values while keeping the four bytes between
# them intact, then we write out the patched DLL.  Finally we modify the
# 'Texte.dat' file to swap out the label of the resolution in the in-game menu.
#
# Source:
# https://www.annozone.de/forum/index.php?page=Thread&threadID=16090
