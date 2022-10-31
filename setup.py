#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Setupfunction for gatherTweet package

@author: claudiakann
"""

__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'ckann10'
__license__ = 'claudiakann'
__copyright__ = 'Copyright 2022 ckann10'

from setuptools import setup, find_packages
from gatherTweet import __version__

setup(
      name = 'gatherTweet',
      url = 'https://github.com/ckann10/gatherTweet',
      author = 'Claudia Kann',
      author_email = 'ckann@caltech.edu',
      packages = find_packages(),
      install_requires = ['pandas', 'TwitterAPI',
                          'datetime', 'requests', 'uuid',
                          'pytz'],
      version = __version__,
      license = 'MIT',
      description = 'Python package to dynamically track events using social media data')
