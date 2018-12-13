import pytest
from refchef.github_utils import *
from refchef import config

@pytest.fixture
def conf():
    d = config.yaml("tests/data/cfg.yaml")
    conf = config.Config(**d)
    return conf

def test_read_menu_from_github(conf):
     a = read_menu_from_github(conf)
     assert type(a) == dict
