import pytest
from refchef.github_utils import *
from refchef import config
import collections
import os

@pytest.fixture
def conf():
    d = config.yaml("tests/data/cfg.yaml")
    conf = config.Config(**d)
    return conf

def test_read_menu_from_github(conf):
     a = read_menu_from_github(conf)
     assert type(a) == dict

def test_setup_git(conf):
    dir, tree = setup_git(conf)
    assert dir == 'tests/data/.git'
    assert tree == 'tests/data/'

def test_read_menu_from_github(conf):
    d = read_menu_from_github(conf)
    assert type(d) == collections.OrderedDict
