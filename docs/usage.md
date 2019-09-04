---

###**refchef-cook** <a name="refchef-cook"></a> 

`refchef-cook` reads [`master.yaml`](./inputs.md#master.yaml) and executes the commands that will retrieve and/or process the references, indices, or annotations.

**usage:**
```bash
refchef-cook [*arguments*]
```
**arguments:**
```bash
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

---

###**refchef-menu** <a name="refchef-menu"></a> 

Refchef-menu provides a way for the user to list all references present in the system, based on [`master.yaml`](./inputs.md#master.yaml), as well as filter the list of references based on metadata options. You must specify either `--master, -m` or `--config, -c`. 

**usage:**
```bash   
refchef-menu [*arguments*]
```
**arguments:**
```bash         
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
```bash
┌ 🐶 RefChef Menu ────────────────────────┬───────────┬───────────────────────────────────────────┬──────────────────────────────────────┐
│ name         │ organism                 │ component │ description                               │ uuid                                 │
├──────────────┼──────────────────────────┼───────────┼───────────────────────────────────────────┼──────────────────────────────────────┤
│ S_cerevisiae │ Saccharomyces cerevisiae │ primary   │ corresponds to ganbank id GCA_000146045.2 │ dff337a6-9a1d-3313-8ced-dc6f3bfc9689 │
└──────────────┴──────────────────────────┴───────────┴───────────────────────────────────────────┴──────────────────────────────────────┘
```

