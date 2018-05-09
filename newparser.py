#!/usr/bin/env python


# Create a function just for a single reference, have that be the 'single' behavior, and then loop over it for the 'multi'
# maybe have two separate argparse flags that determine behavior from the outset


import argparse
import os
import subprocess
import yaml
import time
import sys
import datetime
import collections


######################################



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
					if yamlPar["reference-yaml"]["configuration"]["verbose"] == True:
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



if  __name__ == "__main__":
	yamlPar = yaml.load(open("/users/aleith/reference_yaml/prototype.yaml"))
	rootDirectory = yamlPar["reference-yaml"]["configuration"]["root-directory"]
	referenceKeys = sorted(yamlPar["reference-yaml"]["reference-entries"].keys(), key=lambda entry: int(entry.split('-')[2]))
	# extract the keys under 'reference-entries' named 'reference-information-X'
	run = referenceHandler(errorBehavior=yamlPar["reference-yaml"]["configuration"]["break-on-error"])
	for k in range(0, len(referenceKeys)):
		run.processEntry(rootDirectory, yamlPar["reference-yaml"]["reference-entries"].get(referenceKeys[k]))
		# run processEntry for each 'reference-information-X'




