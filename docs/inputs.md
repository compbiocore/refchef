---

###**master.yaml** <a name="master.yaml"></a>    

**overview**      
Refchef uses YAML files that are composed of nested entry and value pairs -- for example, the entry and value pair `common_name`: `yeast`. The spacing and indentation of the entries and values are meaningful - Refchef uses the convention of using 2 spaces to indent each subsequent level of the entries and values in the YAML and a `:` and space are between each entry and value. Some entries in the yaml will have a preceeding `-` and a space before them (such as `- component:` and the commands under the `commands` header), which are required for Refchef to properly process the YAML.    

See the [`master.yaml` file specifications](./specs.md#master.yaml) for more information.

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

The string of text entered in the `key` field (`S_cerevisiae` in the above example) will be used to create a folder inside the directory you specify as your output in your config file (`cfg.ini` or `cfg.yaml`) or `refchef-cook` arguments. In the previous quickstart example, we used `/Users/jwalla12/references` as the output directory for `refchef-cook`. Here is the collapsed file tree that refchef created, note that the folder containing the primary reference is nested inside a folder named `S_cerevisiae` based on the `key`.

```bash
./Users/jwalla12/references #this directory is specified in refchef-cook or the config files
└── S_cerevisiae
    ├── bowtie2_index
    ├── bwa_index
    ├── gtf
    └── primary

```

**master.yaml metadata**      
The `metadata` section of `master.yaml` contains information about the references, including the organism name, taxon_id, etc.

!!! Caution 
    When running a new YAML file to add additional information to a primary reference, metadata entries present in the initial [`master.yaml`](#master.yaml) file can be omitted (for example, `ncbi_taxon_id:`, `common_name:`). When adding indices or annotations to a primary reference already in [`master.yaml`](#master.yaml), the metadata in [`master.yaml`](#master.yaml) will be overwritten by the metadata in the new.yaml file. This could be helpful in situations where you want to update the metadata fields.

**master.yaml levels**    
The `levels` section contains higher level information about the references, including when they were downloaded and the exact commands used to download and process the references.  

!!! Caution 
    The entry `status` must be set to `false` for Refchef to exeecute the commands in the code block. If it is set to `true`, the code will not execute (even if the -e flag is set). After a code block is executed, the `false` flag will flip to `true` automatically and the `time:` entry will appear under the `status` header. The `time:` header will be populated with the datetime stamp the reference was downloaded. 

**master.yaml commands**    
This portion of the `master.yaml` should be populated with the specific commands you want to execute to download and process your reference. Each command should be prepended with a `-` and a space. 

!!! Caution 
    Each time files are processed using a set of commands in the YAML, the last command must run `md5` on all of the files and direct the output to a file called `final_checksums.md5`.

---

### **cfg.yaml** <a name="cfg.yaml"></a> 
**overview**     
Refchef requires configuration information, which can be passed as arguments or specified in a configuration file. A `cfg.yaml` is one option for configuration and should contain the following fields. Also indicated below: If filling out the field is required, their expected format, and a brief description of their contents.    


See the [`cfg.yaml` file specifications](./specs.md#cfg.yaml) for more information.

**example:**
```yaml
config-yaml:
  path-settings:
    reference-directory: /Users/jwalla12/references
    git-directory: /Users/jwalla12/remote_references
    remote-repository: jrwallace/remote_references
  log-settings:
    log: 'yes'
```


---

### **cfg.ini** <a name="cfg.ini"></a> 
**overview**     
Refchef requires configuration information, which can be passed as arguments or specified in a configuration file. A `cfg.ini` is one option for configuration and should contain the following fields. Also indicated below: If filling out the field is required, their expected format, and a brief description of their contents. 

See the [`cfg.ini` file specifications](./specs.md#cfg.ini) for more information.

**example:**

```toml
[path-settings]
reference-directory=/Users/jwalla12/references
git-directory=/Users/jwalla12/remote_references
remote-repository=jrwallace/remote_references
[log-settings]
log=yes
[runtime-settings]
break-on-error=yes
verbose=yes
```


