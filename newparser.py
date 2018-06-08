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
import shutil


######################################

def generateConfig():
	"""Generate a human-readable configuration YAML for running the software proper.

	Code readability has been traded for output readability via escape character-based document formatting."""
	print("This interactive prompt will allow you to generate a config file for this tool.")
	print("If asked to provide a filepath, please provide the full, absolute filepath.")
	print("Furthermore, please do not append a trailing '/' to the filepaths.")
	print("If you leave your response to a prompt empty, that entry will not be generated.")
	print("\033[1m" + "This operation will overwrite any existing config.yaml.  Type 'yes' to proceed, or anything else to exit." + "\033[0m")
	continue_prompt = raw_input("> ")
	if continue_prompt != "yes":
		sys.exit("Exiting without action.")
	f = open("config.yaml", 'w')
	f.write("config-yaml:\n")
	print("\033[1m" + "Filepaths" + "\033[0m")
	f.write("    path-settings:\n")
	print("What is the filepath of the directory to be used as root for the references? (Required)")
	root_dir = raw_input("> ")
	if root_dir != "":
		f.write("        reference-directory     : " + str(root_dir) + "\n")
	else:
		os.remove("config.yaml")
		sys.exit("Required option omitted; exiting.")
	print("What is the " + "\033[1m" + "local" + "\033[0m" + " Github repository directory (parent directory of cloned repos)?")
	local_git_dir = raw_input("> ")
	if local_git_dir != "":
		f.write("        github-directory        : " + str(local_git_dir) + "\n")
	print("What is the " + "\033[1m" + "remote" + "\033[0m" + " Github repo in the format 'USER/REPO'?")
	remote_git_name = raw_input("> ")
	if remote_git_name != "":
		f.write("        remote-repository       : " + str(remote_git_name) + "\n")
	print("\033[1m" + "Logging" + "\033[0m")
	f.write("    log-settings:\n")
	print("Should logs be generated?  Type 'True' or 'False'. (Default: True)")
	log_setting = raw_input("> ")
	if log_setting == "":
		log_setting = "True"
	f.write("        log                        : " + str(log_setting) + "\n")
	print("\033[1m" + "Runtime Settings" + "\033[0m")
	f.write("    runtime-settings:\n")
	print("Should the tool end its run on any error?  Type 'True' or 'False'. (Default: True)")
	break_on_error = raw_input("> ")
	if break_on_error == "":
		break_on_error = "True"
	f.write("        break-on-error             : " + str(break_on_error) + "\n")
	print("Should the tool be verbose (generate lots of stepwise output)? (Default: False)")
	verbose = raw_input("> ")
	if verbose == "":
		verbose = "False"
	f.write("        verbose                    : " + str(verbose) + "\n")
	f.close()
	current_time = datetime.datetime.now().strftime(("%Y-%m-%d_%H:%M"))
	backup_path = "config_backup_" + current_time + ".yaml"
	shutil.copyfile("config.yaml",backup_path)
	print("Generated config file and timestamped backup.")
	print("To use this backup in the future, simply copy it to a file named 'config.yaml'.")


def append(origin, destination):
	"""Append the 'new' YAML to the 'master' YAML"""

	print("Now appending " + origin + " to " + destination + "...")

	# First, clean up the file's blank lines
	subprocessCommand = 'awk \'NF\' ' + origin + ' > temp.yaml && mv temp.yaml ' + origin
	subprocess.call([subprocessCommand], shell=True)

	subprocessCommand = 'sed -i -e \'$a\\\' ' + origin
	# add a newline to the end of New if there isn't one there already
	subprocess.call([subprocessCommand], shell=True)

	subprocessCommand = 'grep -n "reference-entries" ' + origin + ' | grep -Eo \'^[^:]+\''
	referenceLine = int(subprocess.check_output([subprocessCommand],shell=True))
	subprocessCommand = 'wc -l < ' + origin
	totalLines = int(subprocess.check_output([subprocessCommand],shell=True))
	#subprocessCommand = 'grep -c "^$" ' + origin
	#blankLines = int(subprocess.check_output([subprocessCommand], shell=True))
	## Check if there is a blank line at the end of the file or not - there will be iff there were 1+ blank lines at the end before parsing



	#tailLines = (totalLines + blankLines) - referenceLine
	tailLines = (totalLines) - referenceLine
	subprocessCommand = 'tail -n' + str(tailLines) + ' ' + origin + '> temp.yaml'
	subprocess.call([subprocessCommand], shell=True)
	# create the temp yaml file consisting of only the reference entries and not the config settings

	masterYaml = yaml.load(open(destination))
	tempYaml = yaml.load(open("temp.yaml"))
	masterNames = sorted(masterYaml["reference-yaml"]["reference-entries"].keys(), key=lambda entry: int(entry.split('-')[2]))
	# ^superfluous except for below line, but retained for symmetry
	masterLength = len(masterNames)
	newNames = sorted(tempYaml.keys(), key=lambda entry: int(entry.split('-')[2]))
	newLength = len(newNames)

	#### The first number in temp must be the last number in master + 1

	for k in newNames:
		index = int(k.split("-")[2]) + masterLength
		temp = "reference-information-" + str(index)
		subprocessCommand = "sed -i -e \'s/" + k + "/" + temp + "/g\' temp.yaml"
		subprocess.call([subprocessCommand], shell=True)
		

	# sed -i -e 's/reference-information-3/reference-information-1/g' tester.yaml

	subprocessCommand = 'sed -i -e \'$a\\\' ' + destination
	# add a newline to the end of master if there isn't one there already
	subprocess.call([subprocessCommand], shell=True)
	subprocessCommand = "cat temp.yaml >> " + destination
	# append temp to master
	subprocess.call([subprocessCommand], shell=True)
	subprocess.call(['rm temp.yaml'], shell=True)
	if sys.platform == "darwin":
		subprocess.call(['rm *-e'], shell=True)
		# remove anomalous intermediary files created by bad sed and subprocess integration on OSX only
	#sys.exit("Done")

class referenceHandler:
	def __init__(self, filetype="yaml", errorBehavior="False"):
		self.filetype = filetype
		self.errorBehavior = errorBehavior

	def mirrorGithub(self, gitDir, repository):
		"""Retrieve and parse a master YAML stored somewhere on Github"""
		# use an existing config file to run this 

		startingDir = os.getcwd()
		# retain current working directory to change back to at the end
		os.chdir(gitDir)
		# switch to main git directory
		githubUrl = "https://github.com/" + repository + ".git"
		subprocess.call(['git clone ' + githubUrl], shell=True)
		# clone the repo with the YAML

		# temporarily hardcode the reference directory in lieu of a configuration file for testing purposes
		referenceDirectory = "/Users/aleith/reference_yaml/github_references"






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
		if yamlEntry["retrieve"] == True:
		# check to see if the given reference should be retrieved
			print("\033[1m" + "\nRetrieving " + componentName + "\n"+ "\033[0m")

			componentLocation = rootSubDirectory + "/" + componentName
			# assemble the path for this component of the reference - separate folders for testing purposes
			if os.path.exists(componentLocation)==False:
				subprocess.call(["mkdir " + componentLocation], shell=True)
				# creates a directory for the component's files if said directory does not yet exist

			os.chdir(componentLocation)
			# moves to the given reference's directory

			commandKeys = sorted(yamlEntry["command-sequence"].keys(), key=lambda entry: int(entry.split('-')[1]))
			# create a sorted list of command keys since YAML files are read in unsorted

			if (commandKeys == ["command-" + str(k) for k in range(1, len(commandKeys)+1)]) == False:
			# check to be sure the commands are enumerated by a numerical sequence i.e. don't have typos
				#sys.exit("\033[1m" + "Fatal Error: Command Entries misnumbered for component " + "\033[0m" + componentName)
				subprocess.call(["echo 'Error: misnumbered commands' > error.txt"], shell=True)
				if self.errorBehavior == True:
					sys.exit("\033[1m" + "Fatal Error: Command Entries misnumbered for component: " + "\033[0m" + componentName)
				else:
					print("\033[1m" + "Error: Command Entries misnumbered for component: " + "\033[0m" + componentName + "; skipping...")
					return



			for j in range(0,len(commandKeys)):
					if configYaml["config-yaml"]["runtime-settings"]["verbose"] == True:
						print("\033[1m" + "Now executing command: " + "\033[0m" + yamlEntry["command-sequence"].get(commandKeys[j]) + "\n")
		    			subprocess.call([yamlEntry["command-sequence"].get(commandKeys[j])], shell=True)
		    	else:
		    	# this asymmetric indent is the only way to avoid a strange bug - any other indent pattern is deemed too little or too much
		    		subprocess.call([yamlEntry["command-sequence"].get(commandKeys[j])], shell=True)
		    		# loops through all subentries under the 'command-sequence' entry and runs those commands




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
		allReferences = subYaml.keys()
		allReferences.remove("metadata")
		# creates a list of reference components (the keys for the level below 'reference-information-X')



		referenceParentLocation = rootDirectory + "/" + subYaml["metadata"]["reference-name"]
		# assemble the path of this reference into which components will be put
		if os.path.exists(referenceParentLocation)==False:
				subprocess.call(["mkdir " + referenceParentLocation], shell=True)
				# create the directory if it doesn't exist yet

		metadata = subYaml["metadata"]
		f = open(referenceParentLocation + "/metadata.txt", "w+")
		f.write("Reference Name: " + metadata["reference-name"] + "\n")
		f.write("Species: " + metadata["species"] + "\n")
		f.write("Organization: " + metadata["organization"] + "\n")
		f.write("Downloaded by: " + metadata["downloader"] + "\n")
		f.close()
		# create the metadata file, contents to be expanded upon


		for i in allReferences:
			run.retrieveReference(referenceParentLocation, subYaml[i], i)
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

###pretend this doesn't exist for now
remote_parser = subs.add_parser('remote')
remote_parser.add_argument('--repo', type=str, required = True, help = 'Denotes the remote Github repo')




# Parse arguments
arguments = parser.parse_args()
print(arguments)
#sys.exit("test over")

if  __name__ == "__main__":
	if not os.path.isfile("config.yaml"):
		print("\n\nWarning: No config file detected.  Running configuration generator...\nIf you do have a config file, terminate execution and be sure the file is named 'config.yaml' before rerunning.\n")
		generateConfig()
	configYaml = yaml.load(open("config.yaml"))
	if arguments.new is None:
		if arguments.execute:
			print("No new YAML detected - running the master only...")
			# load the master as yamlPar
			yamlPar = yaml.load(open(arguments.master))
		else:
			sys.exit("Nothing to do - exiting...")
			# load nothing, do nothing
	else:
	# if --new exists
		if arguments.execute:
			print("Running new and appending to master...")
			# load the new as yamlPar and append it after running; no need to load master
			yamlPar = yaml.load(open(arguments.new))
			append(arguments.new, arguments.master)
		else:
			print("Appending to master with no execution...")
			yamlPar = yaml.load(open(arguments.new))
			append(arguments.new, arguments.master)
			sys.exit("Done")

	rootDirectory = configYaml["config-yaml"]["path-settings"]["reference-directory"]
	referenceKeys = sorted(yamlPar["reference-yaml"]["reference-entries"].keys(), key=lambda entry: int(entry.split('-')[2]))
	# extract the keys under 'reference-entries' named 'reference-information-X'
	run = referenceHandler(errorBehavior=configYaml["config-yaml"]["runtime-settings"]["break-on-error"])
	print(referenceKeys)
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, yamlPar["reference-yaml"]["reference-entries"].get(referenceKeys[k]))
		# run processEntry for each 'reference-information-X'



# Begin parsing of YAML
#yamlPar = yaml.load(open(arguments.yaml))


#if  __name__ == "__main__":
	#yamlPar = yaml.load(open("/users/aleith/reference_yaml/prototype.yaml"))







