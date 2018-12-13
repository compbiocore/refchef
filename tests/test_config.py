import pytest
import os
import sys
import shutil
from refchef import config
try:
    input = raw_input
except NameError:
    pass


def test_config_yaml():
    d = config.yaml("tests/data/cfg.yaml")
    c = Config(**d)
    assert c.reference_dir == "tests/data"
    assert len(d) == 6

def test_config_ini():
    d = config.ini("tests/data/cfg.ini")
    c = Config(**d)
    assert c.reference_dir == "tests/data"
    assert len(d) == 6
