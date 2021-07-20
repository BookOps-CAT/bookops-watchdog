from datetime import datetime

import pytest


@pytest.mark.parametrize(
    "arg,expectation",
    [("b122039130", "12203913"), ("o20053174", "2005317"), ("", "")],
)
def test_normalize_sierraNo(arg, expectation, ser):
    assert ser._normalize_sierraNo(arg) == expectation


@pytest.mark.parametrize("arg,expectation", [("1", 1), (2, 2), ("foo", None)])
def test_normalize_copies(arg, expectation, ser):
    assert ser._normalize_copies(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [("01-29-2021", datetime(year=2021, month=1, day=29)), ("foo", None)],
)
def test_normalize_date(arg, expectation, ser):
    assert ser._normalize_date(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (
            "subject1 -- fiction.~subject2 fast~subject3 -- fiction.",
            ["subject1 -- fiction.", "subject3 -- fiction."],
        )
    ],
)
def test_normalize_subjects(arg, expectation, ser):
    assert ser._normalize_subjects(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("Twain, Mark.", "Twain, Mark."),
        ("Twain, Mark, author.", "Twain, Mark."),
        ("A" * 50, "A" * 25),
        ("", None),
    ],
)
def test_normalize_author(arg, expectation, ser):
    assert ser._normalize_author(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("Foo.", "Foo."),
        ("Latvia / Robert Barlas.", "Latvia / Robert Barlas."),
        ("F" * 50, "F" * 25),
    ],
)
def test_normalize_title(arg, expectation, ser):
    assert ser._normalize_title(arg) == expectation
