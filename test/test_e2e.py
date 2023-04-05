# SPDX-License-Identifier: MIT-0
"""
A true end-to-end test which runs the patcher as a separate process.
"""
from filecmp import cmp
from pathlib import Path
from subprocess import run
from pytest import fixture, mark

# Names of files which are expected to be produced by the patcher
EXPECTED_FNAMES = [
    'AnnoFrame_patched_1.dll',
    'AnnoFrame_patched_2.dll',
    'AnnoFrame_patched_3.dll',
    'Texte_patched.dat'
]


@fixture(autouse=True)
def invocation(width: int, height: int, game_path: Path) -> None:
    """Runs the patcher script once until it terminates."""
    args = [
        str(Path(__file__).parent.parent / 'anno-1503-resolution-patcher.py'),
        '-x', str(width),
        '-y', str(height),
        str(game_path)
    ]
    run(args)


@mark.parametrize('fname', EXPECTED_FNAMES)
def test_execution(game_path: Path, patch_path: Path, fname: str):
    """End-to-end test which verifies the generated files."""
    assert cmp(game_path / fname, patch_path / fname, shallow=False)

# The above test is actually suboptimal because we run the patcher multiple
# times per resolution.  We need a way to hierarchically parameterize the
# test, something like this:
#
#     for resolution in resolutions:
#         run the invocation fixture
#         for fname in fnames:
#             run the test under the same invocation
