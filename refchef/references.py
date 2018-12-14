import os
import subprocess
import oyaml as yaml
import datetime
import glob
import uuid

from refchef import utils
from refchef.utils import cd

def execute(conf):
    """Process all steps to create directories, fetch files, and update yaml for
       references/indices/annotations"""
    yaml_file = os.path.join(conf.git_local, 'master.yaml')
    yaml_dict = utils.read_yaml(yaml_file)
    keys = list(yaml_dict.keys())

    for level in ['references', 'annotations', 'indices']:
        for k in keys:
            try:
                item = yaml_dict[k]['levels'][level]
                for i, entry in enumerate(item):
                    # Create directories
                    path_ = create_reference_directories(conf.reference_dir, k, entry['component'])

                    if entry['complete']['status'] == False:
                        component = yaml_dict[k]['levels'][level][i]['component']

                        print(u" \U0001F436 RefChef... getting {0}: {1}, component: {2}".format(utils.singular(level),
                                                                                                k,
                                                                                                component))

                        # Fetch references
                        fetch(entry['commands'], path_)
                        # create metadata file
                        create_metadata_file(yaml_dict[k]['metadata'], path_)
                        # get filenames and add to yaml
                        yaml_dict[k]['levels'][level][i]['location'] = path_
                        yaml_dict[k]['levels'][level][i]['files'] = get_filenames(path_)
                        # flip complete flag
                        yaml_dict[k]['levels'][level][i]['complete']['status'] = True
                        # add time of completion
                        now = datetime.datetime.now()
                        yaml_dict[k]['levels'][level][i]['complete']['time'] = now
                        # get md5 and add to yaml
                        yaml_dict[k]['levels'][level][i]['uuid'] = add_uuid(path_)
            except Exception:
                pass

    # Check if index has and uuid in src and creates a symlink
    index_ref_link(yaml_dict)
    # save updated master.yaml files
    utils.save_yaml(yaml_dict, yaml_file)


def create_reference_directories(reference_dir, key, component):
    """Creates all directories for the references/indices/annotations"""
    path_ = os.path.join(reference_dir, key, component)
    if not os.path.exists(path_):
        os.makedirs(path_)

    return path_

def fetch(command_list, directory):
    """ Run all commands from within the given directory"""
    for c in command_list:
        with cd(directory):
            print("Running command \"{}\"".format(c))
            subprocess.call(c, shell=True)

def get_filenames(path_):
    """Gets filenames with path of downloaded files."""
    files_path = glob.glob(os.path.join(path_, "*"))
    files = [f.split("/")[-1] for f in files_path]
    return files

def add_uuid(path_):
    """Reads final_checksums.md5 and returns id."""
    with open(os.path.join(path_, 'final_checksums.md5'), 'r') as f:
        line = f.read().splitlines()[0]
        id_ = line.split(" = ")[1]
    return str(uuid.uuid4())#str(uuid.uuid3(uuid.NAMESPACE_DNS, id_))

def create_metadata_file(metadata, path_):
    """Creates metadata.txt file."""
    component = path_.split("/")[-1]

    with open(os.path.join(path_, "metadata.txt"), "w+") as f:
        f.write("Reference Name: " + metadata["name"] + "\n")
        f.write("Component Name: " + component + "\n")
        f.write("Species: " + metadata["species"] + "\n")
        f.write("Organization: " + metadata["organization"] + "\n")
        f.write("Downloaded by: " + metadata["downloader"] + "\n")
        f.write("Downloaded on: {}".format(datetime.datetime.now()))

def get_reference_by_uuid(yaml_dict, id_):
    """ Finds reference directory by uuid """
    keys = yaml_dict.keys()
    for k in keys:
        levels = yaml_dict[k]['levels']
        if 'references' in levels.keys():
            ref = levels['references']
            for i, entry in enumerate(ref):
                if ref[i]['uuid'] == id_:
                    loc = ref[i]['location']

    return loc

def index_ref_link(yaml_dict):
    """ Checks if indices have src with id, then creates a symlink between
        index and reference files."""
    keys = list(yaml_dict.keys())
    for k in keys:
        level = yaml_dict[k]['levels']
        if 'indices' in level.keys():
            for ind in level['indices']:
                print(get_reference_by_uuid(yaml_dict, ind['src']))
                print(ind['location'])
                ref_loc = get_reference_by_uuid(yaml_dict, ind['src'])
                # print('ln -s {0} {1}'.format(ind['location'], ref_loc))
                subprocess.call('ln -s {0} {1}'.format(ind['location'], ref_loc), shell=True)


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
