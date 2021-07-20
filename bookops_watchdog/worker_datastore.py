# -*- coding: utf-8 -*-

"""
This module provides methods to add, update, and retrieve data from app's datastore
"""


def insert_or_ignore(session, model, **kwargs):
    """
    Adds record to a table (model) or ignores if already exsits based
    on 'wid'

    Args:
        session:                db session
        model:                  datastore module table
        kwargs:                 record arguments
    """
    if "wid" in kwargs:
        instance = session.query(model).filter_by(wid=kwargs["wid"]).first()
    else:
        instance = session.query(model).filter_by(**kwargs).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance
