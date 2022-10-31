#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Example script in order to walk users through the potential use of the 
gatherNet package. 


First a TwitterEvent object is created using existing pulled data, this found
data is then compressed so as to be functionally used.

@author: claudiakann
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'ckann10'
__license__ = 'claudiakann'
__copyright__ = 'Copyright 2022 ckann10'

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




