# -*- coding: utf-8 -*-

import os
from shutil import copyfile

import pytest

from bookops_watchdog.worker_drive import (
    find_unprocessed_files,
    get_sierra_files,
    is_sierra_export,
)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),
        (None, False),
        ("abc", False),
        ("F" * 25, False),
        ("BookOpsQCb.aaaaaaaaaaaaaa", False),
        ("BookOpsQCb.20210730063001", True),
        ("BookOpsQCn.20210730063001", True),
    ],
)
def test_is_sierra_export(arg, expectation):
    assert is_sierra_export(arg) == expectation


@pytest.mark.parametrize(
    "arg1,arg2,expectation",
    [
        ([], [], []),
        ([], ["BookOpsQCb.20210730063001"], []),
        (["BookOpsQCb.20210701063001"], [], ["BookOpsQCb.20210701063001"]),
        (
            [
                "BookOpsQCb.20210701063001",
                "BookOpsQCb.20210702063001",
                "BookOpsQCb.20210703063001",
            ],
            ["BookOpsQCb.20210701063001", "BookOpsQCb.20210703063001"],
            [
                "BookOpsQCb.20210702063001",
            ],
        ),
    ],
)
def test_find_unprocessed_files(arg1, arg2, expectation):
    assert find_unprocessed_files(arg1, arg2) == expectation


@pytest.mark.parametrize(
    "arg1,arg2",
    [
        ("bpl", "BookOpsQCb.20210801603001"),
        ("nypl", "BookOpsQCn.20210801603001"),
    ],
)
def test_get_sierra_files(arg1, arg2, tmpdir):
    root = tmpdir.mkdir("BookOpsWatchdog")
    os.environ["watchdog_drive"] = str(root)
    os.mkdir(os.path.join(root, arg1.upper()))
    src = os.path.join("tests", arg2)
    dst = os.path.join(os.path.join(root, arg1.upper()), arg2)
    copyfile(src, dst)
    files = get_sierra_files(arg1)
    assert files == [arg2]
