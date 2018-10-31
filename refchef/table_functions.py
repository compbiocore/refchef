import json
import pandas as pd
from pandas.io.json import json_normalize
import terminaltables
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_full_menu(file_path):
    """Reads yaml file and converts to a table format"""

    #read in yaml file
    with open(file_path) as f:
        data = yaml.load(f)

    #json normalize data (to expand dict to table)
    df = json_normalize(data).T.reset_index()
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
    table = json_normalize(res.to_dict(orient="records"))

    #create matadata table
    metadata = table[table["e"] == "metadata"][["c", "d", "f"]].pivot(index="f", columns="d")
    metadata.columns = metadata.columns.droplevel()

    #create levels table
    levels = (pd.DataFrame(table[table["e"] == "levels"][["c.component", "f", "d"]]
                           .groupby(["f", "d"])["c.component"]
                           .apply(list))
              .reset_index()
              .set_index("f"))

    #create full table (menu)
    menu = metadata.join(levels, how="right")
    menu.columns = ["downloader", "name", "organization", "species", "type", "component"]
    menu = menu.reset_index().drop(columns="f")

    return menu


def filter_menu(menu, key, value):
    """Filters table based on key-value pair passed"""

    filtered = menu[menu[key] == value]
    return filtered

def split_filter(string):
    return string.split(":")

def multiple_filter(menu, string):
    if "," in string:
        l = string.split(",")
        for pair in l:
            field, value = split_filter(pair)
            filtered = filter_menu(menu, field, value)
    else:
        field, value = split_filter(string)
        filtered = filter_menu(menu, field, value)

    return filtered

def pretty_print(menu):
    tt_data = [list(menu)]
    for row in menu.iterrows():
        tt_data.append(list(row[1]))
    tab = terminaltables.SingleTable(tt_data, title=u" \U0001F436" + " RefChef Menu ")

    print(tab.table)
