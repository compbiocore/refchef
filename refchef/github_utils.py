import os
import oyaml as yaml
import shutil
import yamlloader
# import urllib2
import github

from refchef import config
from refchef.utils import *

def setup_git(conf):
	git_dir = os.path.join(conf.git_local, '.git')
	work_tree = os.path.join(conf.git_local, '')

	return git_dir, work_tree


def pull(git_dir, work_tree):
	"""
	Pull changes to master.yaml

	Arguments:
	git_dir: local path to .git file in directory
	work_tree: path to directory
	"""
	subprocess.call(['git --git-dir={0} --work-tree={1} pull'.format(git_dir, work_tree)], shell=True)

def commit(git_dir, work_tree):
	"""
	Commits changes to master.yaml

	Arguments:
	git_dir: local path to .git file in directory
	work_tree: path to directory
	"""
	subprocess.call(['git --git-dir={0} --work-tree={1} add --all'.format(git_dir, work_tree)], shell=True)
	subprocess.call(["git --git-dir={0} --work-tree={1} commit -m 'refchef autocommit'".format(git_dir, work_tree)], shell=True)


def push(git_dir, work_tree):
	"""
	Pushes changes remote repository.

	Arguments:
	git_dir: local path to .git file in directory
	work_tree: path to directory
	"""
	subprocess.call(["git --git-dir={0} --work-tree={1} push".format(git_dir, work_tree)], shell=True)


def read_menu_from_github(conf, save=False):
	"""Read master.yaml from GitHub"""
	token = os.getenv("GITHUB_TOKEN")
	g = github.Github(token)
	repo = g.get_repo(conf.git_remote)
	try:
		master = repo.get_contents("master.yaml")
	except github.GithubException:
		master = repo.get_contents("master.yaml")

	master_dict = yaml.load(master.decoded_content)

	if save:
		save_yaml(master_dict, config.reference_dir)
	else:
		return master_dict
