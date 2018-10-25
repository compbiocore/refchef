#!/usr/bin/env python


# Create a function just for a single reference, have that be the 'single' behavior, and then loop over it for the 'multi'
# maybe have two separate argparse flags that determine behavior from the outset
# Create one function, multiindex() or something, to generate indices for all tools provided in a separate subheading of the master yaml
# 	can a yaml have multiple values for one key??? - https://learnxinyminutes.com/docs/yaml/ ctrl+f 'json'



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



######################################

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
	"""
	text = str(text)
	if(text == "true" or text == "True" or text == "TRUE" or text == "T" or text == "t" or text == "1"):
		return True
	elif(text == "false" or text == "False" or text == "FALSE" or text == "F" or text == "f" or text == "0"):
		return False
	else:
		print("Input has no logical analogue.")
		return(text)

def generateConfig():
	"""Generate a human-readable configuration YAML for running the software proper.

	This version of generateConfig() uses an ordered dictionary to generate its YAML."""
	print("This interactive prompt will allow you to generate a config file for this tool.")
	print("If asked to provide a filepath, please provide the full, absolute filepath, with no ~.")
	print("Furthermore, please do not append a trailing '/' to the filepaths.")
	print("If you leave your response to a prompt empty, that entry will not be generated.")
	print("\033[1m" + "This operation will overwrite any existing config.yaml.  Type 'yes' to proceed, or anything else to exit." + "\033[0m")
	continue_prompt = raw_input("> ")
	if continue_prompt != "yes":
		sys.exit("Exiting without action.")
	print("\033[1m" + "Filepaths" + "\033[0m")
	print("What is the filepath of the directory to be used as root for the references? (Required)")
	root_dir = raw_input("> ")
	if "~" in root_dir:
		sys.exit("Please try again without using ~.")
	if root_dir != "":
		print("do nothing")
	else:
		sys.exit("Required option omitted; exiting.")
	print("What is the " + "\033[1m" + "local" + "\033[0m" + " Github repository directory (parent directory of cloned repos)?")
	local_git_dir = raw_input("> ")
	if "~" in local_git_dir:
		sys.exit("Please try again without using ~.")
	if local_git_dir != "":
		print("do nothing")
		#f.write("        github-directory        : " + str(local_git_dir) + "\n")
	print("What is the " + "\033[1m" + "remote" + "\033[0m" + " Github repo in the format 'USER/REPO'?")
	remote_git_name = raw_input("> ")
	if remote_git_name != "":
		print("do nothing")
		#f.write("        remote-repository       : " + str(remote_git_name) + "\n")
	print("\033[1m" + "Logging" + "\033[0m")
	#f.write("    log-settings:\n")
	print("Should logs be generated?  Type 'True' or 'False'. (Default: True)")
	log_setting = raw_input("> ")
	if log_setting == "":
		log_setting = "True"
	#f.write("        log                        : " + str(log_setting) + "\n")
	print("\033[1m" + "Runtime Settings" + "\033[0m")
	#f.write("    runtime-settings:\n")
	print("Should the tool end its run on any error?  Type 'True' or 'False'. (Default: True)")
	break_on_error = raw_input("> ")
	if break_on_error == "":
		break_on_error = "True"
	#f.write("        break-on-error             : " + str(break_on_error) + "\n")
	print("Should the tool be verbose (generate lots of stepwise output)? (Default: False)")
	verbose = raw_input("> ")
	if verbose == "":
		verbose = "False"
	#f.write("        verbose                    : " + str(verbose) + "\n")
	#f.close()
	configObject = OrderedDict([('config-yaml', OrderedDict([('path-settings', OrderedDict([('reference-directory', str(root_dir)), ('github-directory', str(local_git_dir)), ('remote-repository', str(remote_git_name))])), ('log-settings', OrderedDict([('log', str(log_setting))])), ('runtime-settings', OrderedDict([('break-on-error', str(break_on_error)), ('verbose', str(verbose))]))]))])
	#pathSettings = OrderedDict([("reference-directory", "test"), ("github-directory", "test2"), ("remote-repository", "test3")])
	#logSettings = OrderedDict([("log", "True")])
	#runtimeSettings = OrderedDict([("break-on-error", "True"), ("verbose", "False")])
	#yaml.dump(configObject, open('config.yaml', 'w'), Dumper=yamlordereddictloader.Dumper, indent=4, default_flow_style=False)
	yaml.dump(configObject, open('config.yaml', 'w'), Dumper=yamlloader.ordereddict.CDumper, indent=4, default_flow_style=False)
	current_time = datetime.datetime.now().strftime(("%Y-%m-%d_%H:%M"))
	backup_path = "config_backup_" + current_time + ".yaml"
	shutil.copyfile("config.yaml",backup_path)
	print("Generated config file and timestamped backup.")
	print("To use this backup in the future, simply copy it to a file named 'config.yaml'.")


def update_repository(master):
	"""
	Update a github repository
	"""
	configYaml = ordered_load(open("config.yaml"))
	gitPath = configYaml["config-yaml"]["path-settings"]["github-directory"] + "/" + configYaml["config-yaml"]["path-settings"]["remote-repository"].split("/")[1]
	startingDir = os.getcwd()
	os.chdir(gitPath)
	subprocess.call(["git pull"], shell=True)
	os.chdir(startingDir)
	shutil.copyfile(master, gitPath + "/" + master)
	#shutil.copyfile("yamlOne.yaml", "/users/aleith/github_pages/yaml-repository/yamlOne.yaml")
	os.chdir(gitPath)
	subprocess.call(['git add --all && git commit -m  "refchef autopush" && git push origin master'], shell=True)
	os.chdir(startingDir)


def new_append(origin, destination):
	"""
	origin and destination are the new filename and the master filename respectively.

	The function checks to see if a given key in origin exists in destination, adds it if not.

	Open before calling this, close after it ends.
	"""
	# Load in the YAMLs
	masterYaml = ordered_load(open(destination))
	newYaml = ordered_load(open(origin))
	# Loop over each key in the origin and add it to the destination
	for i in newYaml.keys():
		if i in masterYaml.keys():
			for j in newYaml.get(i).keys():
				for s in newYaml.get(i).get(j).keys():
					print(s)
					# add entries that do not previously exist
					### IF THE KEY EXISTS AND THE VALUE IS DIFFERENT, DO NOT OVERWRITE - RECORD WOULD BE COMPROMISED
					### How to handle cases where a new command is added between two old commands?
					### Add new non-default argument to force an overwrite?
					if s in masterYaml.get(i).get(j).keys():
						masterYaml[i][j][str(s)] = newYaml[i][j][s]
		else:
			masterYaml[str(i)] = newYaml.get(i)
	#f = open("master_test_new.yaml", 'w')
	#ordered_dump(masterYaml)
	#yaml.dump(masterYaml, open('temp.yaml', 'w'), Dumper=yamlordereddictloader.Dumper, indent=4, default_flow_style=False)
	yaml.dump(masterYaml, open('temp.yaml', 'w'), Dumper=yamlloader.ordereddict.CDumper, indent=4, default_flow_style=False)

	#f.close()
	#return(destination)

	
def process_remote_file(url, download):
	"""
	Process a Master YAML stored on a github repository
	"""
	url = str(url)
	file = urllib2.urlopen(url)
	data = ordered_load(file)
	if(download):
		filename = url.split("/")[len(url.split("/")) - 1]
		file = urllib2.urlopen(url)
		# must be reassigned, for some reason
		with open(filename, 'w') as output:
  			output.write(file.read())
	return(data)





class referenceHandler:
	def __init__(self, filetype="yaml", errorBehavior="False"):
		self.filetype = filetype
		self.errorBehavior = errorBehavior

	def retrieveReference(self, rootSubDirectory, yamlEntry, componentName):
		"""Create a folder named for the reference component, then download and process the reference files in that folder.

		Additionally, generate md5 checksums for all files in their state immediately post-download.

		Then, create a 'metadata.txt' file, presently containing a timestamp for the download operation.

		do other things to be determined

		Finally, create md5 checksums for all files in their final post-processed state.
		"""

		#yamlEntry.keys()[0] is the top-level key i.e. the name of the reference subunit e.g. 'est' or 'primary-reference'
		#print(yamlEntry)
		#print(yamlEntry.keys())
		print("\n\n\n\n\n\n\n")
		print("made it this far")
		if processLogical(yamlEntry["retrieve"]) == True:
		# check to see if the given reference should be retrieved
			print("\033[1m" + "\nRetrieving " + componentName + "\n"+ "\033[0m")

			componentLocation = rootSubDirectory + "/" + componentName
			# assemble the path for this component of the reference - separate folders for testing purposes
			if os.path.exists(componentLocation)==False:
				#subprocess.call(["mkdir " + componentLocation], shell=True)
				os.mkdir(componentLocation)
				# creates a directory for the component's files if said directory does not yet exist

			os.chdir(componentLocation)
			# moves to the given reference's directory

			commands = yamlEntry["commands"]

			for j in range(0,len(commands)):
					if processLogical(configYaml["config-yaml"]["runtime-settings"]["verbose"]) == True:
						print("\033[1m" + "Now executing command: " + "\033[0m" + yamlEntry["commands"][j] + "\n")
		    			subprocess.call([yamlEntry["commands"][j]], shell=True)
		    			# this line is an actual system command so needs to stay as a subprocess call
		    	else:
		    	# this asymmetric indent is the only way to avoid a strange bug - any other indent pattern is deemed too little or too much
		    		subprocess.call([yamlEntry["commands"][j]], shell=True)
		    		# loops through all subentries under the 'command-sequence' entry and runs those commands
		    		# actual system command as above



			f = open("provinence.txt", "w+")
			f.write("Component Name: " + componentName + "\n")
			f.write("Downloaded on: " + datetime.datetime.now().strftime(("%Y-%m-%d_%H:%M")) + "\n")
			f.close()
			# create provinence file with timestamp entry
		else:
			print "\n"
			print("\033[1m" + "\nSkipping " + componentName + " without retrieval\n"+ "\033[0m")


	def processEntry(self, rootDirectory, subYaml):
		"""Process a given reference entry.  Each reference entry has metadata and at least one reference component.

		rootDirectory is the root directory for all references specified in the YAML, as specified in the 'configuration' subentry

		subYaml is the piece of the YAML called 'reference-information-X' where X is some number corresponding to a single reference and all its components

		"""
		#allReferences = subYaml.keys()
		# subYaml NO LONGER HAS KEYS, THIS STATEMENT MAY BE UNCESSESARY NOW


		#allReferences.remove("metadata")
		# creates a list of reference components (the keys for the level below 'reference-information-X')
		allReferences = subYaml["levels"]["references"]


		referenceParentLocation = rootDirectory + "/" + subYaml["metadata"]["name"]
		# assemble the path of this reference into which components will be put
		if os.path.exists(referenceParentLocation)==False:
				#subprocess.call(["mkdir " + referenceParentLocation], shell=True)
				os.makedirs(referenceParentLocation)
				# create the directory if it doesn't exist yet

		metadata = subYaml["metadata"]
		f = open(referenceParentLocation + "/metadata.txt", "w+")
		f.write("Reference Name: " + metadata["name"] + "\n")
		f.write("Species: " + metadata["species"] + "\n")
		f.write("Organization: " + metadata["organization"] + "\n")
		f.write("Downloaded by: " + metadata["downloader"] + "\n")
		f.close()
		# create the metadata file, contents to be expanded upon

		for i in allReferences:
			#run.retrieveReference(referenceParentLocation, subYaml[i], i)
			run.retrieveReference(referenceParentLocation, i, i["component"])
			# retrieve each component of the reference e.g. 'primary reference', 'est', 'gtf', etc
			# these can be named anything and there can be any number of them


# Create argument parser
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
		generateConfig()
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
	referenceKeys = yamlPar.keys()
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


