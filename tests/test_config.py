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

def preamble():
    test_conf = config_file()
    test_conf.preamble()
    assert 1 == 1

def test_generate_config(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: "yes")
    test_conf = config_file()
    test_conf.generate_config()
    assert os.path.exists("config.yaml")
