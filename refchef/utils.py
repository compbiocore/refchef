import os
import sys
import subprocess
import oyaml as yaml
import yamlloader
from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from future.utils import iteritems
import hiyapyco

def read_yaml(file_path):
    """Simple function to read yaml file"""
    with open(file_path) as yml:
        dict_ = yaml.full_load(yml)
    return dict_

def save_yaml(object, file_path):
    """Saves dict object as yaml file in provided path"""
    yaml.dump(object,
              open(file_path, 'w'),
              Dumper=yamlloader.ordereddict.CDumper,
              indent=2,
              default_flow_style=False)

def merge_yaml(master, new):
    """Merge yaml files"""
    conf = hiyapyco.load(master,
                         new,
                         method=hiyapyco.METHOD_MERGE,
                         interpolate=True,
                         failonmissingfiles=True,
                         mergelists=False,
                         loglevel='ERROR')

    save_yaml(conf, master)

def process_logical(text):
    """
    Turn text into the corresponding logical.

    Arguments:
    text - text to be coerced to a logical, if a corresponding logical exists
    """
    text = str(text)
    if(text == "true" or text == "True" or text == "TRUE" or text == "T" or text == "t" or text == "1" or text.lower() == 'yes'):
        return True
    elif(text == "false" or text == "False" or text == "FALSE" or text == "F" or text == "f" or text == "0" or text.lower() == 'no'):
        return False
    else:
        print("Input has no logical analogue.")
        return(text)


def singular(str_):
    if str_ == 'annotations':
        return 'annotation'
    elif str_ == 'references':
        return 'reference'
    elif str_ == 'indices':
        return 'index'

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
