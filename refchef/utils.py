import os
import sys
import subprocess
import yaml
import yamlloader
from collections import OrderedDict, defaultdict

def read_yaml(file_path):
    """Simple function to read yaml file"""
    with open(file_path) as yml:
        dict_ = yaml.load(yml)
    return dict_

def save_yaml(object, file_path):
	"""Saves dict object as yaml file in provided path"""
	yaml.dump(object,
			  open(file_path, 'w'),
			  Dumper=yamlloader.ordereddict.CDumper,
			  indent=2,
			  default_flow_style=False)

def ordered_load(stream, loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    '''
     Load YAML as an Ordered Dict
    :param stream:
    :param loader:
    :param object_pairs_hook:
    :return:
    Borrowed shamelessly from http://codegist.net/code/python2-yaml/
    '''
    class OrderedLoader(loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping
    )
    return yaml.load(stream, OrderedLoader)

def processLogical(text):
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


#TODO split this function to handle platform and path separatly. Need to handle this more gracefully.
def add_path(string, path):
	"""Adds complete path to shell commands
	Arguments: shell command retrieved from yaml file (string)"""
	if ">" in string:
		s = string.split(" > ")
		command = s[0]
		file_name = os.path.join(path, s[1])
		new_s = command + " > " + file_name
		if "*" in new_s:
			new_s_split = new_s.split(" *")
			return new_s_split[0] + " " + os.path.join(path, "*" + new_s_split[1])
		else:
			return new_s

	elif " *" in string:
		s = string.split(" *")
		return s[0] + " " + os.path.join(path, "*" + s[1])
	else:
		return string
