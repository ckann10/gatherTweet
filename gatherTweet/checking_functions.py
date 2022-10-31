#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

This script is for the purpose of validating the data pulled. For now it 
consists of a function to count the number of tweets found.

@author: claudiakann
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'ckann10'
__license__ = 'claudiakann'
__copyright__ = 'Copyright 2022 ckann10'

import os
from re import search
import json

class checking_functions:
    def  __init__(self):
        pass
        
    def number_of_tweets(self, activities, users, base_directory = "", separator = "CityTown", timeline = False):
        count = 0
        if timeline:
            ty = ['Timeline', '']
        else:
            ty = ['']
        for activity in activities:
            sep_value = eval('activity["' + separator + '"]')
            for t in ty:
                for user in users:
                    path = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + '/' + user + t
                    for files in os.listdir(path):
                        if search('twitter', files):
                            with open(path + '/' + files) as f:
                                file_content = f.read()
                            data = json.loads(file_content)
                            count += len(data)
        return count
                            
                                
                            
                        
            
            
        