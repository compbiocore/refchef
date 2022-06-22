**RefChef comes with three commands:**      

[**`refchef-cook`**](./usage.md#refchef-cook):     
Will read recipes (yaml files) and execute the commands that will retrieve or create the references or their indices, annotations, or other associated files and add the metadata and commands to [`master.yaml`](./inputs.md#master.yaml).     

[**`refchef-menu`**](./usage.md#refchef-menu):   
Prints all references documented in [`master.yaml`](./inputs.md#master.yaml) as a table on the command line.

[**`refchef-serve`**](./serve.md):   
Lists all references documented in [`master.yaml`](./inputs.md#master.yaml) as a minimal web interface.

![Diagram](assets/refchef-cook_and_refchef-menu.svg)         

**RefChef requires a [`master.yaml`](./inputs.md#master.yaml) file:**      

The `master.yaml` file contains a list of references and associated files (indices, annotations, other associated files), their metadata, and the commands necessary to download and/or process the references and associated files.

When [`refchef-cook`](./usage.md#refchef-cook) is executed, RefChef will append the [`master.yaml`](./inputs.md#master.yaml) to change the `complete` flag from `false` to `true`and will also add a `uuid` for each reference. It also adds the date the files were downloaded and their location, as well as a complete list of files downloaded.     
Based on the arguments you pass to [`refchef-cook`](./usage.md#refchef-cook), it will either commit those changes to [`master.yaml`](./inputs.md#master.yaml) to a local repository or commit and push the changes to a remote repository. 

**RefChef requires configuration information:**      

[`refchef-cook`](./usage.md#refchef-cook) and [`refchef-menu`](./usage.md#refchef-menu) both require some configuration information, including:

1. Where you'd like the references to be saved 
2. The local git repository for version control of references   
3. The remote github repository for version control of reference
  sequences (optional).   

This information can be specified in a [`cfg.yaml`](./inputs.md#cfg.yaml) file, a [`cfg.ini`](./inputs.md#cfg.ini) file, or it can be passed as arguments to [`refchef-cook`](./usage.md#refchef-cook). 