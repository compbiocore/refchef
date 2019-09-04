**RefChef comes with two commands:**      

[**`refchef-cook`**](./usage.md#refchef-cook):     
Will read recipes and execute the commands that will retrieve the references, indices, or annotations based on the contents of [`master.yaml`](./inputs.md#master.yaml).     

[**`refchef-menu`**](./usage.md#refchef-menu):   
Provides a way for the user to list all references present in the system, based on [`master.yaml`](./inputs.md#master.yaml), as well as filter the list of references based on metadata options.         

![Diagram](assets/refchef-cook_and_refchef-menu.svg)         

**RefChef requires a [`master.yaml`](./inputs.md#master.yaml) file:**      

In addition to the [`refchef-cook`](./usage.md#refchef-cook) and [`refchef-menu`](./usage.md#refchef-menu) commands, RefChef requires a [`master.yaml`](./inputs.md#master.yaml) containing a list of references, indices, annotations, and metadata, as well as the commands necessary to download and process the files.    
When [`refchef-cook`](./usage.md#refchef-cook) is executed, RefChef will append the [`master.yaml`](./inputs.md#master.yaml) to change the `complete` option from `false` to `true`and will also add a `uuid` for each reference, the date the files were downloaded and their location, as well as a complete list of files downloaded.     
Based on the arguments you pass to [`refchef-cook`](./usage.md#refchef-cook), it will either commit those changes to [`master.yaml`](./inputs.md#master.yaml) to a local repository or commit and push the changes to a remote repository. 

**RefChef requires configuration information:**      

[`refchef-cook`](./usage.md#refchef-cook) and [`refchef-menu`](./usage.md#refchef-menu) both require some configuration information, including:

1. Where you'd like the references to be saved 
2. The local git repository for version control of references   
3. The remote github repository for version control of reference
  sequences (optional).   

This information can be specified in a [`cfg.yaml`](./inputs.md#cfg.yaml) file, a [`cfg.ini`](./inputs.md#cfg.ini) file, or it can be passed as arguments to [`refchef-cook`](./usage.md#refchef-cook). 