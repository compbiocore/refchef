
###**Requesting new RefChef references on Oscar**

**Best Practices**

Refchef is designed to be very flexible to allow for tracking many types of reference datasets. It will run any commands and there's few explicit rules about what information to supply in the yaml. However, we have a set of best practices for users who would like to add new references for tracking on Oscar. 

1. Check what is available on RefChef (https://compbiocore.github.io/refchef-ember/#/references) to make sure the resource you need hasn't been added.
2. Keep reproducibility in mind when providing commands to download data. For example, when downloading data from Ensembl, use a URL that specifies the release number (e.g., ftp://ftp.ensembl.org/pub/release-91/) rather than using a `latest` or `current` URL (http://ftp.ensembl.org/pub/current_fasta/), which will change as new versions of genomes are released.
3. Fill out all fields in the YAML form that apply. Be as detailed and specific as you can be. This will help make RefChef a better resource for all. If there are metadata fields that you feel are relevant that aren't included, please make a GitHub issue (https://github.com/compbiocore/refchef).

**Request Form**

The request form is to request new references to be added to Oscar. The references will go to `/gpfs/data/shared/databases/cbc-references-refchef`. The form is divided into several sections. 

###**RefChef Request - new references**

- The first two fields ask for your name and email so we can contact you if there's any issues with your request. 

**Metadata**     
    - `name` The short name for you reference. This will be the name of the folder where your resources will be stored. Avoid any spaces in this field (use `_` instead).
    - `organism` Genome and species of the organism for the reference. If this doesn't apply -- for example, if the reference is a mix of different organisms -- you can fill in this field with `none` or `na`.
    - `common` Common name for the reference. For example, the common name for `Homo sapiens` would be `human`. Again, if this doesn't apply you can fill in this field with `none` or `na`.
    - `taxon` If this is a genomics reference, this is the NCBI taxon ID. For example, `Homo sapiens` taxon id is 9606  (https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=9606&lvl=3&lin=f&keep=1&srchmode=1&unlock). If this doesn't apply, fill in this field with `none` or `na`.
    - `organization` The hosting organization where reference are being obtained from (for example, you may want data from `Modified National Institute of Standards and Technology` or `Ensembl`). 
    - `description` Short description of your reference, you can use this field to include any other pertinent information about your reference that isn't captured in any of the other fields.
    - `genbank` Genbank accession (if applicable). If it does not apply, you can fill in this field with `none` or `na`.
    - `refseq` Refseq accession (if applicable). If it does not apply, you can fill in this field with `none` or `na`.
    - `ensembl` Ensembl release number (if applicable). If it does not apply, you can fill in this field with `none` or `na`.
    - `custom` This field should be filled with either `true` or `false` based on whether or not this is a custom reference (for example, if you are using RefChef to keep track of and share reference genomes that you have assembled yourself, it is a custom reference).
    - `category` Fill in with `genomics` (if the reference is a nucleic acid or protein sequence reference). We also allow for this to be filled with `other` to allow for RefChef to track non-genomics references.  

**Levels**     
  - `level` This field is multiple choice and describes the reference you are adding. Current options are: 'references' which are a primary resource (e.g. a genome fasta), 'indices' (e.g. a BWA index), 'annotations' (e.g. a .gtf file), or 'other' (none of the above). Note that if you are selecting `index`, it will be an index of some other specific reference tracked via RefChef. 
  - If you selected:
    - `other`, the next question will be a fill-in short answer question to clearly describe the `other` component you are adding (e.g., `testing_images` or `training_images`).
    - I
