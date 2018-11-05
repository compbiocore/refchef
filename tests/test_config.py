import pytest
from refchef.config import *
import argparse
import os
import subprocess
import yaml
import time
import sys
import datetime
import collections
from collections import OrderedDict, defaultdict
import yamlloader


def test_generate_config_3(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "dummy")
    test_conf = config_file()
    #test_conf.input = lambda: 'dummy'
    test_conf.generate_config_3()
    os.path.exists("tests/data/config.yaml")
    # ordered_load reads in a YAML as an ordered dictionary, so its type should be OrderedDict