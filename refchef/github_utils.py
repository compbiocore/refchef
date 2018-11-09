import os
import yaml
import shutil
import yamlloader
# import urllib2
import github

from refchef import config
from refchef.utils import *


def update_repository(conf):
	"""
	Update a github repository.

	Arguments:
	master - the master YAML to be pushed to github
	"""
	# configYaml = ordered_load(open("config.yaml"))
	gitPath = conf.git_local #configYaml["config-yaml"]["path-settings"]["github-directory"] + "/" + configYaml["config-yaml"]["path-settings"]["remote-repository"].split("/")[1]
	startingDir = os.getcwd()
	os.chdir(gitPath)
	subprocess.call(["git pull"], shell=True)
	# os.chdir(startingDir)
	# shutil.copyfile(master, gitPath + "/" + master)
	# os.chdir(gitPath)
	subprocess.call(['git add --all && git commit -m  "refchef autopush" && git push origin master'], shell=True)
	os.chdir(startingDir)

def process_remote_file(url, download):
	"""
	Process a Master YAML stored on a github repository

	Arguments:
	url - the URL of a remote YAML file located on github
	download - a logical denoting whether or not the remote YAML file should be downloaded
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
