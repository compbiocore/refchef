import pytest
import os
import subprocess
import oyaml as yaml
import uuid
from collections import OrderedDict, defaultdict
import yamlloader
import shutil
from refchef.references import *
from refchef.utils import *
from refchef import config

@pytest.fixture
def conf():
    d = config.yaml("tests/data/cfg.yaml")
    conf = config.Config(**d)
    return conf

@pytest.fixture
def dir():
    path_ = "tests/data/test_a/test_a"
    return path_

@pytest.fixture
def master():
    if sys.platform == 'darwin':
        file_name = 'master_osx.yaml'
    else:
        file_name = 'master_linux.yaml'
    return file_name

def test_create_reference_directories(conf, dir):
    create_reference_directories(conf.reference_dir, 'test_a', 'test_a')
    assert os.path.exists(dir)

def test_fetch(dir):
    commands = ['touch test.txt', 'echo test > test.txt', 'md5 test.txt > final_checksums.md5']
    fetch(commands, dir)

    with open(os.path.join(dir, 'test.txt'), 'r') as f:
        line = f.readline()
    assert line == 'test\n'

def test_get_filenames(conf, dir):
    files = get_filenames(dir)
    assert len(files) == 2
    assert 'test.txt' in files
    assert 'final_checksums.md5' in files

def test_add_uuid(dir):
    assert 'final_checksums.md5' in get_filenames(dir)
    with open(os.path.join(dir, 'final_checksums.md5'), 'r') as f:
        l = f.readlines()
        assert l == 'test'
    uuid_test = add_uuid(dir)

    assert type(uuid_test) == str
    assert str(uuid_test) == 'a1949ec6-b1c8-33fe-9326-46ef7d597027'

def test_is_uuid():
    assert is_uuid('a1949ec6-b1c8-33fe-9326-46ef7d597027') == True
    assert is_uuid('not_an_uuid') == False

def test_execute(conf, master):

    execute(conf, master)

    path_1 = os.path.join(conf.reference_dir, 'reference_test1', 'primary')

    files = get_filenames(path_1)
    assert len(files) == 4
    fnames = ['chr1.fa', 'metadata.txt','postdownload_checksums.md5','final_checksums.md5']
    for f in fnames:
        assert f in files

    path_ = os.path.join(conf.git_local, master)
    yaml_dict = utils.read_yaml(path_)

    assert yaml_dict['reference_test1']['levels']['references'][0]['complete']['status'] == True
    id_ = uuid.UUID(yaml_dict['reference_test1']['levels']['references'][0]['uuid'])
    assert type(id_) == uuid.UUID
    assert yaml_dict['reference_test1']['levels']['references'][0]['location'] == path_1
    assert yaml_dict['reference_test1']['levels']['references'][0]['files'] == files

def test_create_metadata(conf, master, dir):
    path_ = os.path.join(conf.git_local, master)
    yaml_dict = utils.read_yaml(path_)

    create_metadata_file(yaml_dict['reference_test1']['metadata'], dir)

    with open(os.path.join(dir, 'metadata.txt'), 'r') as f:
        lines = f.readlines()

    assert os.path.exists(os.path.join(dir, 'metadata.txt'))
    assert len(lines) == 6

def test_get_reference_by_uuid(conf, master):
    path_ = os.path.join(conf.git_local, master)
    yaml_dict = utils.read_yaml(path_)
    path_1 = os.path.join(conf.reference_dir, 'reference_test1', 'primary')

    loc = get_reference_by_uuid(yaml_dict, '8040b09f-3844-3c42-b765-1f6a32614895')

    assert loc == path_1

def test_index_ref_link(conf, master):
    if sys.platform == 'darwin':
        file_name = 'new_osx.yaml'
    else:
        file_name = 'new_linux.yaml'
    ori = os.path.join(conf.git_local, file_name)
    des = os.path.join(conf.git_local, master)
    append_yaml(ori, des)

    execute(conf, master)
    path_1 = os.path.join(conf.reference_dir, 'reference_test1', 'primary', 'bwa_index')

    assert os.path.islink(path_1)
