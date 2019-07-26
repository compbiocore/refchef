
## **Overview** 
RefChef is a reference management tool that helps make your sequencing projects and analyses reproducible. You can use it to document the provenance of reference sequences downloaded from public databases, as well as their associated indices and annotations. It is a flexible workflow that could also be used to internally track the progress through different versions of draft assemblies. RefChef will:   

1. Document the exact steps undertaken in the retrieval and processing of genomic references   
2. Maintain the associated metadata   
3. Provide a mechanism for automatically reproducing retrieval and creation of an exact copy of genomic references  

**RefChef comes with two commands:**      

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[**`refchef-cook`**](#refchef-cook):     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Will read recipes and execute the commands that will retrieve the references, indices, or   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; annotations based on the contents of [`master.yaml`](#master.yaml).     

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[**`refchef-menu`**](#refchef-menu):   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Provides a way for the user to list all references present in the system, based   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; on [`master.yaml`](#master.yaml), as well as filter the list of references based on metadata options. 
![Diagram](assets/refchef-diagram.svg)


**RefChef requires a `master.yaml` file:**      

In addition to the [`refchef-cook`](#refchef-cook) and [`refchef-menu`](#refchef-menu) commands, RefChef requires a [`master.yaml`](#master.yaml) containing a list of references, indices, annotations, and metadata, as well as the commands necessary to download and process the files. When [`refchef-cook`](#refchef-cook) is executed, RefChef will append the [`master.yaml`](#master.yaml) to change the `complete` option from `false` to `true`and will also add a `uuid` for each reference, the date the files were downloaded and their location, as well as a complete list of files. Based on the arguments you pass to [`refchef-cook`](#refchef-cook), it will either commit those changes to [`master.yaml`](#master.yaml) to a local repository or commit and push the changes to a remote repository. 

**RefChef requires configuration information:**      

[`refchef-cook`](#refchef-cook) and [`refchef-menu`](#refchef-menu) both require some configuration information, including:

1. Where you'd like the references to be saved 
2. The local git repository for version control of references   
3. The remote github repository for version control of reference
  sequences (optional).   

This information can be specified in a [`cfg.yaml`](#cfg.yaml) file, a [`cfg.ini`](#cfg.ini) file, or it can be passed as arguments to [`refchef-cook`](#refchef-cook). 

## **Quickstart**

This quickstart assumes that [bwa](http://bio-bwa.sourceforge.net/) and [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) are installed and in your current path.

Create a [remote repository](https://help.github.com/en/articles/creating-a-new-repository) and [clone it](https://help.github.com/en/articles/cloning-a-repository).  

Create a directory for refchef to save your references.

Create a [`master.yaml`](#master.yaml) file and save it in your local git repository directory. Here is a [`master.yaml`](#master.yaml) file that will download a yeast genome from Ensembl:

```yaml
S_cerevisiae:
  metadata:
    name: S_cerevisiae
    common_name: yeast
    ncbi_taxon_id: 4932
    organism: Saccharomyces cerevisiae
    organization: ensembl
    custom: no
    description: corresponds to genbank id GCA_000146045.2
    downloader: joselynn wallace
    ensembl_release_number: 87
    accession:
      genbank:
      refseq:
  levels:
    references:
    - component: primary
      complete:
        status: false
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
```
Pass the configuration arguments in a config file or directly to [`refchef-cook`](#refchef-cook) (as seen in the following example):

```
refchef-cook -e -o /Users/jwalla12/references -gl /Users/jwalla12/remote_references -gr jrwallace/remote_references --git commit -l
```

After [`refchef-cook`](#refchef-cook) is run, [`master.yaml`](#master.yaml) will reflect that you have downloaded the reference and it will now look like this:

```yaml
S_cerevisiae:
  metadata:
    name: S_cerevisiae
    common_name: yeast
    ncbi_taxon_id: 4932
    organism: Saccharomyces cerevisiae
    organization: ensembl
    custom: false
    description: corresponds to genbank id GCA_000146045.2
    downloader: joselynn wallace
    ensembl_release_number: 87
    accession:
      genbank: null
      refseq: null
  levels:
    references:
    - component: primary
      complete:
        status: true
        time: '2019-07-25 09:08:37.478553'
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
      location: /Users/jwalla12/references/S_cerevisiae/primary
      files:
      - metadata.txt
      - postdownload-checksums.md5
      - CHECKSUMS
      - final_checksums.md5
      - Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      uuid: dff337a6-9a1d-3313-8ced-dc6f3bfc9689
```

Make another .yaml file to create a bowtie2 index of this genome, call the file `bowtie2.yaml`.

```yaml
S_cerevisiae:
  levels:
    indices:
    - component: bowtie2_index
      complete:
        status: false
      src: dff337a6-9a1d-3313-8ced-dc6f3bfc9689 
      commands:
      - mkdir /Users/jwalla12/references/S_cerevisiae/bowtie2_index
      - cd /Users/jwalla12/references/S_cerevisiae/bowtie2_index
      - ln -s /Users/jwalla12/references/S_cerevisiae/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa /Users/jwalla12/references/S_cerevisiae/bowtie2_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - bowtie2-build /Users/jwalla12/references/S_cerevisiae/bowtie2_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa S_cerevisiae
      - md5 /Users/jwalla12/references/S_cerevisiae/bowtie2_index/*.* > /Users/jwalla12/references/S_cerevisiae/bowtie2_index/final_checksums.md5
```

!!! Caution 
    Note that in the above example of a new YAML, metadata entries present in the initial [`master.yaml`](#master.yaml) file have been omitted (for example, `ncbi_taxon_id:`, `common_name:`). When adding indices or annotations to a primary reference already in [`master.yaml`](#master.yaml), the metadata in [`master.yaml`](#master.yaml) will be overwritten by the metadata in the new.yaml file. This could be helpful in situations where you want to update the metadata fields.


Then use [`refchef-cook`](#refchef-cook) and specify the new yaml to add to [`master.yaml`](#master.yaml).

```
refchef-cook -e -o /Users/jwalla12/references -gl /Users/jwalla12/remote_references -gr jrwallace/remote_references -n /Users/jwalla12/remote_references/bowtie2.yaml -g commit -l
```

Make another .yaml file to create a bwa index of this genome, call the file `bwa.yaml`.

```yaml
S_cerevisiae:
  levels:
    indices:
    - component: bwa_index
      complete:
        status: false
      src: dff337a6-9a1d-3313-8ced-dc6f3bfc9689 
      commands:
      - mkdir /Users/jwalla12/references/S_cerevisiae/bwa_index
      - cd /Users/jwalla12/references/S_cerevisiae/bwa_index
      - ln -s /Users/jwalla12/references/S_cerevisiae/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa /Users/jwalla12/references/S_cerevisiae/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - bwa index /Users/jwalla12/references/S_cerevisiae/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa > /Users/jwalla12/references/S_cerevisiae/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - md5 /Users/jwalla12/references/S_cerevisiae/bwa_index/*.* > /Users/jwalla12/references/S_cerevisiae/bwa_index/final_checksums.md5
```

Then use [`refchef-cook`](#refchef-cook) and specify the new yaml to add to [`master.yaml`](#master.yaml).

```
refchef-cook -e -o /Users/jwalla12/references -gl /Users/jwalla12/remote_references -gr jrwallace/remote_references -n /Users/jwalla12/remote_references/bwa.yaml -g commit -l
```

We can also track annotation files for the reference genome. Make the following .yaml file and call it `gtf.yaml`:

```yaml
S_cerevisiae:
  levels:
    annotations:
    - component: gtf
      complete:
        status: false
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.87.gtf.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/gtf/saccharomyces_cerevisiae/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
```

Then use [`refchef-cook`](#refchef-cook) and specify the new yaml to add to [`master.yaml`](#master.yaml). 

```
refchef-cook -e -o /Users/jwalla12/references -gl /Users/jwalla12/remote_references -gr jrwallace/remote_references -n /Users/jwalla12/remote_references/gtf.yaml -g commit -l
```
We can see what references are available using [`refchef-menu`](#refchef-menu):
```
refchef-menu -f /Users/jwalla12/remote_references/master.yaml
```
```
┌ 🐶 RefChef Menu ────────────────────────┬───────────────┬───────────────────────────────────────────┬──────────────────────────────────────┐
│ name         │ organism                 │ component     │ description                               │ uuid                                 │
├──────────────┼──────────────────────────┼───────────────┼───────────────────────────────────────────┼──────────────────────────────────────┤
│ S_cerevisiae │ Saccharomyces cerevisiae │ gtf           │ corresponds to genbank id GCA_000146045.2 │ 5f7ae94c-2e51-3cc6-bcbf-6e251c75ef2f │
│ S_cerevisiae │ Saccharomyces cerevisiae │ bowtie2_index │ corresponds to genbank id GCA_000146045.2 │ 93393699-cb40-3ad7-ac07-ae4bdb1efd3e │
│ S_cerevisiae │ Saccharomyces cerevisiae │ bwa_index     │ corresponds to genbank id GCA_000146045.2 │ 482c6e70-389e-3559-8c19-d86cac067060 │
│ S_cerevisiae │ Saccharomyces cerevisiae │ primary       │ corresponds to genbank id GCA_000146045.2 │ dff337a6-9a1d-3313-8ced-dc6f3bfc9689 │
└──────────────┴──────────────────────────┴───────────────┴───────────────────────────────────────────┴──────────────────────────────────────┘
```
We can also get this information if we look at [`master.yaml`](#master.yaml):
```yaml
S_cerevisiae:
  metadata:
    name: S_cerevisiae
    common_name: yeast
    ncbi_taxon_id: 4932
    organism: Saccharomyces cerevisiae
    organization: ensembl
    custom: false
    description: corresponds to genbank id GCA_000146045.2
    downloader: joselynn wallace
    ensembl_release_number: 87
    accession:
      genbank: null
      refseq: null
  levels:
    references:
    - component: primary
      complete:
        status: true
        time: '2019-07-25 16:26:42.700668'
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
      location: /Users/jwalla12/references/S_cerevisiae/primary
      files:
      - metadata.txt
      - postdownload-checksums.md5
      - CHECKSUMS
      - final_checksums.md5
      - Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      uuid: dff337a6-9a1d-3313-8ced-dc6f3bfc9689
    indices:
    - component: bowtie2_index
      complete:
        status: true
        time: '2019-07-25 16:26:43.971349'
      src: dff337a6-9a1d-3313-8ced-dc6f3bfc9689
      commands:
      - mkdir /Users/jwalla12/references/yeast_refs/bowtie2_index
      - cd /Users/jwalla12/references/yeast_refs/bowtie2_index
      - ln -s /Users/jwalla12/references/yeast_refs/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
        /Users/jwalla12/references/yeast_refs/bowtie2_index/
      - bowtie2-build /Users/jwalla12/references/yeast_refs/bowtie2_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
        S_cerevisiae
      - md5 /Users/jwalla12/references/yeast_refs/bowtie2_index/*.* > /Users/jwalla12/references/yeast_refs/bowtie2_index/final_checksums.md5
      location: /Users/jwalla12/references/S_cerevisiae/bowtie2_index
      files:
      - metadata.txt
      uuid: 84928c3e-af1a-11e9-a45e-8c8590bd206d
    - component: bwa_index
      complete:
        status: true
        time: '2019-07-25 16:26:45.183284'
      src: dff337a6-9a1d-3313-8ced-dc6f3bfc9689
      commands:
      - mkdir /Users/jwalla12/references/yeast_refs/bwa_index
      - cd /Users/jwalla12/references/yeast_refs/bwa_index
      - ln -s /Users/jwalla12/references/yeast_refs/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
        /Users/jwalla12/references/yeast_refs/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - bwa index /Users/jwalla12/references/yeast_refs/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
        > /Users/jwalla12/references/yeast_refs/bwa_index/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - md5 /Users/jwalla12/references/yeast_refs/bwa_index/*.* > /Users/jwalla12/references/yeast_refs/bwa_index/final_checksums.md5
      location: /Users/jwalla12/references/S_cerevisiae/bwa_index
      files:
      - metadata.txt
      uuid: 854b7780-af1a-11e9-a9f8-8c8590bd206d
    annotations:
    - component: gtf
      complete:
        status: true
        time: '2019-07-25 16:26:54.326082'
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.87.gtf.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/gtf/saccharomyces_cerevisiae/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
      location: /Users/jwalla12/references/S_cerevisiae/gtf
      files:
      - metadata.txt
      - postdownload-checksums.md5
      - Saccharomyces_cerevisiae.R64-1-1.87.gtf
      - CHECKSUMS
      - final_checksums.md5
      uuid: 5f7ae94c-2e51-3cc6-bcbf-6e251c75ef2f
```
## **Usage**

###**refchef-cook** <a name="refchef-cook"></a> 

Refchef-cook reads recipes (yaml files) and executes the commands that will retrieve and/or process the references, indices, or annotations.


**usage:**
```
refchef-cook [*arguments*]
```
**arguments:**
```  
--help, -h         Show this help message and exit. 

--execute, -e      Executes the YAML file (master or new if specified).  

--append, -a       Will append commands to the master YAML.

--new, -n          Full path to the new YAML.      

--git, -g          Git commands to use, choose from `commit` or `push`.

--outdir, -o       Output folder where references will be stored. 

--git_local, -gl   Required, git folder where the `master.yaml` is stored.  

--git_remote, -gr  Remote git repository (in the format `user/project_name`). 

--config, -c       Path to config file (.yaml or .ini format).     

--logs, -l         Whether to save the log files.    
```
**examples:**       
    1. This will read in `new.yaml` file, append to `master.yaml` and commit the changes using git: 
`refchef-cook --config /path/to/cfg.yaml --execute --new new.yaml --git commit`.   
    2. This will process `master.yaml`, commit and push changes to the remote repository:    
`refchef-cook --execute -o /path/to/output/dir --git_local /path/to/git/dir --git_remote user/project_name --git push`.   



###**refchef-menu** <a name="refchef-menu"></a> 

Refchef-menu provides a way for the user to list all references present in the system, based on `master.yaml`, as well as filter the list of references based on metadata options. You must specify either `--master, -m` or `--config, -c`. 

**usage:**
```   
refchef-menu [*arguments*]
```
**arguments:**
```         
--help, -h         Show this help message and exit. 

--filter           Field:value pair for filtering menu.    

--master, -f       Path to `master.yaml` file, needed if `-c` argument unused.    

--config, -c       Path to config file in .yaml or .ini format.    

--full             Will show full table (including files and their locations).    

--meta, -m         Return metadata for a specific reference.     
```
**example:**     
  1 - This will look at all primary genome references available in the current system:     
`refchef-menu -f /Users/jwalla12/remote_references/master.yaml --filter component:primary`
```
┌ 🐶 RefChef Menu ────────────────────────┬───────────┬───────────────────────────────────────────┬──────────────────────────────────────┐
│ name         │ organism                 │ component │ description                               │ uuid                                 │
├──────────────┼──────────────────────────┼───────────┼───────────────────────────────────────────┼──────────────────────────────────────┤
│ S_cerevisiae │ Saccharomyces cerevisiae │ primary   │ corresponds to ganbank id GCA_000146045.2 │ dff337a6-9a1d-3313-8ced-dc6f3bfc9689 │
└──────────────┴──────────────────────────┴───────────┴───────────────────────────────────────────┴──────────────────────────────────────┘
```

## **Inputs**
###**master.yaml** <a name="master.yaml"></a>    

**master.yaml overview**      
Refchef makes use of YAML files that are composed of nested entry and value pairs -- for example, the entry and value pair `common_name`: `yeast`. The spacing and indentation of the entries and values are meaningful - Refchef uses the convention of using 2 spaces to indent each subsequent level of the entries and values in the YAML. Additionally, the spaces and colons are important: be sure to include a `:` and space between each entry and value. 

Example `master.yaml` before processing:
```yaml
S_cerevisiae:
  metadata:
    name: S_cerevisiae
    common_name: yeast
    ncbi_taxon_id: 4932
    organism: Saccharomyces cerevisiae
    organization: ensembl
    custom: no
    description: corresponds to genbank id GCA_000146045.2
    downloader: joselynn wallace
    ensembl_release_number: 87
    accession:
      genbank:
      refseq:
  levels:
    references:
    - component: primary
      complete:
        status: false
      commands:
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa.gz
      - wget ftp://ftp.ensembl.org/pub/release-87/fasta/saccharomyces_cerevisiae/dna/CHECKSUMS
      - md5 *.gz > postdownload-checksums.md5
      - gunzip *.gz
      - md5 *.* > final_checksums.md5
```
**master.yaml keys**    
The first line of the yaml is the `key` for the block of code that follows it (`S_cerevisiae:` in the above example).   
    1. The `key` must be a string.   
    2. The `key` must match the `name` entry under the `metadata` header of the yaml.   

The string of text entered in `key` field will be used to create a folder inside the directory you specify as your output in your config file (cfg.ini or cfg.yaml) or `refchef-cook` arguments. In the previous quickstart example, we used `/Users/jwalla12/references` as the output directory for `refchef-cook` and here is the collapsed file tree that refchef created, note that the folders containing the primary references, indices, and gtf annotations are nested inside a folder named `S_cerevisiae`.

```
./Users/jwalla12/references
└── S_cerevisiae
    ├── bowtie2_index
    ├── bwa_index
    ├── gtf
    └── primary

```
**master.yaml metadata**    
The `metadata` section must contain all of the following fields listed below (although not all of them need to be filled out). Also indicated below: if filling the fields out is required (Yes or No), their expected format, and a brief description of their expected content:

```

  metadata:
    name:                   Required, string, should match `key`
    common_name:            Required, string, common name of organism or 'none' of not applicable. 
    ncbi_taxon_id:          Required, integer, based on NCBI conventions, enter 'none' if not applicable
    organism:               Required, string, suggest using genus, species, and/or strain identifiers
    organization:           Required, string, genome reference database, enter 'none' if a custom assembly
    custom:                 Required, string, should be 'yes'/'no' to indicate if reference was generated/altered in-house
    description:            Required, string, additional pertinent information about reference
    downloader:             Required, string, indicates who downloaded reference
    ensembl_release_number: Not required, integer, leave blank if reference is not from ensembl
    accession:
      genbank:   Not required, string, leave blank if reference is not from genbank
      refseq:    Not required, string, leave blank if reference is not from refseq
```
**master.yaml levels**    
The `levels` section contains following fields below. Also indicated below: if filling the fields out is required (Yes or No), their expected format, and a brief description of their expected content:

```
    references: 

    - component:              Yes, string
                              must be either 'primary', 'indices', or 'annotations'  
      complete:

        status:               Yes, string
                              'true'/'false', refchef will execute commands only if 'false'
      commands:

```






In the above `master.yaml` file, `grch38` is the reference name, which is a required entry in the `master.yaml` file. 

The next chunk (`metadata`) contains the following fields:
`common_name`: Required, can be any commonly used name for your reference.
`ncbi_taxon_id`: Required, see the [NCBI taxonomy browser](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi) for more information. If your organism doesn't have an NCBI taxonomy assignment (for example, it is a metagenome) you can fill in any other string for this entry (for example, `none` rather than `9606`).
`organism`: Required, can be any string including genus, species, or strain level information. 
`organization`: Required, should convey information about which organization was the source of your reference genome (`ensembl`, `refseq`, etc.)


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


### cfg.yaml <a name="cfg.yaml"></a> 

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

### cfg.ini <a name="cfg.ini"></a> 

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

## **Files** <a name="files"></a> 


```

```
