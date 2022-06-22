### Install RefChef

To install from PyPI using **pip**:  
`pip install refchef`

### Set up Git and GitHub
[Git](https://help.github.com/en/articles/set-up-git) is a requirement for using RefChef. As you add references to your system using `refchef-cook`, it will add the metadata and download commands to the `master.yaml` file. Git is used to track those changes to `master.yaml` as new references are added to your system. The path to the local repository (folder) where your `master.yaml` is stored is specified in the `cfg.yaml` or `cfg.ini` file. 

Optionally, `master.yaml` can be pushed to a remote repository on GitHub. If you want to use GitHub to host your repository, create a GitHub account and set up an [access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line). You can add the token to the `.env` file in the repository. You should also create a [`.gitignore` file](https://help.github.com/en/articles/ignoring-files) to control which files are pushed to GitHub. The remote repository where your `master.yaml` is stored is also specified in the `cfg.yaml` or `cfg.ini` file. 

To set up a `.gitignore` and `.env` file, first create a `.gitignore` file as follows:

```bash
touch .gitignore
```

Then add `.env` to the `.gitignore` by pasting the following into the `.gitignore` file.

```bash
# ignore env files
*.env
```

Now create a `.env` file.
```bash
touch .env
```

Paste the contents of the `.env.template` file in the `RefChef` home directory into the `.env` file, which will now look like this:

```bash
GITHUB_TOKEN=
```

Then, paste the GitHub access token into the `GITHUB_TOKEN=` line into your `.env` file, which might now look like this:

```bash
GITHUB_TOKEN=5c25370fcf7db4a676d98d72700e2922654485ed
```

### Development
To install a **development version** from the current directory:  
```bash
git clone https://github.com/compbiocore/refchef.git
cd refchef
pip install -e .
```

Run unit tests as:
`python setup.py test`

## Contributing

Contributions consistent with the style and quality of existing code are
welcome. Be sure to follow the guidelines below.

Check the issues page of this repository for available work.

### Committing

This project uses [commitizen](https://pypi.org/project/commitizen/)
to ensure that commit messages remain well-formatted and consistent
across different contributors.

Before committing for the first time, install commitizen and read
[Conventional
Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/).

```bash
pip install commitizen
```

To start work on a new change, pull the latest `develop` and create a
new *topic branch* (e.g. `feature-resume-model`,
`chore-test-update`, `bugfix-bad-bug`).

Add your changes to the current branch.
```bash
git add .
```

To commit your changes, run the following command (instead of `git commit`) and
follow the directions:

```bash
cz commit
```

#### Contact

email: cbc-help@brown.edu
