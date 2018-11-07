import pytest
import os
import subprocess
import yaml
from collections import OrderedDict, defaultdict
import yamlloader

from refchef.references import *
from refchef.utils import *

@pytest.fixture
def conf():
    conf = Config("tests/data")
    return conf

def test_references(conf):
	data = ordered_load(open("tests/data/test_master.yaml"))
	rootDirectory = "tests/data/"
	referenceKeys = list(data.keys())
	run = referenceHandler(conf, errorBehavior = False)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, data.get(referenceKeys[k]))
	assert os.path.isfile("tests/data/ucsc_mm9_chr1/primary/chr1.fa.gz")


def test_new_append(conf):
	f1 = "test_master.yaml"
	f2 = "example.yml"
	new_append(f1,f2,conf)
