#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

This script serves as the home to functions which wrap the tweets into a 
usable format. Key functions include read_tweets, read_tweets_basic, 
wrap_csv, and wrap_csv_basic

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
import pandas as pd


class read:
    def __init__(self):
        pass

    def read_tweets(self, event, users = 'Core'):
        self.base_directory = event.base_directory
        if not isinstance(users, list):
            users = [users]
        for use in users:
            count = 0
            categories = []
            for activity in event.activities:
                tweets = pd.DataFrame() 
                num = 0
                sep_value = eval('activity["' + event.separator + '"]')
                print(activity['ID'])
                if not os.path.exists(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/' ):
                    os.mkdir(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/' )     
                path = self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/' + use
                file_count = 0
                for files in os.listdir(path):
                    num += 1
                    print(str(num) + ' of ' + str(len(os.listdir(path))))
                    if num >= 61:
                        num = 1
                        print('printing ' + str(file_count))
                        tweets.to_csv(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/'  + use + '_' + str(file_count)  +'.csv')
                        tweets = pd.DataFrame() 
                        file_count += 1
                        
                    if search('twitter', files):
                        with open(path + '/' + files) as f:
                            file_content = f.read()
                        data = json.loads(file_content)
                        for tweet in data:
                            count += 1
                            dicts_exist = True
                            if count <= 1000:
                                if isinstance(tweet, dict):
                                    options_new = [[x] for x in tweet.keys()]# if x != "entities"]
                                    while dicts_exist:
                                        options = options_new
                                        options_new = []
                                        dicts_exist = False
                                        for opt in options:
                                            if isinstance(eval('tweet["' + '"]["'.join(opt) + '"]'), dict):
                                                expand = [opt + [x] for x in eval('tweet["' + '"]["'.join(opt) + '"]').keys()]
                                                options_new += expand
                                                dicts_exist = True
                                            else:
                                                options_new += [opt]
                                                             
                                categories_new = ['_-'.join(x) for x in options]
                                categories = list(set(categories_new) | set(categories))
                                
                                'unions of categories and categories new, set others to 0 if doesnt exist, ifnew category ad NA'
        
                                tweet_as_string = ",".join(['"' + '_-'.join(x) + '": tweet["' + '"]["'.join(x) + '"]' for x in options_new] +
                                                    ['"' + x + '": "NaN"' for x in list(set(categories) - set(categories_new))])  
                                                           
                                tweets = tweets.append(eval('{' + tweet_as_string + ', "activity": activity["ID"]}'), ignore_index=True)
                            else:
                                tweet_as_dict = {}
                                for opt in categories:
                                    try:
                                        tweet_as_dict.update(eval('{"' + opt + '" : tweet["' + '"]["'.join(opt.split("_-")) + '"]}'))
                                    except: 
                                        tweet_as_dict.update(eval('{"' + opt + '" : "NaN"}'))
                               
                                tweets = tweets.append(tweet_as_dict, ignore_index=True)
                                
                print('printing csv')                    
                tweets.to_csv(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/'  + use + '_' + str(file_count)  + '.csv')
                
    def read_tweets_basic(self, event, users = 'Core'):
        self.base_directory = event.base_directory
        if not isinstance(users, list):
            users = [users]
        for use in users:
            count = 0
            for activity in event.activities:
                tweets = pd.DataFrame() 
                num = 0
                sep_value = eval('activity["' + event.separator + '"]')
                print(activity['ID'])
                if not os.path.exists(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/' ):
                    os.mkdir(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/' )     
                path = self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/' + use
                file_count = 0
                for files in os.listdir(path):
                    num += 1
                    print(str(num) + ' of ' + str(len(os.listdir(path))))
                    if num >= 61:
                        num = 1
                        print('printing ' + str(file_count))
                        tweets.to_csv(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/Basic'  + use + '_' + str(file_count)  +'.csv')
                        tweets = pd.DataFrame() 
                        file_count += 1
                        
                    if search('twitter', files):
                        with open(path + '/' + files) as f:
                            file_content = f.read()
                        data = json.loads(file_content)
                        for tweet in data:
                            count += 1
                            tweets = tweets.append({"text": tweet['text'], "author_id": tweet['author_id'], "id": tweet['id'], "created_at": tweet['created_at'],  "activity": activity["ID"]}, ignore_index=True)
                                
                print('printing csv')                    
                tweets.to_csv(self.base_directory + '/' + sep_value + '/'  + sep_value + "_" + activity['Date'].replace(" ", "-") + '/analysis/Basic'  + use + '_' + str(file_count)  + '.csv')                
            
    def wrap_csv(self, event, users = 'Core', full = False, part = True):
        self.base_directory = event.base_directory
        if not isinstance(users, list):
            users = [users]
        for use in users:
            if part:
                for val in os.listdir(self.base_directory):
                    print(val)
                    count = 0
                    if ('analysis' not in val) & ('.DS_Store' not in val) & (os.path.isdir(self.base_directory + '/' + val ) == True):
                        tweets = pd.DataFrame()
                        if not os.path.exists(self.base_directory + '/' + val + '/analysis/' ):
                            os.mkdir(self.base_directory + '/' + val + '/analysis/' )
                        for activity in os.listdir(self.base_directory + '/' + val):
                            count += 1
                            print(count)
                            if ('analysis' not in activity) & ('.DS_Store' not in activity) & (os.path.isdir(self.base_directory + '/' + val + '/' + activity) == True):
                                path = self.base_directory + '/' + val + '/' + activity + '/analysis'
                                for files in os.listdir(path):
                                    if use + '_' in files:
                                        tweets = tweets.append(pd.read_csv(path + '/' + files))
                        
                        tweets.to_csv(self.base_directory + '/' + val + '/analysis/' + use + '.csv')
            if full:
                tweets = pd.DataFrame()
                for val in os.listdir(self.base_directory):
                    if ('analysis' not in val) & ('.DS_Store' not in val) & (os.path.isdir(self.base_directory + '/' + val ) == True):
                        tweets = tweets.append(pd.read_csv(self.base_directory + '/' + val + '/analysis/' + use + '.csv'))
                if not os.path.exists(self.base_directory + 'analysis/' ):
                    os.mkdir(self.base_directory + 'analysis/' )     
                tweets.to_csv(self.base_directory + 'analysis/' + use + '.csv')                           
                            
             
    def wrap_csv_basic(self, event, users = 'Core', full = False, part = True):
        self.base_directory = event.base_directory
        if not isinstance(users, list):
            users = [users]
        for use in users:
            if part:
                for val in os.listdir(self.base_directory):
                    print(val)
                    count = 0
                    if ('analysis' not in val) & ('.DS_Store' not in val) & (os.path.isdir(self.base_directory + '/' + val ) == True):
                        tweets = pd.DataFrame()
                        if not os.path.exists(self.base_directory + '/' + val + '/analysis/' ):
                            os.mkdir(self.base_directory + '/' + val + '/analysis/' )
                        for activity in os.listdir(self.base_directory + '/' + val):
                            count += 1
                            print(count)
                            if ('analysis' not in activity) & ('.DS_Store' not in activity) & (os.path.isdir(self.base_directory + '/' + val +'/' + activity) == True):
                                path = self.base_directory + '/' + val + '/' + activity + '/analysis'
                                for files in os.listdir(path):
                                    if 'Basic' + use + '_' in files:
                                        tweets = tweets.append(pd.read_csv(path + '/' + files))
                        
                        tweets.to_csv(self.base_directory + '/' + val + '/analysis/Basic' + use + '.csv')
            if full:
                tweets = pd.DataFrame()
                for val in os.listdir(self.base_directory):
                    if ('analysis' not in val) & ('.DS_Store' not in val) & (os.path.isdir(self.base_directory + '/' + val ) == True):
                        tweets = tweets.append(pd.read_csv(self.base_directory + '/' + val + '/analysis/Basic' + use + '.csv'))
                if not os.path.exists(self.base_directory + 'analysis/' ):
                    os.mkdir(self.base_directory + 'analysis/' )     
                tweets.to_csv(self.base_directory + 'analysis/Basic' + use + '.csv')                           
                                                   
                
                
            
            

class analysis:
    def __init__(self):
        pass
    
    def look_all():
        print('looking')
        