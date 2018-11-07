import pytest
from refchef.github_utils import *


def test_read_menu_from_github():
    a, b = read_menu_from_github()
    assert type(b) == str
