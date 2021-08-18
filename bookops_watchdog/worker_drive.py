# -*- coding: utf-8 -*-

"""
This module handles retrieval of Sierra exports from a shared drive
"""
from datetime import datetime
import logging
import os
from typing import List


mlogger = logging.getLogger("bookops-watchdog")


def is_sierra_export(file_handle: str) -> bool:
    """
    Returns only file handles that follow Sierra export naming schema

    Args:
        file_handle:            file handle

    Returns:
        boolean
    """

    if not isinstance(file_handle, str):
        return False

    if len(file_handle) != 25:
        return False

    if file_handle[:11] not in ("BookOpsQCb.", "BookOpsQCn."):
        return False

    try:
        datetime.strptime(file_handle[11:], "%Y%m%d%H%S%f")
    except ValueError:
        return False

    return True


def find_unprocessed_files(delivered: List[str], processed: List[str]) -> List[str]:
    """
    Compares two lists: delivered files names and processed file names and
    returns fh that are not present in the processed list

    Args:
        delivered:              list of file handles delivered from Sierra files
        processed:              list of file handles retrieved from datastore

    Returns:
        unprocessed:            list of file handles for processing
    """
    extra_files = list(set(delivered) - set(processed))
    unprocessed = []
    for fh in extra_files:
        if is_sierra_export(fh):
            unprocessed.append(fh)
    return unprocessed


def get_sierra_files(library: str) -> List[str]:
    """
    Returns all files in given folder

    Args:
        folder:                 directory's path
        library                 relevant library: 'bpl' or 'nypl'
    """
    root_dir = os.getenv("watchdog_drive")
    directory = os.path.join(root_dir, library.upper())
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    return files
