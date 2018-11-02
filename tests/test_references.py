import pytest
from refchef.references import *
from refchef.utility_functions import *
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


def test_references():
	data = ordered_load(open("tests/data/test_master.yaml"))
	rootDirectory = "tests/data/"
	referenceKeys = data.keys()
	run = referenceHandler(errorBehavior = False)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, data.get(referenceKeys[k]))
	assert os.path.isfile("tests/data/ucsc_mm9_chr1/primary/final_checksums.md5") 