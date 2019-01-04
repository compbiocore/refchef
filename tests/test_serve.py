import os
from refchef.utils import *
from refchef.serve import *

def test_get_items():
    master = read_yaml(os.path.join('tests/data/master.yaml'))
    items = get_items(master)

    for k in ['type', 'name', 'species', 'organization', 'component',
              'downloader', 'files', 'location', 'uuid']:
        assert k in items[0]

    assert len(items) == 2
    assert items[0]['name'] == 'reference_test1'
