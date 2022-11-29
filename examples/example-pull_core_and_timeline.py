#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

Example script in order to walk users through the potential use of the 
gatherNet package. A TwitterEvent object is created using the 
event_template.xlsx file. This object is than populated with the Core and 
Core timeline information.

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

