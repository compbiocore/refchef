import pytest
from refchef.github_utils import *
from refchef.config import Config

@pytest.fixture
def conf():
    conf = Config("tests/data")
    return conf

def test_read_menu_from_github(conf):
     a = read_menu_from_github(conf)
     assert type(a) == dict
