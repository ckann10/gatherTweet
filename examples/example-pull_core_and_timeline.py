#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Example script in order to walk users through the potential use of the 
gatherNet package. A TwitterEvent object is created using the 
event_template.xlsx file. This object is than populated with the Core and 
Core timeline information.


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
    print('Please add the Excel file "event_template.xlsx" to the directory before running the script again')
    raise SystemExit()
    
if(os.path.isfile(dirr + '/event_template.xlsx') == False):
    print('No file "/event_template.xlsx" in directory ' + dirr )
    raise SystemExit()

BLM = tw.TwitterEvent("BLM", base_directory = dirr)
BLM.upload_from_excel(dirr+'/event_template.xlsx')
BLM.pull.get_tweets(BLM,types = ['Core', 'CoreTimeline'])
count = BLM.check.number_of_tweets(BLM.activities, users = ['Core'], base_directory=BLM.base_directory, timeline = True)
print('Collected ' + str(count) + ' Tweets from the Core')

