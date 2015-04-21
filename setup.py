# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ProjectX",
    version = "0.1.0",
    author = "Rokas Aleksiūnas",
    author_email = "rokas.aleksiunas@gmail.com",
    description = ("The most elegant set of equipment for python microservices"),
    license = "GPLv3",
    keywords = "elegant microservice flow",
    url = "https://github.com/Zogg/Tiltai",
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv3 License",
    ],
)

