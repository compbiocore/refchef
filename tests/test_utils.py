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
    if sys.platform == 'darwin':
        file_name = 'new_osx.yaml'
    else:
        file_name = 'new_linux.yaml'
    p = os.path.join('tests/data', file_name)
    data = read_yaml(p)
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
    assert process_logical(case1) == True
    assert process_logical(case2) == True
    assert process_logical(case3) == True
    assert process_logical(case4) == True
    assert process_logical(case5) == False
    assert process_logical(case6) == False
    assert process_logical(case7) == False
    assert process_logical(case8) == False
    assert process_logical(case9) == case9
    # process_logical turns text into its logical equivalent if such exists, so case9 should not be converted
