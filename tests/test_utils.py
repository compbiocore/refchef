import pytest
from refchef.utils import *
import os
import subprocess
import yaml
import time
import sys
import datetime
import collections
from collections import OrderedDict, defaultdict

def test_ordered_load():
    print(os.getcwd())
    data = ordered_load(open("tests/data/example.yml"))
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

def test_add_path():
    s = "md5 *.fa > final_checksums.md5"
    assert add_path(s, "test/") == "md5 *.fa > test/final_checksums.md5"