# SPDX-License-Identifier: MIT-0

from os import listdir
from re import match
from pathlib import Path
from typing import Iterator, Tuple
from tempfile import TemporaryDirectory
from shutil import copyfile
from pytest import fixture

DATA_PATH = Path(__file__).parent / 'data'


@fixture
def game_path() -> Iterator[Path]:
    """Provides a temporary game path with test data."""
    with TemporaryDirectory() as game_dir:
        result = Path(game_dir)
        for fname in ['AnnoFrame.dll', 'Texte.dat']:
            copyfile(DATA_PATH / fname, result / fname)
        yield result


@fixture(params=[n for n in listdir(DATA_PATH) if match(r'\d+x\d+$', n)])
def patch_path(request) -> str:
    """Provides the path to the expected data files."""
    return Path(__file__).parent / 'data' / request.param


@fixture
def resolution(patch_path: Path) -> Tuple[int, int]:
    """Provides the name of a resolution"""
    name = patch_path.parts[-1]
    parts = tuple(int(i) for i in name.split('x'))
    return (parts[0], parts[1])


@fixture
def width(resolution: Tuple[int, int]) -> int:
    """Provides the width of a given resolution tuple."""
    return resolution[0]


@fixture
def height(resolution: Tuple[int, int]) -> int:
    """Provides the height of a given resolution tuple."""
    return resolution[1]
