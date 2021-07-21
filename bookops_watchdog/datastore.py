# -*- coding: utf-8 -*-

"""
Watchdog's database models
"""
from datetime import datetime
import os
from contextlib import contextmanager

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()


class DataAccessLayer:
    def __init__(self, mode=None):
        """
        Creates connection to the datastore.
        Args:
            mode:           options: 'test' or None;
                            use 'test' for in-memory db
        """
        if mode == "test":
            self.conn = "sqlite://"
        else:
            self.conn = f"sqlite:///{os.getenv('watchdog_store')}"
        self.engine = None
        self.session = None

    def connect(self):
        self.engine = create_engine(self.conn)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


@contextmanager
def session_scope(mode=None):
    dal = DataAccessLayer(mode)
    dal.connect()
    session = dal.Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class File(Base):
    __tablename__ = "file"
    wid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    handle = Column(String, nullable=False)
    library_wid = Column(Integer, ForeignKey("library.wid"), nullable=False)

    def __repr__(self):
        return (
            f"<File(wid='{self.wid}', timestamp='{self.timestamp}', "
            f"handle='{self.handle}', library_wid='{self.library_wid}')>"
        )


class Library(Base):
    __tablename__ = "library"

    wid = Column(Integer, primary_key=True)
    code = Column(String(3))

    def __repr__(self):
        return f"<Library(wid='{self.wid}', code='{self.code}')>"


class Bib(Base):
    __tablename__ = "bib"
    __table_arg__ = UniqueConstraint("wid", "library_wid")

    wid = Column(Integer, primary_key=True, autoincrement=False)
    library_wid = Column(Integer, ForeignKey("library.wid"), nullable=False)
    bibType = Column(String(1))
    catDate = Column(Date)
    title = Column(String(25), nullable=False)
    author = Column(String(25))
    callNo = Column(String(100))
    callFormat = Column(String(5), nullable=False)
    callAudn = Column(String(1), nullable=False)
    callWl = Column(Boolean, nullable=False)
    callType = Column(String(5))
    callCutter = Column(Boolean, nullable=False)
    callDewey = Column(String)
    allowedBplDiv = Column(Integer)
    subjects = Column(String)
    subjectPerson = Column(Boolean, nullable=False)
    critWork = Column(Boolean, nullable=False)

    orders = relationship("Order", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Bib(wid='{self.wid}', libary_wid='{self.library_wid}', "
            f"bibType='{self.bibType}', catDate='{self.catDate}', "
            f"title='{self.title}')>, "
            f"author='{self.author}', callNo='{self.callNo}', "
            f"callFormat='{self.callFormat}', "
            f"callAudn='{self.callAudn}', callWl='{self.callWl}', "
            f"callType='{self.callType}', "
            f"callCutter='{self.callCutter}', callDewey='{self.callDewey}', "
            f"allowedBplDiv='{self.allowedBplDiv}', subjects='{self.subjects}', "
            f"subjectPerson='{self.subjectPerson}', critWork='{self.critWork}')>"
        )


class Order(Base):
    __tablename__ = "order"
    wid = Column(Integer, primary_key=True, autoincrement=False)
    bib_wid = Column(Integer, ForeignKey("bib.wid"), nullable=False)
    orderDate = Column(Date)
    orderBranches = Column(String)
    orderShelves = Column(String)
    orderAudn = Column(String(1))
    copies = Column(Integer, nullable=False)
    venNote = Column(String)

    def __repr__(self):
        return (
            f"<Order(wid='{self.wid}', bib_wid='{self.bib_wid}', "
            f"orderDate='{self.orderDate}', orderBranches='{self.orderBranches}', "
            f"orderShelves='{self.orderShelves}', orderAudn='{self.orderAudn}', "
            f"copies='{self.copies}', venNote='{self.venNote}')>"
        )


class Conflict(Base):
    __tablename__ = "conflict"
    wid = Column(Integer, primary_key=True)
    tier = Column(String(7))
    code = Column(String(8))
    description = Column(String)

    def __repr__(self):
        return (
            f"<Conflict(wid='{self.wid}', tier='{self.tier}', "
            f"code='{self.code}', description='{self.description}')>"
        )


class Ticket(Base):
    __tablename__ = "ticket"
    wid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    conflict_wid = Column(Integer, ForeignKey("conflict.wid"), nullable=False)
    order_wid = Column(Integer, nullable=False)
    bib_wid = Column(Integer, nullable=False)
    copies = Column(Integer, nullable=False, default=0)
    reported = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return (
            f"<Ticket(wid='{self.wid}', timestamp='{self.timestamp}', "
            f"conflict_wid='{self.conflict_wid}', "
            f"order_wid='{self.order_wid}', bib_wid='{self.bib_wid}', "
            f"copies='{self.copies}', reported='{self.reported}')>"
        )
