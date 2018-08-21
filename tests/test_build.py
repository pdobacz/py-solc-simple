import pytest
import os

from solc_simple import Builder

def test_compilation_does_not_crash():
    OWN_DIR = os.path.dirname(os.path.realpath(__file__))
    CONTRACTS_DIR = os.path.abspath(os.path.realpath(os.path.join(OWN_DIR, '../priv')))
    OUTPUT_DIR = os.path.abspath(os.path.realpath(os.path.join(OWN_DIR, '../priv/build')))
    builder = Builder(CONTRACTS_DIR, OUTPUT_DIR)
    builder.compile_all()
