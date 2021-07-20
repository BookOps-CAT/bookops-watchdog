# -*- coding: utf-8 -*-

"""
This module includes methods for parsing Sierra reports
"""
from collections import namedtuple
import csv
from datetime import datetime
import logging


mlogger = logging.getLogger("bookops-watchdog")


Row = namedtuple(
    "Row",
    [
        "bibNo",
        "catDate",
        "recType",
        "title",
        "author",
        "callNo",
        "subjects",
        "orderNo",
        "orderDate",
        "locations",
        "copies",
        "venNotes",
        "status",
    ],
)

# Record = namedtuple()


class SierraExportReader(object):
    def __init__(self, fh: str):
        self.fh = fh

        self._length = None

    def __iter__(self):
        mlogger.debug(f"Intitating parsing of a Sirra export.")
        self._length = 0
        with open(self.fh, "r") as f:
            reader = csv.reader(f, delimiter="^")
            reader.__next__()
            for row in map(Row._make, reader):
                data = self._normalize_data(row)
                self._length += 1
                yield data

    def __len__(self):
        if self._length is None:
            for row in self:
                continue
        return self._length

    def _normalize_data(self, row):
        bibNo = self._normalize_sierraNo(row.bibNo)
        orderNo = self._normalize_sierraNo(row.orderNo)
        catDate = self._normalize_date(row.catDate)
        orderDate = self._normalize_date(row.orderDate)
        copies = self._normalize_copies(row.copies)
        title = self._normalize_title(row.title)
        author = self._normalize_desc(row.author)
        subjects = self._normalize_subjects(row.subjects)
        record = dict(
            author=author,
            bibNo=bibNo,
            catDate=catDate,
            orderDate=orderDate,
            orderNo=orderNo,
            copies=copies,
            subjects=subjects,
            title=title,
        )
        return record

    def _normalize_copies(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            mlogger.debug(f"Unable to parse quantity from value '{value}'")
            return None

    def _normalize_sierraNo(self, value):
        return value[1:-1]

    def _normalize_date(self, value):
        try:
            date = datetime.strptime(value, "%m-%d-%Y")
            return date
        except ValueError:
            mlogger.debug(f"Unable to parse date from value '{value}'")
            return None

    def _normalize_subjects(self, value):
        subs = [s for s in value.split("~") if "fast" not in s]
        return subs

    def _normalize_title(self, value):
        return value[:25].strip()

    def _normalize_author(self, value):
        author = value[:25].replace(", author.", ".").strip()
        if author != "":
            return author
        else:
            return None
