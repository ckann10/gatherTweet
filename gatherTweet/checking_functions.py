#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

This script is for the purpose of validating the data pulled. For now it 
consists of a function to count the number of tweets found.

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
from re import search
import json

class checking_functions:
    def  __init__(self):
        pass
        
    def number_of_tweets(self, activities, users, base_directory = "", separator = "CityTown", timeline = False):
        count = 0
        people = 0
        list_tweeters = []
        if timeline:
            ty = ['Timeline', '']
        else:
            ty = ['']
        for activity in activities:
            sep_value = eval('activity["' + separator + '"]')
            for t in ty:
                for user in users:
                    path = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + '/' + user + t
                    if (t == ''):
                        if (user != 'Core'):
                            for files in os.listdir(path):
                                with open(path + '/' + files) as f:
                                    file_content = f.readlines()
                                people += len(set(file_content))
                        else: 
                            for files in os.listdir(path):
                                if search('twitter', files):
                                    with open(path + '/' + files) as f:
                                        file_content = f.read()
                                    data = json.loads(file_content)
                                    list_tweeters = list_tweeters + [x['author_id'] for x in data]
                    else:
                        for files in os.listdir(path):
                            if search('twitter', files):
                                with open(path + '/' + files) as f:
                                    file_content = f.read()
                                data = json.loads(file_content)
                                count += len(data)
        people += len(set(list_tweeters))
        return (people, count)                            
                                
                            
                        
            
            
        