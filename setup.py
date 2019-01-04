import setuptools
import re

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('refchef/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

setuptools.setup(
    name="refchef",
<<<<<<< HEAD
    version="0.0.6",
=======
    version=version,
>>>>>>> master
    author="Andrew Leith & Fernando Gelin",
    author_email="cbc-help@brown.edu",
    description="Genome reference manager.",
    long_description=long_description,
    url="https://github.com/compbiocore/refchef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS",
        "Operating System :: Unix"
    ],
<<<<<<< HEAD
    # install_requires=[
    #     "argparse",
    #     "python-dotenv",
    #     "pyyaml",
    #     "pygithub",
    #     "yamlloader",
    #     "pandas",
    #     "terminaltables",
    #     "mock",
    #     "future",
    #     "pytest>=3",
    #     "coverage>=4.4",
    #     "pytest-cov>=2.0"
    #     ],
    # setup_requires=["pytest-runner"],
    # tests_require=["pytest"],
=======
    install_requires=[
        "argparse",
        "python-dotenv",
        "oyaml",
        "pygithub",
        "yamlloader",
        "pandas",
        "terminaltables",
        "mock",
        "future",
        "configparser",
        "pytest>=3",
        "coverage>=4.4",
        "pytest-cov>=2.0"
        ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
>>>>>>> master
    scripts=["scripts/refchef-cook", "scripts/refchef-menu"]
)
