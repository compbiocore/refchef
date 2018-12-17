import os
import subprocess
import oyaml as yaml
import datetime
import glob
import uuid

from refchef import utils
from refchef.utils import cd

def execute(conf, file_name):
    """Process all steps to create directories, fetch files, and update yaml for
       references/indices/annotations"""
    yaml_file = os.path.join(conf.git_local, file_name)
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
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, id_))

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

def is_uuid(str_):
    try:
        uuid.UUID(str_)
        return True
    except:
        return False

def index_ref_link(yaml_dict):
    """ Checks if indices have src with id, then creates a symlink between
        index and reference files."""
    keys = list(yaml_dict.keys())
    for k in keys:
        level = yaml_dict[k]['levels']
        if 'indices' in level.keys():
            for ind in level['indices']:
                if is_uuid(ind['src']):
                    ref_loc = get_reference_by_uuid(yaml_dict, ind['src'])
                    subprocess.call('ln -s {0} {1}'.format(ind['location'], ref_loc), shell=True)
