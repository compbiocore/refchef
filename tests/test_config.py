import pytest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import os
import sys
import shutil
from refchef.config import *

def preamble():
    test_conf = config_file()
    test_conf.preamble()
    assert 1 == 1

def test_generate_config(monkeypatch):
    user_input = ["yes", "tests/data", "tests/data", "fernandogelin/refchef-test",
                  "yes", "yes", "yes"]
    mock = MagicMock(side_effect=user_input)
    monkeypatch.setattr("builtins.input", mock)
    test_conf = config_file()
    test_conf.generate_config("tests/data/.refchef.config")
    assert os.path.exists(os.path.expanduser("tests/data/.refchef.config"))

def test_config():
    c = Config("tests/data")
    assert c.reference_dir == "tests/data"
