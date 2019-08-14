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
      - ln -s /Users/jwalla12/references/S_cerevisiae/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa ./Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa 
      - bowtie2-build Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa S_cerevisiae
      - md5 ./*.* > ./final_checksums.md5
```

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
      - ln -s /Users/jwalla12/references/S_cerevisiae/primary/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa ./Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
      - bwa index Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa -p S_cerevisiae
      - md5 ./*.* > ./final_checksums.md5
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
│ S_cerevisiae │ Saccharomyces cerevisiae │ bwa_index     │ corresponds to genbank id GCA_000146045.2 │ dff337a6-9a1d-3313-8ced-dc6f3bfc9689 │
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