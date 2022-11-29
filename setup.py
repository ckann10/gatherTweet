#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Setup function for gatherTweet package

Copyright (C) 2022 Claudia Kann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'Claudia Kann'
__license__ = 'GPL-3'
__copyright__ = 'Copyright 2022 Claudia Kann'
__contact__ = 'ckann@caltech.edu'


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
