import pytest
from refchef.table_functions import *

@pytest.fixture
def menu():
    menu = get_full_menu("tests/data/example.yml")
    return menu

def test_table_columns(menu):
    assert menu.shape == (6,6)
    assert list(menu) == ['downloader', 'name', 'organization', 'species', 'type', 'component']

def test_filter(menu):
    filtered = filter_menu(menu, "species", "human")
    assert filtered.shape == (5,6)
    for i in list(filtered["species"]):
        assert i == "human"
