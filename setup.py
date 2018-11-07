import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="refchef",
    version="0.0.1 - alpha",
    author="Andrew Leith & Fernando Gelin",
    author_email="aleith@brown.edu",
    description="Genome reference manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compbiocore/refchef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "argparse",
        "python-dotenv",
        "PyYAML",
        "PyGithub",
        "yamlloader",
        "pandas",
        "terminaltables",
        "PyGithub"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=["scripts/refchef-cook", "scripts/refchef-menu"]
)
