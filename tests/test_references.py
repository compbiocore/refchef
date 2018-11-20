import pytest
import os
import subprocess
import yaml
from collections import OrderedDict, defaultdict
import yamlloader
import shutil
from refchef.references import *
from refchef.utils import *

@pytest.fixture
def conf():
    conf = Config("tests/data")
    return conf

def test_references(conf):
	if sys.platform == 'darwin':
		shutil.copy("tests/data/master_osx.yaml", "tests/data/master.yaml")
	else:
		shutil.copy("tests/data/master_linux.yaml", "tests/data/master.yaml")
	data = ordered_load(open("tests/data/master.yaml"))
	rootDirectory = os.path.join(os.getenv('HOME'), 'build/compbiocore/refchef', 'tests/data')
	referenceKeys = list(data.keys())
	run = referenceHandler(conf, errorBehavior = False)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, data.get(referenceKeys[k]))
	os.chdir(os.path.join(os.getenv('HOME'), 'build/compbiocore/refchef'))
	assert os.path.isfile("tests/data/reference_test1/primary/chr1.fa")

def test_new_append(conf):
	f1 = "tests/data/test_master.yaml"
	f2 = "example.yml"
	new_append(f1,f2,conf)
