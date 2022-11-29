#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Example script in order to walk users through the potential use of the 
gatherNet package. 


First a TwitterEvent object is created using existing pulled data, this found
data is then compressed so as to be functionally used.

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


import os
import gatherTweet as tw

dirr = os.path.expanduser('~') +"/gatherTweet_example"
if (os.path.isdir(dirr) == False):
    os.mkdir(os.path.expanduser('~') +"/gatherTweet_example")
    print('Made the directory:')
    print(os.path.expanduser('~') +"/gatherTweet_example")
    print("""This directory is empty, please run example-pull_core_and_timeline.py 
          in order to populate the directory, then you may try again.""")
    quit()


BLM = tw.TwitterEvent("BLM", base_directory = dirr)

BLM.upload_from_file_structure()
BLM.read.read_tweets(BLM, users = "Core")
BLM.read.wrap_csv(BLM, users = "Core")
BLM.read.read_tweets_basic(BLM, users = "CoreTimeline")
BLM.read.wrap_csv_basic(BLM, users = "CoreTimeline")


