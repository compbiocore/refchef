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
#from inspect import getouterframes, currentframe
#import yamlordereddictloader
import yamlloader
import urllib2

parser = argparse.ArgumentParser(description='Controls how to run the reference parser')
subs = parser.add_subparsers(dest='command')


local_parser = subs.add_parser('local')
local_parser.add_argument('-e', '--execute', help = 'Executes the YAML file, either the new if it exists or the master if not', action='store_true')
local_parser.add_argument('--master', type=str, required = True, help = 'Denotes the Master YAML')
local_parser.add_argument('--new', type=str, help = 'Denotes the new YAML')
local_parser.add_argument('--skip', help = 'Skip appending the new YAML (mainly for testing)', action="store_true")
# check for --master and --new FIRST to determine the mode, then check --execute to determine what to do
# do not allow running both the --new and the --master in one command
# if --new exists and --execute is TRUE, run the --new and append --new to --master (subject to --skip in testing)
# if --new exists and --execute is FALSE, do not run anything and just append --new to --master (subject to --skip in testing)
# if --new does not exist and --execute is TRUE, run the --master
# if --new does not exist and --execute is FALSE, exit with an error, as this combination is pointless

remote_parser = subs.add_parser('remote')
remote_parser.add_argument('--url', type=str, required = True, help = 'Denotes the URL of the remote file')
remote_parser.add_argument('--download', help = 'Download a copy of the file to the working directory', action="store_true")




# Parse arguments
arguments = parser.parse_args()
#print(arguments)
#sys.exit("test over")

if  __name__ == "__main__":
	home = os.getcwd()
	if not os.path.isfile("config.yaml"):
		print("\n\nWarning: No config file detected.  Running configuration generator...\nIf you do have a config file, terminate execution and be sure the file is named 'config.yaml' before rerunning.\n")
		conf = config_file()
		conf.preamble()
		if sys.version_info[0] == 2:
			conf.generate_config_2()
		elif sys.version_info[0] == 3:
			conf.generate_config_3()
		#generateConfig()
	configYaml = ordered_load(open("config.yaml"))
	if(arguments.command == "local"):
		if arguments.new is None:
			if arguments.execute:
				print("No new YAML detected - running the master only...")
				# load the master as yamlPar
				yamlPar = ordered_load(open(arguments.master))
			else:
				sys.exit("Nothing to do - exiting...")
				# load nothing, do nothing
		else:
		# if --new exists
			if arguments.execute:
				print("Running new and appending to master...")
				# load the new as yamlPar and append it after running; no need to load master
				yamlPar = ordered_load(open(arguments.new))
				new_append(arguments.new, arguments.master)
				os.rename("temp.yaml", arguments.master)
			else:
				print("Appending to master with no execution...")
				yamlPar = ordered_load(open(arguments.new))
				new_append(arguments.new, arguments.master)
				os.rename("temp.yaml", arguments.master)
				if(arguments.command == "local"):
					if configYaml["config-yaml"]["path-settings"]["github-directory"] != "":
						update_repository(arguments.master)
				sys.exit("Done")
	elif(arguments.command == "remote"):
		print("remote")
		if(arguments.download):
			yamlPar = process_remote_file(arguments.url, download = True)
		else:
			yamlPar = process_remote_file(arguments.url, download = False)
		print(yamlPar)

	rootDirectory = configYaml["config-yaml"]["path-settings"]["reference-directory"]
	referenceKeys = list(yamlPar.keys())
	#print(yamlPar.keys())
	# extract the keys under 'reference-entries' named 'reference-information-X'
	run = referenceHandler(errorBehavior = processLogical(configYaml["config-yaml"]["runtime-settings"]["break-on-error"]))
	#print(referenceKeys)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, yamlPar.get(referenceKeys[k]))
		# run processEntry for each subheading
	os.chdir(home)
	if(arguments.command == "local"):
		if configYaml["config-yaml"]["path-settings"]["github-directory"] != "":
			update_repository(arguments.master)


