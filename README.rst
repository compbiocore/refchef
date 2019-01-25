RefChef
~~~~~~~

|Travis| |Coverage| |Docs| |License| |PyPi|

RefChef is a reference management tool used to (1) document the exact
steps undertaken in the retrieval of genomic references, (2) maintain
the associated metadata, (3) provide a mechanism for automatically
reproducing retrieval and creation of an exact copy of genomic
references.

Installation
~~~~~~~~~~~~

| To install from PyPI using **pip**:
| ``pip install refchef``

| To install using **Anaconda Python**:
| ``conda install -c compbiocore refchef``

Development
~~~~~~~~~~~

To install a **development version** from the current directory:

.. code:: bash

    git clone https://github.com/compbiocore/refchef.git
    cd refchef
    pip install -e .

Run unit tests as: ``python setup.py test``

Set up ``.env`` file with GitHub Access Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sensitive environment variables are stored in the .env file. This file
is included in .gitignore intentionally, so that it is never committed.
- Create a ``.env`` file and copy into it the contents of
``.env.template`` - Get your `GitHub Access
Token <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/>`__
and add to the ``.env`` file.

Contributing
~~~~~~~~~~~~

Contributions consistent with the style and quality of existing code are
welcome. Be sure to follow the guidelines below.

Check the issues page of this repository for available work.

Committing
^^^^^^^^^^

This project uses `commitizen <https://pypi.org/project/commitizen/>`__
to ensure that commit messages remain well-formatted and consistent
across different contributors.

Before committing for the first time, install commitizen and read
`Conventional
Commits <https://www.conventionalcommits.org/en/v1.0.0-beta.2/>`__.

::

    pip install commitizen

To start work on a new change, pull the latest ``develop`` and create a
new *topic branch* (e.g. ``feature-resume-model``,
``chore-test-update``, ``bugfix-bad-bug``).

::

    git add .

To commit, run the following command (instead of ``git commit``) and
follow the directions:

::

    cz commit

Contact
^^^^^^^

Contact cbc-help@brown.edu - this is our general help line, so please
specify that your issue is with this site's contents

.. |Travis| image:: https://img.shields.io/travis/compbiocore/refchef/master.svg?style=flat-square
   :target: https://travis-ci.org/compbiocore/refchef
.. |Coverage| image:: https://img.shields.io/coveralls/github/compbiocore/refchef/master.svg?style=flat-square
   :target: https://coveralls.io/github/compbiocore/refchef
.. |Docs| image:: https://img.shields.io/badge/docs-stable-blue.svg?style=flat-square
   :target: https://compbiocore.github.io/refchef
.. |License| image:: https://img.shields.io/badge/license-GPL_3.0-orange.svg?style=flat-square
   :target: https://raw.githubusercontent.com/compbiocore/cbc-documentation-templates/master/LICENSE.md
.. |PyPi| image:: https://img.shields.io/pypi/v/refchef.svg?style=flat-square
   :target: https://pypi.org/project/refchef/
