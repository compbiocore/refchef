import argparse
import os
import subprocess
import yaml
import time
import sys
import datetime
import collections
from collections import OrderedDict, defaultdict
import shutil
import yamlloader
try:
    input = raw_input
except NameError:
    pass

class config_file():
	def __init__(self, filetype="yaml"):
		self.filetype = filetype

	@staticmethod
	def preamble():
		"""Print out the preamble, which is not version-specific."""
		print("This interactive prompt will allow you to generate a config file for this tool.")
		print("If asked to provide a filepath, please provide the full, absolute filepath, with no ~.")
		print("Furthermore, please do not append a trailing '/' to the filepaths.")
		print("If you leave your response to a prompt empty, that entry will not be generated.")


	@staticmethod
	def generate_config():
		"""Generate a human-readable configuration YAML for running the software proper.

		This version of generateConfig() uses an ordered dictionary to generate its YAML.

		This version is for Python 3 and uses input()."""
		print("\033[1m" + "This operation will overwrite any existing config.yaml.  Type 'yes' to proceed, or anything else to exit." + "\033[0m")
		continue_prompt = input("> ")
		if continue_prompt != "yes":
			sys.exit("Exiting without action.")
		print("\033[1m" + "Filepaths" + "\033[0m")
		print("What is the filepath of the directory to be used as root for the references? (Required)")
		root_dir = input("> ")
		if "~" in root_dir:
			sys.exit("Please try again without using ~.")
		if root_dir != "":
			print("do nothing")
		else:
			sys.exit("Required option omitted; exiting.")
		print("What is the " + "\033[1m" + "local" + "\033[0m" + " Github repository directory (parent directory of cloned repos)?")
		local_git_dir = input("> ")
		if "~" in local_git_dir:
			sys.exit("Please try again without using ~.")
		if local_git_dir != "":
			print("do nothing")
		print("What is the " + "\033[1m" + "remote" + "\033[0m" + " Github repo in the format 'USER/REPO'?")
		remote_git_name = input("> ")
		if remote_git_name != "":
			print("do nothing")
		print("\033[1m" + "Logging" + "\033[0m")
		print("Should logs be generated?  Type 'True' or 'False'. (Default: True)")
		log_setting = input("> ")
		if log_setting == "":
			log_setting = "True"
		print("\033[1m" + "Runtime Settings" + "\033[0m")
		print("Should the tool end its run on any error?  Type 'True' or 'False'. (Default: True)")
		break_on_error = input("> ")
		if break_on_error == "":
			break_on_error = "True"
		print("Should the tool be verbose (generate lots of stepwise output)? (Default: False)")
		verbose = input("> ")
		if verbose == "":
			verbose = "False"
		configObject = OrderedDict([('config-yaml', OrderedDict([('path-settings', OrderedDict([('reference-directory', str(root_dir)), ('github-directory', str(local_git_dir)), ('remote-repository', str(remote_git_name))])), ('log-settings', OrderedDict([('log', str(log_setting))])), ('runtime-settings', OrderedDict([('break-on-error', str(break_on_error)), ('verbose', str(verbose))]))]))])
		yaml.dump(configObject, open('config.yaml', 'w'), Dumper=yamlloader.ordereddict.CDumper, indent=4, default_flow_style=False)
		current_time = datetime.datetime.now().strftime(("%Y-%m-%d_%H:%M"))
		backup_path = "config_backup_" + current_time + ".yaml"
		shutil.copyfile("config.yaml",backup_path)
		print("Generated config file and timestamped backup.")
		print("To use this backup in the future, simply copy it to a file named 'config.yaml'.")
