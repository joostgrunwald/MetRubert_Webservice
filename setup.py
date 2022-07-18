#! /usr/bin/env python
# -*- coding: utf8 -*-


import os
import io
from setuptools import setup


def getreadme():
    for fname in ('README.rst','README.md', 'README'):
        if os.path.exists(fname):
            return io.open(os.path.join(os.path.dirname(__file__), fname),'r',encoding='utf-8').read()
    return ""

setup(
    name = "metaphorclam",
    version = "0.4", #make sure SYSTEM_VERSION in your service configuration is set to the same value!
    author = "Joost Grunwald", #adapt this
    description = ("MetRubert is a dutch metaphor predictor. You can upload either tokenised or untokenised files (which will be automatically tokenised for you using ucto), the output will consist of a zip file containing XML files, one for each sentence in the input document."),
    license = "GPL-3.0-only",
    keywords = [ "nlp", "linguistics", "MetRubert", "dependency parsing", "syntax"],
    url = "https://github.com/joostgrunwald/MetRubert_webservice",
    packages=['metaphorclam'],
    long_description=getreadme(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {'metaphorclam':['*.wsgi','*.yml','*.sh'] },
    include_package_data=True,
    install_requires=['CLAM >= 3.0', 'natsort'] #Alpino is also required but is an external dependency that setuptools can't handle, we specify it in codemeta-harvest.json for metadata harvesting purposes
)
