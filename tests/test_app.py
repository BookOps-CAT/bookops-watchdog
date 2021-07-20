# -*- coding: utf-8 -*-

"""
Test app.py module
"""
import argparse


from bookops_watchdog.app import (
    createArgParser,
)


def test_createArgParser_correct_obj_returned():
    parser = createArgParser()
    assert type(parser) == argparse.ArgumentParser
