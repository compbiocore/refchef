import os
from dotenv import load_dotenv
import yaml

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# Add yaml constructor that deals with working directory.
def add_yaml_constructor():
	""" Create wdir function to read in path in yaml file"""
	def wdir(loader, node):
	    seq = loader.construct_sequence(node)
	    return ' '.join(['cd', seq[0]])

	yaml.add_constructor('!wdir', wdir)

add_yaml_constructor()
