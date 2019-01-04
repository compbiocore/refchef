from refchef.table_utils import *

def get_items(master):
    menu = get_full_menu(master)

    items = []
    for i, r in menu.iterrows():
        item = {'type': r['type'],
                'name': r['name'],
                'species': r['species'],
                'organization': r['organization'],
                'component': r['component'],
                'downloader': r['downloader'],
                'files': ", ".join(r['files']),
                'location': r['location'],
                'uuid': r['uuid']}
        items.append(item)
    return items
