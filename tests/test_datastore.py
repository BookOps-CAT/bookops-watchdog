# -*- coding: utf-8 -*-
import os

import pytest

from bookops_watchdog.datastore import (
    Bib,
    Conflict,
    DataAccessLayer,
    File,
    Library,
    Order,
    Ticket,
    session_scope,
)


def test_bib_tbl_repr():
    bib = Bib(
        library_wid=1,
        bibType="b",
        bibItemForm=None,
        bibWl=False,
        bibAudn="j",
        bibPhysicalDesc="1 volume",
        catDate="2021-07-01",
        title="Foo",
        author="Bar",
        callNoStaff="ABC",
        callNoBot="ABD",
        callFormat="print",
        callAudn="j",
        callWl=False,
        callType="dew",
        callCutter=True,
        callDewey="111",
        allowedBplDiv=16,
        subjects="foo-bar",
        subjectPerson=False,
        critWork=False,
    )
    assert (
        str(bib)
        == "<Bib(wid='None', libary_wid='1', bibType='b', bibItemForm='None', bibWl='False', bibAudn='j', bibPhysicalDesc='1 volume', catDate='2021-07-01', title='Foo', author='Bar', callNoStaff='ABC', callNoBot='ABD', callFormat='print', callAudn='j', callWl='False', callType='dew', callCutter='True', callDewey='111', allowedBplDiv='16', subjects='foo-bar', subjectPerson='False', critWork='False')>"
    )


def test_conflict_tbl_repr():
    conflict = Conflict(wid=1, tier="Foo", code="bar", description="spam")
    assert (
        str(conflict)
        == "<Conflict(wid='1', tier='Foo', code='bar', description='spam')>"
    )


def test_DataAccessLayer_evn_var_conn(mock_all_env_variables):
    assert (
        DataAccessLayer().conn
        == "sqlite:///C:\\Users\\Foo\\APPDATA\\TEMP\\Bookops-Watchdog\\datastore.db"
    )


# def test_DataAccessLayer_test_conn():
#     assert DataAccessLayer().conn == "sqlite://"


def test_file_tbl_repr():
    file = File(wid=1, timestamp="2021-07-01-07:01", handle="foo.txt", library_wid=1)
    assert (
        str(file)
        == "<File(wid='1', timestamp='2021-07-01-07:01', handle='foo.txt', library_wid='1')>"
    )


def test_library_tbl_repr():
    assert str(Library(wid=1, code="foo")) == "<Library(wid='1', code='foo')>"


def test_order_tbl_repr():
    order = Order(
        bib_wid=1,
        orderDate="2021-07-01",
        orderBranches="41,50,16",
        orderShelves="afc",
        orderAudn="a",
        copies=20,
        venNote="nfc",
    )
    assert (
        str(order)
        == "<Order(wid='None', bib_wid='1', orderDate='2021-07-01', orderBranches='41,50,16', orderShelves='afc', orderAudn='a', copies='20', venNote='nfc')>"
    )


def test_session_scope_returns_correct_obj():
    with session_scope() as s:
        assert str(type(s)) == "<class 'sqlalchemy.orm.session.Session'>"


def test_ticket_tbl_repr():
    issue = Ticket(
        wid=1,
        timestamp="2021-07-01-07:01",
        conflict_wid=2,
        order_wid=3,
        bib_wid=4,
        copies=10,
        reported=False,
    )
    assert (
        str(issue)
        == "<Ticket(wid='1', timestamp='2021-07-01-07:01', conflict_wid='2', order_wid='3', bib_wid='4', copies='10', reported='False')>"
    )
