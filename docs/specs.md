### `master.yaml` <a name="master.yaml"></a>

The [`master.yaml`](./inputs.md#master.yaml) file is the main source of information that RefChef uses to retrieve references, indices, and annotations. It is composed of sequences of code blocks that correspond to each reference. Each code block in [`master.yaml`](./inputs.md#master.yaml) starts with a `key`, followed by `metadata` and `levels`.       

See the [`master.yaml` overview and usage](./inputs.md#master.yaml) for more information.

---

The `key` section consists of:    

`<reference_name>:`     
Expected format: String where <reference_name\> is the name of the reference.

---

The `metadata` section consists of:

>`metadata.name`    
>Expected format: <reference_name\> string, should be the same as the block's `key`

>`metadata.common_name`     
>Expected format: string

>`metadata.ncbi_taxon_id`     
>Expected format: integer, based on [NCBI taxon ID](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi)
 
>`metadata.organism`          
>Expected format: string    

>`metadata.organization`       
>Expected format: string

>`metadata.custom`              
>Expected format: string

>`metadata.description`       
>Expected format: string

>`metadata.downloader`          
>Expected format: string

>`metadata.ensembl_release_number`       
>Expected format: integer

>>`metadata.accession.genbank`       
>>Expected format: string

>>`metadata.accession.refseq`       
>>Expected format: string

---

The `levels` section consists of:

>`levels.<type>`  
>Where <type\>: `references`, `annotations`, or `indices`  
 
>>`levels.<type>.- component`  
>>Expected format: string  

>>>`levels.<type>.complete.status`   
>>>Expected format: boolean (note that if `complete.status` is set to `true` RefChef will skip the current block and not retrieve any file. RefChef automatically changes the status to `true` after retrieving files for the first time.)   

>>`levels.<type>.src`       
  Expected format: UUID string from existing reference, when adding an index file for a reference RefChef will create a symlink to the index files in the reference folder.

>>`levels.<type>.commands`       
  Expected format: Each command should start with `- `, this section is a list of commands to download and process each reference.

After [`refchef-cook`](./usage.md#refchef-cook) is run and references are downloaded, `levels.<type>.complete.status: false` will change to `levels.<type>.complete.status: true` and the following fields will be added to `master.yaml`

>>>`levels.<type>.complete.time`          
>>>Expected format: RefChef will autopopulate this field with the date and time stamp the reference was downloaded if `levels.<type>.complete.status: true`

>>`levels.<type>.location`       
  Expected format: Refchef will autopopulate this field with the directory where downloaded files are stored if `levels.<type>.complete.status: true`
  
>>`levels.<type>.files`       
  Expected format: Refchef will autopopulate this field with a list of files that were downloaded if `levels.<type>.complete.status: true`

>>`levels.<type>.uuid`       
  Expected format: Refchef will autopopulate this field with a UUID for your reference file if `levels.<type>.complete.status: true`       
---

### `cfg.yaml` <a name="cfg.yaml"></a>

If using a `cfg.yaml` file, the `cfg.yaml` file should follow the following specs:

>>`config-yaml.path-settings.reference-directory`
Expected format: String, path to reference storage directory

>>`config-yaml.path-settings.git-directory`
Expected format: String, path to local git repository

>>`config-yaml.path-settings.remote-repository`
Expected format: String, remote git repository, should be in the format of `user/repo`

>>`config-yaml.log-settings.log`
Expected format: String, should be either 'yes' or 'no' in single quotes, indicating whether or not log files will be made

Also see the [`cfg.yaml` overview and example.](./usage.md#cfg.yaml)

---
### `cfg.ini` <a name="cfg.ini"></a>

If using a `cfg.ini` file, the `cfg.ini` file should follow the following specs:     

`[path-settings].reference-directory=`      
Expected format: String, path to reference storage directory

`[path-settings].git-directory=`      
Expected format: String, path to local git repository

`[path-settings].remote-repository=`      
Expected format: String, remote git repository, should be in the format of `user/repo`

`[log-settings].log=`      
Expected format: String, should be either 'yes' or 'no', indicating whether or not log files will be made

`[runtime-settings].break-on-error=`      
Expected format: String, should be either 'yes' or 'no', indicating how RefChef should respond when encountering an error

`[runtime-settings].verbose=`      
Expected format: String, should be either 'yes' or 'no', toggles between verbosity output settings

Also see the [`cfg.ini` overview and example.](./usage.md#cfg.ini)


