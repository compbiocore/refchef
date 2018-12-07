import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="refchef",
    version="0.0.6",
    author="Andrew Leith & Fernando Gelin",
    author_email="aleith@brown.edu",
    description="Genome reference manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compbiocore/refchef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS",
        "Operating System :: Unix"
    ],
    install_requires=[
        "argparse",
        "python-dotenv",
        "pyyaml",
        "pygithub",
        "yamlloader",
        "pandas",
        "terminaltables",
        "mock",
        "future",
        "pytest>=3",
        "coverage>=4.4",
        "pytest-cov>=2.0"
        ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=["scripts/refchef-cook", "scripts/refchef-menu"]
)
