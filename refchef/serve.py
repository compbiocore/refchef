from flask import Flask
from flask_table import Table, Col
import os
# import argparse
import oyaml as yaml
from refchef.table_utils import *
from refchef.utils import *
from refchef import config

# parser = argparse.ArgumentParser(description='Get and filter references available in the system.')
#
# parser.add_argument('--master', '-m', type=str, help='Path do to master.yaml')
# parser.add_argument('--config', '-c', type=str, help='Path do to config file in .yaml or .ini format.')
#
# arguments = parser.parse_args()
#
# if arguments.config:
#     try:
#         d = config.yaml(arguments.config)
#     except:
#         d = config.ini(arguments.config)
#     conf = config.Config(**d)
#
#     master = read_yaml(os.path.join(conf.git_local, 'master.yaml'))
#
# if arguments.master:
#     master = read_yaml(os.path.expanduser(arguments.master))


master = read_yaml("/Users/fgelin/compbiocore/refchef-test/reference-yaml/master.yaml")

app = Flask(__name__)

# Declare table
class ItemTable(Table):
    type = Col('Type')
    name = Col('Name')
    species = Col('Species')
    organization = Col('Organization')
    component = Col('Components')
    downloader = Col('Downloader')
    files = Col('Files')
    location = Col('Location')
    uuid = Col('uuid')

# Get some objects
class Item(object):
    def __init__(self, type, name, species, organization, component, downloader, files, location, uuid):
        self.type = type
        self.name = name
        self.species = species
        self.organization = organization
        self.component = component
        self.downloader = downloader
        self.files = files
        self.location = location
        self.uuid = uuid

def get_items(master):
    menu = get_full_menu(master)

    items = []
    for i, r in menu.iterrows():
        item = Item(str(r['type']),
                    str(r['name']),
                    str(r['species']),
                    str(r['organization']),
                    str(r['component']),
                    str(r['downloader']),
                    str(r['files']),
                    str(r['location']),
                    str(r['uuid']))
        items.append(item)
    return items

html_table = ItemTable(get_items(master))

@app.route("/")
def table():
    return html_table.__html__()
ato
