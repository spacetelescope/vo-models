#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    "pydantic-xml"
                ]


setup(
    name='vo-models',
    version='0.1.0',
    description="Open-source data models for IVOA specifications",
    author="Joshua Fraustro",
    author_email='jfraustro@stsci.edu',
    url='https://github.com/jwfraustro/vo-models',
    packages=[
        'vo-models',
    ],
    package_dir={'vo-models':
                 'vo-models'},
    include_package_data=True,
    install_requires=requirements,
    keywords='vo-models',
)
