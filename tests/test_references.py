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

def processLogical(text):
	"""
	Turn text into the corresponding logical.

    Arguments:
    text - text to be coerced to a logical, if a corresponding logical exists
	"""
	text = str(text)
	if(text == "true" or text == "True" or text == "TRUE" or text == "T" or text == "t" or text == "1"):
		return True
	elif(text == "false" or text == "False" or text == "FALSE" or text == "F" or text == "f" or text == "0"):
		return False
	else:
		print("Input has no logical analogue.")
		return(text)

def test_references():
	data = ordered_load(open("tests/data/test_master.yaml"))
	rootDirectory = "tests/data/"
	referenceKeys = list(data.keys())
	run = referenceHandler(errorBehavior = False)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, data.get(referenceKeys[k]))
	assert os.path.isfile("tests/data/ucsc_mm9_chr1/primary/final_checksums.md5") 
