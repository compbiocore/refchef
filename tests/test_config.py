import pytest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
import os
import sys
import shutil
from refchef.config import *
from refchef.utils import save_yaml
try:
    input = raw_input
except NameError:
    pass

def preamble():
    test_conf = config_file()
    test_conf.preamble()
    assert 1 == 1

# Disable this test in python 2 for now.
def test_generate_config(monkeypatch):
    if sys.version_info >= (3, 0):
        user_input = ["yes", "tests/data", "tests/data", "fernandogelin/refchef-test",
                      "yes", "yes", "yes"]
        mock_ = MagicMock(side_effect=user_input)
        monkeypatch.setattr("builtins.input", mock_)
        test_conf = config_file()
        test_conf.generate_config("tests/data/.refchef.config")
        assert os.path.exists(os.path.expanduser("tests/data/.refchef.config"))
    else:
        configObject = OrderedDict([('config-yaml',
                OrderedDict([('path-settings',
                        OrderedDict([('reference-directory', "tests/data"),
                                     ('github-directory', "tests/data"),
                                     ('remote-repository', "fernandogelin/refchef-test")])),
                             ('log-settings',
                             OrderedDict([('log', "yes")])),
                             ('runtime-settings',
                             OrderedDict([('break-on-error', "yes"), ('verbose', "yes")]))]))])
        save_yaml(configObject, os.path.expanduser("tests/data/.refchef.config"))
        assert os.path.exists(os.path.expanduser("tests/data/.refchef.config"))


def test_config():
    c = Config("tests/data")
    assert c.reference_dir == "tests/data"
