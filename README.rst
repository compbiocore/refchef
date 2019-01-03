### RefChef

[![Travis](https://img.shields.io/travis/compbiocore/refchef/master.svg?style=flat-square)](https://travis-ci.org/compbiocore/refchef)
[![Coverage](https://img.shields.io/coveralls/github/rechef/refchef/master.svg?style=flat-square)](https://coveralls.io/github/compbiocore/refchef) [![Docs](https://img.shields.io/badge/docs-stable-blue.svg?style=flat-square)](https://compbiocore.github.io/refchef)
[![License](https://img.shields.io/badge/license-GPL_3.0-orange.svg?style=flat-square)](https://raw.githubusercontent.com/compbiocore/cbc-documentation-templates/master/LICENSE.md)
[![PyPi](https://img.shields.io/pypi/v/refchef.svg?style=flat-square)](https://pypi.org/project/refchef/)
---

RefChef is a reference management tool used to (1) document the exact steps undertaken in the retrieval of genomic references, (2) maintain the associated metadata, (3) provide a mechanism for automatically reproducing retrieval and creation of an exact copy of genomic references.

### Installation

To install from PyPI using **pip**:  
`pip install refchef`

To install using **Anaconda Python**:  
`conda install -c compbiocore refchef`


### Development
To install a **development version** from the current directory:  
```bash
git clone https://github.com/compbiocore/refchef.git
cd refchef
pip install -e .
```

Run unit tests as:
`python setup.py test`

### Set up `.env` file with GitHub Access Token
Sensitive environment variables are stored in the .env file. This file is included in .gitignore intentionally, so that it is never committed.
- Create a `.env` file and copy into it the contents of `.env.template`
- Get your [GitHub Access Token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) and add to the `.env` file.

### Contributing

Contributions consistent with the style and quality of existing code are welcome. Be sure to follow the guidelines below.

Check the issues page of this repository for available work.

#### Committing

This project uses [commitizen][commitizen] to
ensure that commit messages remain well-formatted and consistent across
different contributors.

Before committing for the first time, install commitizen and read [Conventional Commits][conventional-commits].

```
pip install commitizen
```

To start work on a new change, pull the latest `develop` and create
a new _topic branch_ (e.g. `feature-resume-model`, `chore-test-update`,
`bugfix-bad-bug`).

```
git add .
```

To commit, run the following command (instead of `git commit`) and follow the
directions:

```
cz commit
```


#### Contact
Contact cbc-help@brown.edu - this is our general help line, so please specify that your issue is with this site's contents

[commitizen]: https://pypi.org/project/commitizen/
[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0-beta.2/
