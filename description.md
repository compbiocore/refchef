# This file contains a description of the refchef repo, including folder organization and functions.

- The `docs` folder contains several markdown files that comprise the documentation for how to use refchef. There's also an `assets` folder that contains all the images embedded in the documentation.
- the `mkdocs` file in the home directory specifcies how these markdown files are organized on the compbiocore website.
- the `refchef` folder contains all the python scripts for refchefs functioning under the hood.
- the `scripts` folder contains some python scripts that don't have a .py extension, the names of the scripts are the main functions of refchef so maybe the lack of .py extensions is related to them being the forward-facing parts of refchef?
- the `tests` folder tests the functions in the `refchef` folder.

questions:
what is the difference between `scripts` and `refchef` folder?
    - the names of the files in the `scripts` folder correspond to the actual commands you use to run refchef and they are referenced in setup.py, so maybe these are related to the actual packaging of refchef? 
what are `tests/__init__.py` and `tests/__init__.pyc`? .pyc files are compiled bytecode files, which aren't strictly necessary but help save compilation time
what is `.env.template`? `setup.cfg` and `setup.py`? setuptools docs things

`refchef-cook` imports:
from refchef import config
from refchef.utils import *
from refchef.table_utils import *
from refchef.references import *
import refchef.github_utils as gh
but the first two are unused according to pycharm

`refchef-cook`
- checks the command line arguments and config files and initializes some logging, using argparse and logging and datetime
- starting on 103 runs `utils.merge_yaml`, which adds the new yaml to master yaml and `read_menu`, which checks in pwd for the master.yaml and if it isn't there it pulls it from github, it prints some information about whats being added to refchef and adds information to the logs.
- starting at 130 are the lines where the commands are run (`execute(conf, 'master.yaml')`) and some more logging is done.
- starting at 142 is where the git commits and pushes happen.

`refchef-menu`
- checks command line arguments, configs, and yamls for args and initializes some logging
- runs `read_yaml` and `get_full_menu` to print a ref table

`refchef-serve`
- checks arguments and initializes some logging
- starting on line 29 is where the flask app is described -- runs `read_yaml` and `get_items` and returns an html table of the references or `items`.

- add a feature and make sure it behaves 
