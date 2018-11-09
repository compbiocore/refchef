import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="refchef",
    version="0.0.1",
    author="Andrew Leith & Fernando Gelin",
    author_email="aleith@brown.edu",
    description="Genome reference manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compbiocore/refchef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2 :: 3",
        "License :: OSI Approved :: GLP 3.0",
        "Operating System :: Mac OS :: Linux",
    ],
    install_requires=[
        "argparse",
        "python-dotenv",
        "PyYAML",
        "PyGithub",
        "yamlloader",
        "pandas",
        "terminaltables",
        "mock",
        "future"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=["scripts/refchef-cook", "scripts/refchef-menu"]
)
