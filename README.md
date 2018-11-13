### RefChef

[![Travis](https://img.shields.io/travis/compbiocore/refchef/master.svg?style=flat-square)](https://travis-ci.org/compbiocore/refchef)
[![Coverage](https://img.shields.io/coveralls/github/rechef/refchef/master.svg?style=flat-square)](https://coveralls.io/github/compbiocore/refchef) [![Docs](https://img.shields.io/badge/docs-stable-blue.svg?style=flat-square)](https://compbiocore.github.io/cbc-documentation-templates)
[![License](https://img.shields.io/badge/license-GPL_3.0-orange.svg?style=flat-square)](https://raw.githubusercontent.com/compbiocore/cbc-documentation-templates/master/LICENSE.md)  

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

### Usage

RefChef comes with two main commands (`refchef-cook` and `refchef-menu`).
When using either of the commands, you'll be prompted to create a `.refchef-config` file. Alternatively,
you can create the config file in your home directory.

Here's an example of `.refchef.config`
```yaml
config-yaml:
  path-settings:
    reference-directory: ~/data/references_dir # directory where references will be downloaded and processed.
    github-directory: ~/data/git_local # local git repository where `master.yaml` is located.
    remote-repository: user/repo # remote user and repository for version control of `master.yaml`
  log-settings:
    log: 'yes'
  runtime-settings:
    break-on-error: 'yes'
    verbose: 'yes'
```

### `refchef-cook`:  
This command will read a `master.yaml` located in the `github-directory` path from the config file. The `master.yaml` file contains a list of references, as well as metadata, and commands necessary to download them (see example below).  
Arguments:  
`--exectue, -e`: will execute all commands listed in the `master.yaml` for each reference, if reference doesn't exist in the location provided in the config file.  
`--new, -n`: path to a new yaml file containing other references to be downloaded and appended to the `master.yaml`.  
`--update, -u`: whether to update the remote git repository with the new `master.yaml`.

Example run:  
    1 - This will read in `new.yaml` file, append to `master.yaml` and update the remote GitHub repository.
    `refchef-cook -e --new new.yaml --update`  

    2 - This will process `master.yaml` only and won't update the remote GitHub repository:  
    `refchef-cook -e`


Example `master.yaml`
```yaml
reference_test1:
  metadata:
    name: reference_test1
    species: mouse
    organization: ucsc
    downloader: aleith
  levels:
    references:
      - component: primary
        retrieve: true
        commands:
          - curl https://s3.us-east-2.amazonaws.com/refchef-tests/chr1.fa.gz
          - md5 *.fa.gz > postdownload_checksums.md5
          - gunzip *.gz
          - md5 *.fa > final_checksums.md5
reference_test2:
  metadata:
    name: reference_test2
    species: human
    organization: ucsc
    downloader: fgelin
  levels:
    references:
      - component: primary
        retrieve: true
        commands:
          - curl https://s3.us-east-2.amazonaws.com/refchef-tests/chr1.fa.gz
          - md5 *.fa.gz > postdownload_checksums.md5
          - gunzip *.gz
          - md5 *.fa > final_checksums.md5
```


### `refchef-menu`
This command provides a way for the user to list all references present in the system, based on `master.yaml`, as well as filter the list of references based on metadata options.  
Arguments:  
`--filter`: used to filter references based on metadata. Takes a pair key:value, or a list of pairs separated by comma: `key:value,key2:value2,key3:value3...`

Example:

`refchef-menu`

![menu](docs/assets/menu-full.png)

`refchef-menu --filter species:human`

![menu](docs/assets/menu-filtered.png)



#### Contact
Contact cbc-help@brown.edu - this is our general help line, so please specify that your issue is with this site's contents
