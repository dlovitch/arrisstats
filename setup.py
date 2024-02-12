#! /usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'beautifulsoup4>=4.5.3',
    'click>=6.7',
    'lxml>=3.7.2',
    'requests>=2.13.0',
    ]

setup(
    name='arrisstats',
    version='1.0.0',
    description='Stats from Arris cable modems',
    author='David L',
    author_email='1191170+dlovitch@users.noreply.github.com',
    url='https://github.com/dlovitch/arrisstats/',
    packages=find_packages(),
    install_requires=requires
    )
