# Specifications for `master.yaml`
---
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

The `master.yaml` file is the main source of information that RefChef uses to retrieve references, indices, and annotations.

### Specifications
---

Each block has a key with the name of the reference, index, or annotation.

`reference_name.metadata`  
Expected format: key - value mapping

`reference_name.metadata.name`  
Expected format: <reference_name> string, should be the same as the block's key

`reference_name.metadata.species`   
Expected format: string

`reference_name.metadata.organization`   
Expected format: string

`reference_name.metadata.downloader`   
Expected format: string

`reference_name.levels`  
Expected format: key - value mapping

`reference_name.levels.<type>`  
Where <type\>: `references`, `annotations`, or `indices`  
Expected format: list of key - value mappings

> `reference_name.levels.<type>.-`  

> `component`  
Expected format: string  
`complete.status`   
Expected formate: boolean (note that if `complete.status` is set to `true` RefChef will skip the current block and not retrieve any file. RefChef automatically changes the status to true after retrieving files for the first time.)   
`src`  
Expected format: UUID v4, or string. If a UUID of an existing reference is entered, RefChef will create a symlink to the index files from the reference folder.
`commands`   
Expected format: list of strings

After RefChef runs and retrieves the files, the following fields will be appended the following fields to `master.yaml`:   

>`reference_name.levels.<type>.-`

> `location`  
Expected format: string  
`files`  
Expected format: list of strings  
`uuid`  
Expected format: UUID v4
