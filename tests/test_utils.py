import pytest
import os
import subprocess
import oyaml as yaml
import time
import sys
import datetime
import collections
from collections import OrderedDict, defaultdict

from refchef.utils import *
from refchef.table_utils import *
from refchef import config

@pytest.fixture
def conf():
    d = config.yaml("tests/data/cfg.yaml")
    conf = config.Config(**d)
    return conf

def test_read_yaml():
    data = read_yaml("tests/data/example.yml")
    assert type(data).__name__ == "OrderedDict"
    # ordered_load reads in a YAML as an ordered dictionary, so its type should be OrderedDict

def test_logical():
    case1 = "True"
    case2 = "true"
    case3 = "TRUE"
    case4 = "1"
    case5 = "False"
    case6 = "false"
    case7 = "FALSE"
    case8 = "0"
    case9 = "illogical"
    assert processLogical(case1) == True
    assert processLogical(case2) == True
    assert processLogical(case3) == True
    assert processLogical(case4) == True
    assert processLogical(case5) == False
    assert processLogical(case6) == False
    assert processLogical(case7) == False
    assert processLogical(case8) == False
    assert processLogical(case9) == case9
    # processLogical turns text into its logical equivalent if such exists, so case9 should not be converted

def test_read_menu_from_local(conf):
    a = read_menu_from_local(conf.git_local)
    assert type(a) == dict
