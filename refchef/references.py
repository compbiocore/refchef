import os
import subprocess
import yaml
import datetime
from collections import OrderedDict, defaultdict

from refchef import utils
from refchef.config import Config

def new_append(origin, destination, conf):
    """
    The function checks to see if a given key in origin exists in destination, adds it if not.

    Open before calling this, close after it ends.

    Arguments:
    origin - the file path of the new YAML file to be appended to an existing YAML file
    destination - the file path of an existing YAML file to which a new YAML file will be appended
    """
    # Load in the YAMLs
    masterYaml = utils.ordered_load(open(os.path.join(conf.git_local, destination)))
    newYaml = utils.ordered_load(open(origin))
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
            print(masterYaml.keys())
    utils.save_yaml(masterYaml, os.path.join(conf.git_local, destination))

class referenceHandler:
    def __init__(self, conf, filetype="yaml", errorBehavior="False"):
        self.filetype = filetype
        self.errorBehavior = errorBehavior
        self.config = conf

    def retrieveReference(self, rootSubDirectory, yamlEntry, componentName):
        """Create a folder named for the reference component, then download and process the reference files in that folder.

        Additionally, generate md5 checksums for all files in their state immediately post-download.

        Then, create a 'metadata.txt' file, presently containing a timestamp for the download operation.

        Finally, create md5 checksums for all files in their final post-processed state.

        Arguments:
        rootSubDirectory - the filepath of the root directory plus the reference name
        yamlEntry - the list associated with a single reference component
        componentName - the name of the reference component
        """
        cwd = os.getcwd()
        if utils.processLogical(yamlEntry["retrieve"]) == True:
        # check to see if the given reference should be retrieved
            print("\033[1m" + "\nRetrieving " + componentName + "\n"+ "\033[0m")
            componentLocation = os.path.join(rootSubDirectory, componentName)
            # assemble the path for this component of the reference - separate folders for testing purposes
            if os.path.exists(componentLocation)==False:
                os.mkdir(componentLocation)
                # creates a directory for the component's files if said directory does not yet exist

            commands = yamlEntry["commands"]
            for j in range(0,len(commands)):
                if utils.processLogical(self.config.verbose) == True:
                    print("\033[1m" + "Now executing command: " + "\033[0m" + yamlEntry["commands"][j] + "\n")

                os.chdir(componentLocation)
                subprocess.call([yamlEntry["commands"][j]][0], shell=True)
                # loops through all subentries under the 'command-sequence' entry and runs those commands
                # actual system command as above

            f = open(os.path.join(componentLocation, "provinence.txt"), "w+")
            f.write("Component Name: " + componentName + "\n")
            f.write("Downloaded on: " + datetime.datetime.now().strftime(("%Y-%m-%d_%H:%M")) + "\n")
            f.close()
            # create provinence file with timestamp entry
        else:
            print("\n")
            print("\033[1m" + "\nSkipping " + componentName + " without retrieval\n"+ "\033[0m")

        print(cwd)

    def processEntry(self, rootDirectory, subYaml):
        """Process a given reference entry.  Each reference entry has metadata and at least one reference component.

        Arguments:
        rootDirectory - the root directory for all references specified in the YAML, as specified in the 'configuration' subentry
        subYaml - the piece of the YAML called 'reference-information-X' where X is some number corresponding to a single reference and all its components
        """
        # creates a list of reference components (the keys for the level below 'reference-information-X')
        allReferences = subYaml["levels"]["references"]
        if "annotations" in subYaml["levels"]:
            all_annotations = subYaml["levels"]["annotations"]
        if "indices" in subYaml["levels"]:
            all_indices = subYaml["levels"]["indices"]

        referenceParentLocation = os.path.join(rootDirectory, subYaml["metadata"]["name"])
        # assemble the path of this reference into which components will be put
        if os.path.exists(referenceParentLocation) == False:
                os.makedirs(referenceParentLocation)
                # create the directory if it doesn't exist yet

        metadata = subYaml["metadata"]
        f = open(os.path.join(referenceParentLocation, "metadata.txt"), "w+")
        f.write("Reference Name: " + metadata["name"] + "\n")
        f.write("Species: " + metadata["species"] + "\n")
        f.write("Organization: " + metadata["organization"] + "\n")
        f.write("Downloaded by: " + metadata["downloader"] + "\n")
        f.close()

        # create the metadata file, contents to be expanded upon

        for i in allReferences:
            self.retrieveReference(referenceParentLocation, i, i["component"])
        if "annotations" in subYaml["levels"]:
            if len(all_annotations) > 0:
                for j in all_annotations:
                    self.retrieveReference(referenceParentLocation, j, j["component"])
        if "indices" in subYaml["levels"]:
            if len(all_indices) > 0:
                for k in all_indices:
                    self.retrieveReference(referenceParentLocation, k, k["component"])
        # retrieve each component of the reference e.g. 'primary reference', 'est', 'gtf', etc
        # these can be named anything and there can be any number of them
