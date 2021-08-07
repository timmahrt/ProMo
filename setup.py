#!/usr/bin/env python
# encoding: utf-8
"""
Created on Aug 29, 2014

@author: tmahrt
"""
from setuptools import setup
import io

setup(
    name="promo",
    version="1.3.3",
    author="Tim Mahrt",
    author_email="timmahrt@gmail.com",
    url="https://github.com/timmahrt/ProMo",
    package_dir={"promo": "promo"},
    packages=["promo", "promo.morph_utils"],
    license="LICENSE",
    install_requires=["praatio ~= 4.1"],
    description=(
        "Library for manipulating pitch and duration in an "
        "algorithmic way, for resynthesizing speech"
    ),
    long_description=io.open("README.rst", "r", encoding="utf-8").read(),
    #       install_requires=[], # No requirements! # requires 'from setuptools import setup'
)
