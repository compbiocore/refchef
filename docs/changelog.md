# Brown CBC's RefChef Changelog


### Upcoming Features (in order of priority)


Option for S3 push of reference directory

Options to handle failed / partially failed downloads

Multiple options for handing duplicate reference names

Command-level execution control (such control currently exists only at the reference subcomponent level)


### Version 0.9.2 - 7/13/18


Appending with no execution now allows github autopush


### Version 0.9.1 - 7/12/18


Updated 'usage' and 'walkthrough' pages on this site to reflect the software's current status


### Version 0.9 - 7/11/18


Refactored configuration generation to use ordered dictionary

Fixed multiple bugs in interactive configuration generation

Optional github autopush added (controlled via config.yaml)

Added remote operation mode, including an option to download the remote master file


### Version 0.8.1 - 7/6/18


YAML dumping refactored

All internal subprocess commands replaced with python commands


### Version 0.8 - 6/27/18


Major overhaul to nearly every aspect of functionality

Name changed to 'RefChef'

append() function deprecated and supplanted by new_append()

All dictionaries changed to ordered dictionaries

Reference keys changed to use reference names

Local / remote structure implemented (only local functional as of now)

Git functionality partially implemented

Interactive configuration file prompts added, invoked if config file absent

Created function to dump an ordered dictionary as a YAML


### Version 0.7 - 6/8/18


Configuration file scheme added

Interactive config file generation added (autotriggered when no config file is present)

Began subparser implementation

### Version 0.61 - 5/29/18


Added a separate tutorial zip file for OSX and Linux due to different commands for creating md5 files

Fixed a minor issue causes by OSX's sed and subprocess integration (not present on Linux)

### Version 0.6 - 5/23/18


Fixed bug where blank lines in New YAML would cause incorrect appending and break execution

Added requirements information to the manual page

Added tutorial zip file to the github repository

### Version 0.5 - 5/21/18


Base version for describing future changes