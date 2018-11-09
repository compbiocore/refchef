import pytest
from refchef.table_utils import *
from refchef.utils import *
from refchef.config import Config

@pytest.fixture # macro to set up a fixture that will be used in other functions.
def menu():
    conf = Config("tests/data")
    master = read_menu(conf)
    menu = get_full_menu(master)
    return menu

def test_split_filter():
    t = split_filter("1:2")
    assert len(t) == 2
    assert t[0] == "1"
    assert t[1] == "2"

def test_table_columns(menu): #takes the fixture created above as an argument.
    assert menu.shape == (2,6)
    assert list(menu) == ['downloader', 'name', 'organization', 'species', 'type', 'component']

def test_filter(menu):
    filtered = filter_menu(menu, "species", "human")
    assert filtered.shape == (1,6)
    for i in list(filtered["species"]):
        assert i == "human"

    filtered2 = filter_menu(menu, "type", "references")
    for i in list(filtered2["type"]):
        assert i == "references"

def test_multiple_filter(menu):
    s1 = "species:human"
    s2 = "species:human,type:references"

    f1 = multiple_filter(menu, s1)
    assert f1.shape == (1,6)
    for i in list(f1["species"]):
        assert i == "human"

    f2 = multiple_filter(menu, s2)
    assert f2.shape == (1,6)

    for i in list(f2["species"]):
        assert i == "human"

    for i in list(f2["type"]):
        assert i == "references"
