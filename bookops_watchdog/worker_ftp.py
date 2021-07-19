# -*- coding: utf-8 -*-

"""
This module handles communication with Watchdog's FTP
"""
from datetime import datetime, timedelta
from ftplib import FTP, all_errors
import logging
import os
from typing import Dict, List


mlogger = logging.getLogger("bookops-watchdog")


def archive_files(ftp: FTP, files: str) -> None:
    """
    Moves indicated files to a archive directory

    Args:
        ftp:                    ftplib FTP instance
        files:                  fh of files to be archived
    """
    failed = False
    cwd = ftp.pwd()
    for f in files:
        try:
            dst_fh = f"./Archive/{f}"
            ftp.rename(f, dst_fh)
            mlogger.debug(f"FTP: file '{f}' moved from '{cwd}' to archive.")
        except all_errors as exc:
            failed = True
            mlogger.error(
                f"FTP: Unable to move '{f}' from '{cwd}' to archive. Error: '{exc}'"
            )
    if not failed:
        mlogger.info(f"FTP: {len(files)} have been moved from '{cwd}'' to archive.")


def find_unprocessed_files(retrieved: List, processed: List) -> List:
    """
    Compares two lists: retrieved files names and processed file names and
    returns fh that are not present in the processed list

    Args:
        retrieved:              list of file handles retrieved from FTP
        processed:              list of file handles retrieved from datastore

    Returns:
        unprocessed:            list of file handles for processing
    """

    return list(set(retrieved) - set(processed))


def is_aged_out(file_date: datetime, days: int) -> bool:
    """
    Args:
        file_date:              date portion of a QC file
        days:                   number of days since today

    Return:
        boolean
    """
    thresh_hold = datetime.now() - timedelta(days=days)
    if file_date < thresh_hold:
        return True
    else:
        return False


def get_file_date(fh: str) -> datetime:
    """
    Args:                       QC file handle that includes datetime component,
                                example: 'BookOpsQC.20210707063001'

    Returns:
        file_date:              date of file
    """
    date_str = fh[10:].strip()
    return datetime.strptime(date_str, "%Y%m%d%H%M%S")


def find_aged_out_files(files: List, days: int) -> List:
    """
    Identifies files that are older than provided number of days

    Args:
        files:                  list of file handles retrieved from FTP
        days:                   age in days

    Returns:
        aged_out:               list of files ready for achiving
    """
    aged_out = []
    for f in files:
        file_date = get_file_date(f)
        if is_aged_out(file_date, days):
            aged_out.append(f)

    mlogger.debug(f"FTP: identified following aged out files: '{aged_out}'.")
    return aged_out


def ftp_connect(host: str, user: str, passw: str, folder: str, library: str):
    """

    Args:
        host:       ftp host
        user:       ftp user
        passw:      ftp password
        folder:     ftp workspace folder
        library:    'NYPL' or 'BPL'
    """
    ftp = FTP(host)
    conn = ftp.login(user, passw)
    try:
        if conn[:3] == "230":
            mlogger.debug(f"FTP: successfully connected to '{host}'.")
            directory = get_library_directory(folder, library)
            ftp.cwd(directory)
            mlogger.debug(f"FTP: current folder changed to '{directory}'.")
            return ftp
    except all_errors as exc:
        mlogger.error(f"FTP: failed to connect to FTP with follwing error: '{exc}'.")
        return None


def get_ftp_creds_from_env_var() -> Dict:
    """
    Retrieves ftp credentials from environmental variables

    Returns:
        creds:              credentials as dictionary
    """

    creds = dict(
        host=os.getenv("watchdog_ftp_host"),
        user=os.getenv("watchdog_ftp_user"),
        passw=os.getenv("watchdog_ftp_passw"),
        folder=os.getenv("watchdog_ftp_folder"),
    )
    mlogger.info(f"FTP: credentials successfully retrieved from environment variables.")
    return creds


def get_files_in_dir(ftp: FTP) -> List:
    return ftp.nlst()


def get_library_directory(folder, library: str):
    return f"{folder}/{library}"


def retrieve_file(ftp: FTP, file: str, dst_fh: str):
    """
    Downloads file from FTP to local machine

    Args:
        ftp:                ftplib.FTP instance
        file:               file name to be downloaded
        dst_fh:             destination path

    """
    try:
        cwd = ftp.pwd()
        ftp.retrbinary(f"RETR {file}", open(dst_fh, "wb").write)
        mlogger.info(f"FTP: retrieved '{file}' from '{cwd}' for processing.")
    except all_errors as exc:
        mlogger.error(
            f"FTP: Unable to retrieve '{file}' file from '{cwd}'. Error: {exc}"
        )
