import pytest
from refchef.table_utils import *
from refchef.utils import *
from refchef import config

@pytest.fixture # macro to set up a fixture that will be used in other functions.
def menu():
    d = config.yaml("tests/data/cfg.yaml")
    conf = config.Config(**d)

    if sys.platform == 'darwin':
        file_name = 'master_osx.yaml'
    else:
        file_name = 'master_linux.yaml'
    master = read_yaml(os.path.join(conf.git_local, file_name))
    menu = get_full_menu(master)
    return menu

def test_split_filter():
    t = split_filter("1:2")
    assert len(t) == 2
    assert t[0] == "1"
    assert t[1] == "2"

def test_table_columns(menu): #takes the fixture created above as an argument.
    assert menu.shape == (1,9)

def test_filter(menu):
    filtered = filter_menu(menu, "species", "mouse")
    assert filtered.shape == (1,9)
    for i in list(filtered["species"]):
        assert i == "mouse"

    filtered2 = filter_menu(menu, "type", "references")
    for i in list(filtered2["type"]):
        assert i == "references"

def test_multiple_filter(menu):
    s1 = "species:mouse"
    s2 = "species:mouse,type:references"

    f1 = multiple_filter(menu, s1)
    assert f1.shape == (1,9)
    for i in list(f1["species"]):
        assert i == "mouse"

    f2 = multiple_filter(menu, s2)
    print(f2)
    assert f2.shape == (1,9)

    for i in list(f2["species"]):
        assert i == "mouse"

    for i in list(f2["type"]):
        assert i == "references"
