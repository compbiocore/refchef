### Overview 
RefChef comes with two main commands ([`refchef-cook`](#refchef-cook) and [`refchef-menu`](#refchef-menu)). 

- [**refchef-cook**](#refchef-cook): Will read recipes and execute the commands that will retrieve the references, indices, or annotations. 
- [**refchef-menu**](#refchef-menu): This command provides a way for the user to list all references present in the system, based on [`master.yaml`](#master.yaml), as well as filter the list of references based on metadata options. 

In addition to the [`refchef-cook`](#refchef-cook) and [`refchef-menu`](#refchef-menu) commands, RefChef requires a [`master.yaml`](#master.yaml) containing a list of references, indices, and annotations, as well as their metadata, and commands necessary to download and process the files. When [`refchef-cook`](#refchef-cook) is executed, RefChef will append the [`master.yaml`](#master.yaml) to change the `complete` option from `false` to `true` and will also add a `uuid` for each reference, the date the files were downloaded and their location, as well as a complete list of files. 

RefChef also requires some configuration information, including:

1. Where you'd like the references to be saved 
2. The local git repository for version control of references
3. The remote github repository for version control of reference
  sequences (optional).

This information can be specified in a [`cfg.yaml`](#cfg.yaml) or [`cfg.ini`](#cfg.ini) file or it can be passed as arguments to [`refchef-cook`](#refchef-cook). 

### Quickstart
**The following example uses a local repository for tracking references.**

Create your own local repository for tracking references:
```
cd /Volumes/jwalla12
git init local_references
```

Create a directory for refchef to store your references:
```
mkdir /Volumes/jwalla12/references
```

Create a [`master.yaml`](#master.yaml) file and save it in your git repository directory. As a minimal example, here is a [`master.yaml`](#master.yaml) file that will download the grch38 human genome from Ensembl:

```
grch38:
  metadata:
    name: grch38
    organism: Homo sapiens
    common_name: human
    ncbi_taxon_id: 9606
    organization: ensembl
    description: Genome Reference Consortium Human Build 38
    genbank_accession: 
    refseq_accession:
    ensembl_release_number: 87
    custom: no
    downloader: jrwallace
  levels:
    references:
    - component: primary
      complete:
        status: false
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/CHECKSUMS
      - md5sum *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5sum *.* > final_checksums.md5

```
In addition to the .yaml file, you will also need to create a `cfg.ini` or `cfg.yaml` configuration file that specifies the
following details:



You can also pass these details as arguments to `refchef-cook`, as in the following example:

```
refchef-cook -e -o /Volumes/jwalla12/references -gl /Volumes/jwalla12/local_references
```

After running `refchef-cook`, you'll see the following:

```
(base) CIS2703FHTDH:local_references jwalla12$ refchef-cook -e -o /Volumes/jwalla12/references -gl /Volumes/jwalla12/local_references
/anaconda3/lib/python3.7/site-packages/refchef/utils.py:13: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  dict_ = yaml.load(yml)
2019-07-16 10:34:12,972 INFO: 
        ===========================================
        REFCHEF 🐶
        -------------------------------------------
        - References will be downloaded to: /Volumes/jwalla12/references
        - Remote repository for master.yaml False
        - Local repository for master.yaml /Volumes/jwalla12/local_references
        - Logs files: /Volumes/jwalla12/local_references/logs/
        -------------------------------------------
        

        ===========================================
        REFCHEF 🐶
        -------------------------------------------
        - References will be downloaded to: /Volumes/jwalla12/references
        - Remote repository for master.yaml False
        - Local repository for master.yaml /Volumes/jwalla12/local_references
        - Logs files: /Volumes/jwalla12/local_references/logs/
        -------------------------------------------
        
2019-07-16 10:34:12,972 INFO: 
        -------------------------------------------
        The folowing references will be downloaded:
            - grch38
        ===========================================
            

        -------------------------------------------
        The folowing references will be downloaded:
            - grch38
        ===========================================
            
2019-07-16 10:34:12,974 INFO:  🐶 RefChef... getting reference: grch38, component: primary
 🐶 RefChef... getting reference: grch38, component: primary
2019-07-16 10:34:12,975 INFO: Running command "wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
Running command "wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
--2019-07-16 10:34:12--  ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
           => ‘Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz’
Resolving ftp.ensembl.org (ftp.ensembl.org)... 193.62.193.8
Connecting to ftp.ensembl.org (ftp.ensembl.org)|193.62.193.8|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /pub/release-87/fasta/homo_sapiens/dna ... done.
==> SIZE Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz ... 881214448
==> PASV ... done.    ==> RETR Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz ... done.
Length: 881214448 (840M) (unauthoritative)

Homo_sapiens.GRCh38 100%[===================>] 840.39M  10.6MB/s    in 91s     

2019-07-16 10:35:46 (9.24 MB/s) - ‘Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz’ saved [881214448]

2019-07-16 10:35:46,020 INFO: Running command "wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/CHECKSUMS"
Running command "wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/CHECKSUMS"
--2019-07-16 10:35:46--  ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/CHECKSUMS
           => ‘CHECKSUMS’
Resolving ftp.ensembl.org (ftp.ensembl.org)... 193.62.193.8
Connecting to ftp.ensembl.org (ftp.ensembl.org)|193.62.193.8|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /pub/release-87/fasta/homo_sapiens/dna ... done.
==> SIZE CHECKSUMS ... 5010
==> PASV ... done.    ==> RETR CHECKSUMS ... done.
Length: 5010 (4.9K) (unauthoritative)

CHECKSUMS           100%[===================>]   4.89K  --.-KB/s    in 0s      

2019-07-16 10:35:48 (50.3 MB/s) - ‘CHECKSUMS’ saved [5010]

2019-07-16 10:35:48,338 INFO: Running command "md5 *.gz > postdownload-checksums.md5"
Running command "md5 *.gz > postdownload-checksums.md5"
2019-07-16 10:35:50,186 INFO: Running command "gunzip *.gz"
Running command "gunzip *.gz"
2019-07-16 10:36:47,937 INFO: Running command "md5 *.* > final_checksums.md5"
Running command "md5 *.* > final_checksums.md5"
2019-07-16 10:37:16,145 INFO: References processed: ['grch38']
References processed: ['grch38']
2019-07-16 10:37:16,145 INFO: Location of references: /Volumes/jwalla12/references
Location of references: /Volumes/jwalla12/references

```

After this command is run, master.yaml will reflect that you have downloaded the references and it will now look like this:

```
grch38:
  metadata:
    name: grch38_release87
    species: Homo sapiens
    organization: ensembl
    downloader: jrwallace
  levels:
    references:
    - component: primary
      complete:
        status: true
        time: 2019-07-12 16:02:25.505498
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/dna/CHECKSUMS
      - md5sum *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5sum *.* > final_checksums.md5
      location: /Volumes/jwalla12/references/grch38/primary
      files:
      - CHECKSUMS
      - final_checksums.md5
      - Homo_sapiens.GRCh38.dna.primary_assembly.fa
      - metadata.txt
      - postdownload-checksums.md5

```


todo: add information re: adding references already present elsewhere (should the command be more like a cp command?)

### **refchef-cook**

Will read recipes and execute the commands that will retrieve the references, indices, or annotations.

Usage: `refchef-cook [*arguments*]`

Arguments:  
`--execute, -e`: will execute all commands listed in the `master.yaml` for each reference, if reference doesn't exist in the location provided in the config file.  
`--new, -n`: path to a new yaml file containing other references to be downloaded and appended to the `master.yaml`.
`--git, -g`: Git action. Choose from `commit` or `push`.
`--outdir, -o`: output directory, where references will be downloaded to.
`--git_local, -gl`: Local git directory, where the `master.yaml` file can be found.
`--git_remote, -gr`: Remote git repository, in the format `user/project_name`.
`--logs, -l`: Whether to save the log files.

Example:  
  1 - This will read in `new.yaml` file, append to `master.yaml` and commit the changes using git.
    `refchef-cook --config /path/to/cfg.yaml --execute --new new.yaml --git commit`.

  2 - This will process `master.yaml`, commit and push changes to the remote repository:  
    `refchef-cook --execute -o /path/to/output/dir --git_local /path/to/git/dir --git_remote user/project_name --git push`


### **refchef-menu**
This command provides a way for the user to list all references present in the system, based on `master.yaml`, as well as filter the list of references based on metadata options.  

Usage: `refchef-cook [*arguments*]`

Arguments:  
`--master, -m`: path to `master.yaml` file. Must be used if `--config` argument is not used.
`--filter`: used to filter references based on metadata. Takes a pair key:value, or a list of pairs separated by comma: `key:value,key2:value2,key3:value3...`
`--full`: whether to show the full table including files and location of files.

Example:
`refchef-menu`

![menu](assets/menu-full.png)

`refchef-menu --filter species:human`

![menu](assets/menu-filtered.png)




Arguments:



# Config
# Refchef-menu


#### User workflow diagram

![Diagram](assets/refchef-diagram.svg)

RefChef comes with two main scripts. `refchef-cook` will parse `master.yaml`, execute the commands listed (download and process reference files), commit, and push the `master.yaml` using git. `refchef-menu` is used to list the references already downloaded and processed. It also provides an easy way to find a reference uuid for use when processing new indices.
Both scripts can take a `--config (-c)` argument with the path for a config file, that can be one of the following formats:

`cfg.yaml`:
```yaml
config-yaml:
  path-settings:
    reference-directory: ~/data/references_dir # directory where references will be downloaded and processed.
    git-directory: ~/data/git_local # local git repository where `master.yaml` is located.
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

### master.yaml name and header must match

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

