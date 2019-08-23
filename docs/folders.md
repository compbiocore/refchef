
RefChef creates folders to store your references. The names of these folders is based on:    

1. The [`master.yaml`](./specs.md#master.yaml) key (which should match the 'name' entry under 'metadata' in `master.yaml`).   

2. The 'component' entry under 'levels' in [`master.yaml`](./specs.md#master.yaml).   

 Here is the collapsed file tree that refchef created from the Tutorial part of the documentation and what the directory names are based on:  

```bash
./Users/jwalla12/references #this directory is specified in refchef-cook or the config files
└── S_cerevisiae            #this is named after the 'key' and the 'name' entry under 'metadata' in master.yaml
    ├── bowtie2_index       #this folder is created in the master.yaml `commands` section.
    ├── bwa_index           #this folder is created in the master.yaml `commands` section.
    ├── gtf                 #this folder is created in the master.yaml `commands` section.
    └── primary             #this is named after the 'component' entry under 'levels' in master.yaml
```

Here is the expanded file tree: 

```bash
./Users/jwalla12/references 
└── S_cerevisiae      
    ├── bowtie2_index 
    │   └── metadata.txt
    ├── bwa_index     
    │   └── metadata.txt
    ├── gtf          
    │   ├── CHECKSUMS
    │   ├── Saccharomyces_cerevisiae.R64-1-1.87.gtf
    │   ├── final_checksums.md5
    │   ├── metadata.txt
    │   └── postdownload-checksums.md5
    └── primary      
        ├── CHECKSUMS
        ├── Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
        ├── bowtie2_index -> /Users/jwalla12/references/S_cerevisiae/bowtie2_index
        ├── bwa_index -> /Users/jwalla12/references/S_cerevisiae/bwa_index
        ├── final_checksums.md5
        ├── metadata.txt
        └── postdownload-checksums.md5
```
This indicates that refchef has created symlinked directories for bowtie2 and bwa indices  in `/Users/jwalla12/references/S_cerevisiae/primary`. This process (linking reference and index) is triggered by:
1. The addition of the `src:` line in bowtie2.yaml and bwa.yaml
2. Specifying the master.yaml `levels` are `indices:` in the master.yaml

If we look at the output from [`refchef-menu`](./usage.md#refchef-menu), we see the UUID for the primary reference file, which is `dff337a6-9a1d-3313-8ced-dc6f3bfc9689`.

```bash
┌ 🐶 RefChef Menu ────────────────────────┬───────────┬───────────────────────────────────────────┬──────────────────────────────────────┐
│ name         │ organism                 │ component │ description                               │ uuid                                 │
├──────────────┼──────────────────────────┼───────────┼───────────────────────────────────────────┼──────────────────────────────────────┤
│ S_cerevisiae │ Saccharomyces cerevisiae │ primary   │ corresponds to ganbank id GCA_000146045.2 │ dff337a6-9a1d-3313-8ced-dc6f3bfc9689 │
└──────────────┴──────────────────────────┴───────────┴───────────────────────────────────────────┴──────────────────────────────────────┘
```
In this clipping from bowtie2.yaml, note that the UUID was indicated in the `src:` entry under `component`, `indices`, and `levels`.

```yaml
S_cerevisiae:
  levels:
    indices:
    - component: bowtie2_index
      complete:
        status: false
      src: dff337a6-9a1d-3313-8ced-dc6f3bfc9689 
```

This indicates which primary reference was used to create the index file.