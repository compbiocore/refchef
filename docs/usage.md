### Usage

RefChef comes with two main commands (`refchef-cook` and `refchef-menu`).
When using either of the commands, you'll be prompted to create a `.refchef-config` file. Alternatively,
you can create the config file in your home directory.

Here's an example of `.refchef.config`. The config file will set the basic requirements of refchef. It stores the name of the directories where the references will be saved, the local git repository path as well as the remote (this is where the `master.yaml` is stored). In addition you can set up log and runtime options.

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

### `refchef-cook`  
This command will read a `master.yaml` located in the `github-directory` path from the config file. The `master.yaml` file contains a list of references, as well as metadata, and commands necessary to download them (see example below).  
The `master.yaml` file stores all the information about a reference that is downloaded or will be downloaded. When `refchef-cook -e` is executed, the references in the master file that are not installed in the path provided in the config file will be downloaded. 

Arguments:  
`--execute, -e`: will execute all commands listed in the `master.yaml` for each reference, if reference doesn't exist in the location provided in the config file.  
`--new, -n`: path to a new yaml file containing other references to be downloaded and appended to the `master.yaml`.  
`--update, -u`: whether to update the remote git repository with the new `master.yaml`.

Example run:  
  1 - This will read in `new.yaml` file, append to `master.yaml` and update the remote GitHub repository.
    `refchef-cook -e --new new.yaml --update`.

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

![menu](assets/menu-full.png)

`refchef-menu --filter species:human`

![menu](assets/menu-filtered.png)
