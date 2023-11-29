#!/usr/bin/env python
"""Setup package for vo-models"""

from setuptools import find_packages, setup

requirements = [
    "pydantic-xml[lxml]",
    "pylint>=2.7.2",
]


setup(
    name="vo.models",
    version="0.1.0",
    description="Open-source data models for IVOA specifications",
    author="Joshua Fraustro",
    author_email='jfraustro@stsci.edu',
    url='https://github.com/jwfraustro/vo-models',
    packages=["vo." + pkg for pkg in find_packages("vo")],
    package_dir={"vo-models": "vo"},
    include_package_data=True,
    install_requires=requirements,
    keywords='vo-models',
)
