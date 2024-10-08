import os
import json
import pandas as pd
#from pandas.io.json import json_normalize
import terminaltables
import oyaml as yaml
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

from refchef import config
from refchef.github_utils import read_menu_from_github
from refchef.utils import *
#from pandas.io.json import json_normalize

def get_full_menu(master):
    """Reads yaml file and converts to a table format"""

    #json normalize data (to expand dict to table)
    df = pd.json_normalize(master).T.reset_index()
    df.columns = ["a", "b"]

    #rearange data
    res = df.set_index(["a"])["b"].apply(pd.Series).stack()
    res = res.reset_index()
    res.columns = ["a", "b", "c"]
    res["d"] = res["a"].apply(lambda x: x.split(".")[-1])
    res["e"] = res["a"].apply(lambda x: x.split(".")[1])
    res["f"] = res["a"].apply(lambda x: x.split(".")[0])
    res.drop(columns=["a"])

    #expand dict again for lower levels
    table = pd.json_normalize(res.to_dict(orient="records"))

    #create matadata table
    metadata = table[table["e"] == "metadata"][["c", "d", "f"]].pivot(index="f", columns="d")
    metadata.columns = metadata.columns.droplevel(0)
    metadata = metadata.reset_index().rename_axis(index = None)

    #create levels table
    levels = table[table["e"] == "levels"][["c.component", "c.files", "c.location", "c.uuid", "f", "d"]]

    levels.rename(columns={"f":"name"}, inplace=True)
    m = metadata
    #create full table (menu)
    menu = m.merge(levels).drop(columns=["f"])


    cols = ['category', 'common_name', 'custom', 'description', 'downloader',
       'ensembl_release_number', 'genbank', 'name', 'ncbi_taxon_id',
       'organism', 'organization', 'refseq', 'component', 'files',
       'location', 'uuid', 'type']

    if ('genbank' not in menu.columns):
        cols.remove('genbank')

    if ('refseq' not in menu.columns):
        cols.remove('refseq')

    menu.columns = cols

    return menu

def filter_menu(menu, key, value):
    """Filters table based on key-value pair passed."""

    filtered = menu[menu[key] == value]
    return filtered

def split_filter(string):
    """Simple function to split on semicolon and return tuple."""
    return string.split(":")

def multiple_filter(menu, string):
    """Filter table by passing multiple filter options
    Arguments
    menu: pandas DataFrame
    string: comma-separated string representing filter options as:
        "field:value,field2:value2,fieldn:valuen"
    """
    if "," in string:
        l = string.split(",")
        filtered = menu.copy()
        for pair in l:
            field, value = split_filter(pair)
            filtered = filter_menu(filtered, field, value)
    else:
        field, value = split_filter(string)
        filtered = filter_menu(menu, field, value)

    return filtered

def get_metadata(menu, name):
    """Return metadata for reference"""
    meta = menu.loc[menu['name'] == name]
    cols = ['common_name', 'custom', 'description', 'downloader',
        'ensembl_release_number', 'name', 'ncbi_taxon_id', 'organism',
        'organization']

    if 'genbank' in meta.columns:
        cols.append('genbank')
    if 'refseq' in meta.columns:
        cols.append('refseq')

    return meta[cols]

def pretty_print(menu):
    """Print table with puppy emoji"""
    tt_data = [list(menu)]
    for row in menu.iterrows():
        tt_data.append(list(row[1]))
    tab = terminaltables.SingleTable(tt_data, title=u" \U0001F436" + " RefChef Menu ")

    print(tab.table)


def read_menu_from_local(file_path):
    """Looks for master.yml in config.reference_dir
    stops if it doesn't find anything, returns menu if master.yml is present"""
    try:
        master = read_yaml(os.path.join(file_path, "master.yml"))
    except:
        master = read_yaml(os.path.join(file_path, "master.yaml"))

    return master

def read_menu(conf):
    """Looks for master.yml in config.reference_dir, if file not found,
    retrieves it from GitHub"""
    try:
        master = read_menu_from_local(conf.git_local)
    except FileNotFoundError:
        print("Master YAML not found in your current path. Reading from GitHub.")
        master = read_menu_from_github(conf)

    return master
