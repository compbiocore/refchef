# Brown CBC's RefChef Usage Guide

At present, this documentation exists to describe the software in its current state to aid in the development process.  It will therefore usually lag one version behind the software itself, so some of the information presented herein may be incorrect/outdated.

For a more hands-on introduction to this software via walkthrough with code and sample files, please see the 'Sample Workflow / Walkthrough' page linked in the sidebar and on the homepage.

### Master YAML / New YAML Scheme Overview

In the broadest possible sense, this tool can accommodate either one or two YAMLs.  It must always be given a 'Master YAML' - that is to say, a comprehensive list of references and their associated commands and metadata.  The Master YAML (hereafter simply 'the Master') is, essentially, a manifest of all references on the entire system (meant to be continually updated when further references are added).  The tool can also be given a 'New YAML' alongside the Master containing additional references.  Both of these files have the same formatting, but a New YAML corresponds to references that are being newly added to a system where some references are already present as tabulated in the Master.  Providing both the Master and a New YAML causes the New YAML's reference section to be appended to Master, ensuring the manifest remains comprehensive.

### YAML Structure

Please see the following screenshot for an example YAML file, then refer to the description below the image for an explanation of its properties.

<p>example.yaml</p>
<img src="../assets/master_yaml_screenshot.png">

There are several important features of this file structure that should be noted.

#### Top-Level Subheadings

The reference subheadings constitute the vast majority of the YAML.  These subheading fully describe all of the references documented within the YAML, along with the commands used in their acquisition.  We will describe the contents of one such subheading's structure from the image - the most complicated one, 'ucsc-hg19-concatenate'.

**Per-Reference Subheadings**

Within 'ucsc-hg19-concatenate', there are several subheadings.  One of these, 'metadata', is required for all references.  The others, which can have any name and be as numerous as is needed, each describe one type of feature for a specified reference.  If that appears confusing at first glance, please continue reading.

The 'metadata' subheading includes important pieces of metadata that the user must record for a given reference.  'reference-name' is a field that is used to name the directory created by the software for that reference's files (which can be the same as, or different than, the respective yaml key), while the rest are merely recorded for the sake of completeness.  At this time, three such pieces of metadata are supported: 'species', denoting the organism's species; 'organization', indicating which organization created the reference (e.g. UCSC); and 'downloader', indicating which user ran the software on this reference.  In addition to being tabulated in the YAML, this metadata is written to a file and included in the reference's root directory with the component subfolders.

The other subheadings each refer to a component of the reference in question.  They include two subheadings of their own: 'retrieve', which tells the program whether or not to run the associated commands, and 'command-sequence', which lists out all of the commands involved in the download and processing of the reference component.  In the depicted example, 'ucsc-hg19-concatenate', the UCSC version of hg19 with all of its separate chromosome files concatenated, has two components: the main genome fasta ('primary-reference') and a list of ESTs assocated with that version of the genome ('est').  These component subheadings can have any name and will be placed in a subdirectory bearing that designation, as seen below:

<p>example.yaml</p>
<img src="../assets/hg19_parent_directory.png">