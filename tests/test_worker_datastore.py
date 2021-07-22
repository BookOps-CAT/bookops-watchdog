# -*- coding: utf-8 -*-

import pytest


from bookops_watchdog.worker_datastore import insert_or_ignore
from bookops_watchdog.datastore import Library


def test_insert_or_ignore_insert(mock_datastore_session):
    rec = insert_or_ignore(mock_datastore_session, Library, code="bpl")
    mock_datastore_session.commit()
    assert rec.wid == 1
    assert rec.code == "bpl"


def test_insert_or_ignore_wid_dup_ignore(mock_datastore_session):
    s = mock_datastore_session
    rec1 = Library(code="bpl")
    s.add(rec1)
    s.commit()

    rec2 = insert_or_ignore(s, Library, wid=1, code="foo")
    assert rec2.wid == 1
    assert rec2.code == "bpl"


def test_insert_or_ignore_not_unique_ignore(mock_datastore_session):
    s = mock_datastore_session
    rec1 = Library(code="bpl")
    s.add(rec1)
    s.commit()

    rec2 = insert_or_ignore(s, Library, code="bpl")
    s.add(rec2)
    s.commit()
    assert rec2.wid == 1
