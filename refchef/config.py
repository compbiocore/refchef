import os
import subprocess
from collections import OrderedDict, defaultdict
import configparser
from refchef import utils
try:
    input = raw_input
except NameError:
    pass


class Config:
	def __init__(self, reference_dir, git_local, git_remote, log, break_on_error, verbose):
		self.reference_dir = os.path.expanduser(reference_dir)
		self.git_local = os.path.expanduser(git_local)
		self.git_remote = git_remote
		self.log = log
		self.break_on_error = break_on_error
		self.verbose = verbose

def yaml(path):
	dict_ = utils.read_yaml(path)

	d = {}
	d['reference_dir'] = dict_['config-yaml']['path-settings']['reference-directory']
	d['git_local'] = dict_['config-yaml']['path-settings']['git-directory']
	d['git_remote'] = dict_['config-yaml']['path-settings']['remote-repository']
	d['log'] = dict_['config-yaml']['log-settings']['log']
	d['break_on_error'] = dict_['config-yaml']['runtime-settings']['break-on-error']
	d['verbose'] = dict_['config-yaml']['runtime-settings']['verbose']

	return d


def ini(path):
	config = configparser.ConfigParser()
	config.read(path)

	d = {}
	d['reference_dir'] = config.get('path-settings', 'reference-directory')
	d['git_local'] = config.get('path-settings', 'git-directory')
	d['git_remote'] = config.get('path-settings', 'remote-repository')
	d['log'] = config.get('log-settings', 'log')
	d['break_on_error'] = config.get('runtime-settings', 'break-on-error')
	d['verbose'] = config.get('runtime-settings', 'verbose')

	return d
