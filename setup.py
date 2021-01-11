from setuptools import find_packages, setup

import versioneer

with open("./README.rst") as f:
    long_description = f.read()

requirements = [
    # package requirements go here
    "pandas==1.2.0",
    "scipy==1.6.0",
    "networkx==2.5",
    "geopandas==0.6.1",
    "shapely==1.6.4",
    "matplotlib==3.3.3",
]

setup(
    name="gerrychain",
    description="Use Markov chain Monte Carlo to analyze districting plans and gerrymanders",
    author="Metric Geometry and Gerrymandering Group",
    author_email="gerrymandr@gmail.com",
    maintainer="Max Hully",
    maintainer_email="max@mggg.org",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mggg/GerryChain",
    packages=find_packages(exclude=("tests",)),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=requirements,
    keywords="GerryChain",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)
