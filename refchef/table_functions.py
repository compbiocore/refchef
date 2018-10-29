def get_full_menu(file_path):
    """Reads yaml file and converts to a table format"""

    #read in yaml file
    with open(file_path) as f:
        data = yaml.load(f)

    #json normalize data (to expand dict to table)
    df = json_normalize(data).T.reset_index()
    df.columns = ["a", "b"]

    #rearange data
    res = df.set_index(['a'])['b'].apply(pd.Series).stack()
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

    #create levels table
    levels = (pd.DataFrame(table[table["e"] == "levels"][["c.component", "f", "d"]]
                           .groupby(["f", "d"])["c.component"]
                           .apply(list))
              .reset_index()
              .set_index("f"))

    #create full table (menu)
    menu = metadata.join(types, how="right")
    menu.columns = ["downloader", "name", "organization", "species", "type", "component"]

    return menu


def filter_menu(menu, key, value):
    """Filters table based on key-value pair passed"""

    filtered = menu[menu[key] == value]
    return filtered
