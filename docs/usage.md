RefChef comes with two main commands (`refchef-cook` and `refchef-menu`). `refchef-cook` will read the recipes and execute the commands that will retrieve the references, indices, or annotations. `refchef-menu` provides an easy way to summarize the items already on the system.

#### User workflow diagram

![Diagram](assets/refchef-diagram.svg)

RefChef comes with two main scripts. `refchef-cook` will parse `master.yaml`, execute the commands listed (download and process reference files), commit, and push the `master.yaml` using git. `refchef-menu` is used to list the references already downloaded and processed. It also provides an easy way to find a reference uuid for use when processing new indices.
Both scripts can take a `--config (-c)` argument with the path for a config file, that can be one of the following formats:

`cfg.yaml`:
```yaml
config-yaml:
  path-settings:
    reference-directory: ~/data/references_dir # directory where references will be downloaded and processed.
    github-directory: ~/data/git_local # local git repository where `master.yaml` is located.
    remote-repository: user/repo # remote user and repository for version control of `master.yaml`
  log-settings:
    log: 'yes'
```

`cfg.ini`:
```toml
[path-settings]
reference-directory=~/data/references_dir #directory where references will be downloaded and processed.
git-directory=~/data/git_local #local git repository where `master.yaml` is located.
remote-repository=user/repo # remote user and repository for version control of `master.yaml`
[log-settings]
log=yes
[runtime-settings]
break-on-error=yes
verbose=yes
```

!!! Note
    You can opt not to use a config file. In that case, when using `refchef-menu`, you must pass the argument `--master (-m)` with he path to the `master.yaml` file.
    When using `refchef-cook`, you must pass at least the output directory (``--outdir, -o`) and the path to the local git directory, where the `master.yaml` file is located (``--git_local, -gl`). If you want the changes to `master.yaml` to be pushed to a git service, you must also pass `--git_remote (-gr)`.

### `refchef-cook`

#### Downloading and processing references, indices, or annotations.
This command will read a `master.yaml` located in the `github-directory` path from the config file, or the directory passed to `--git_local`. The `master.yaml` file contains a list of references, indices, and annotations, as well as their metadata, and commands necessary to download and process the files (see example below).  
The `master.yaml` file stores all the information about a reference that is downloaded or will be downloaded. When `refchef-cook -e` is executed, the files are downloaded to the output directory and processed. In addition, RefChef updates the status of the complete option to `true` in the  `master.yaml`, it also adds an `uuid`, the date, location, and list of files. If a reference has the `true` in the complete status, that entry will not be processed again.  

Example `master.yaml` before processing:  

```yaml
reference_test1:
  metadata:
    name: reference_test1
    species: mouse
    organization: ucsc
    downloader: fgelin
  levels:
    references:
    - component: primary
      complete:
        status: false
      commands:
      - wget -nv https://s3.us-east-2.amazonaws.com/refchef-tests/chr1.fa.gz
      - md5 *.fa.gz > postdownload_checksums.md5
      - gunzip *.gz
      - md5 *.fa > final_checksums.md5
```

Example `master.yaml` after processing:  
```yaml
reference_test1:
  metadata:
    name: reference_test1
    species: mouse
    organization: ucsc
    downloader: fgelin
  levels:
    references:
    - component: primary
      complete:
        status: true
        time: 2018-12-20 11:14:13.153237
      commands:
      - wget -nv https://s3.us-east-2.amazonaws.com/refchef-tests/chr1.fa.gz
      - md5 *.fa.gz > postdownload_checksums.md5
      - gunzip *.gz
      - md5 *.fa > final_checksums.md5
      location: refchef-data/reference_test1/primary
      files:
      - chr1.fa
      - metadata.txt
      - postdownload_checksums.md5
      - final_checksums.md5
      uuid: 8040b09f-3844-3c42-b765-1f6a32614895
```

#### Downloading an index linked to a reference.

Indices can be downloaded just like any reference or annotation (see process above), but also, one might download an index that is linked to a particular reference. In that case, the index entry in the `master.yaml` file has a key `src` that takes the `uuid` of the reference to be linked to the index.

Example of index `master.yaml`:
```yaml
index_1:
  metadata:
    name: index_test1
    species: mouse
    organization: ucsc
    downloader: fgelin
  levels:
    indices:
    - component: bwa_index
      complete:
        status: false
      src: 8040b09f-3844-3c42-b765-1f6a32614895
      commands:
      - wget -nv https://s3.us-east-2.amazonaws.com/refchef-tests/chr1.fa.gz
      - md5 *.fa.gz > postdownload_checksums.md5
      - gunzip *.gz
      - md5 *.fa > final_checksums.md5
```

In this case, the commands will be processed like before, but in the reference folder, a symlink to the index folder will be created.

Arguments:  
`--execute, -e`: will execute all commands listed in the `master.yaml` for each reference, if reference doesn't exist in the location provided in the config file.  
`--new, -n`: path to a new yaml file containing other references to be downloaded and appended to the `master.yaml`.
`--git, -g`: Git action. Choose from `commit` or `push`.
`--outdir, -o`: output directory, where references will be downloaded to.
`--git_local, -gl`: Local git directory, where the `master.yaml` file can be found.
`--git_remote, -gr`: Remote git repository, in the format `user/project_name`.
`--logs, -l`: Whether to save the log files.

Example run:  
  1 - This will read in `new.yaml` file, append to `master.yaml` and commit the changes using git.
    `refchef-cook --config /path/to/cfg.yaml --execute --new new.yaml --git commit`.

  2 - This will process `master.yaml`, commit and push changes to the remote repository:  
    `refchef-cook --execute -o /path/to/output/dir --git_local /path/to/git/dir --git_remote user/project_name --git push`


### `refchef-menu`
This command provides a way for the user to list all references present in the system, based on `master.yaml`, as well as filter the list of references based on metadata options.  
Arguments:  
`--master, -m`: path to `master.yaml` file. Must be used if `--config` argument is not used.
`--filter`: used to filter references based on metadata. Takes a pair key:value, or a list of pairs separated by comma: `key:value,key2:value2,key3:value3...`
`--full`: whether to show the full table including files and location of files.

Example:

`refchef-menu`

![menu](assets/menu-full.png)

`refchef-menu --filter species:human`

![menu](assets/menu-filtered.png)
