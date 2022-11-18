#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

This script generates the object types TwitterActivity, TwitterEvent, and 
TwitterKey. The associated functions for poplating these objects is also included.

@author: claudiakann
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'ckann10'
__license__ = 'claudiakann'
__copyright__ = 'Copyright 2022 ckann10'

import os
# import TwitterAPI as TwitterAPI
import pandas as pd
import warnings
from datetime import datetime
# import time
from .pulling_functions import pulling_functions as pull
from .checking_functions import checking_functions as check
from .analysis_function import analysis, read

class TwitterActivity:
    def __init__(self, ID, starting_date, ending_date, CityTown, StateTerritory, Date, BestGuess):
        self.ID = ID
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.CityTown = CityTown
        self.StateTerritory = StateTerritory
        self.Date = Date
        self.BestGuess = BestGuess
        self.indiv_timeline = False
        self.period_start = "0"
        self.period_end = "0"
        self.west = "0"
        self.east = "0"
        self.south = "0"
        self.north = "0"

        
    def add_timing(self, period_start, period_end):
        self.period_start = period_start
        self.period_end = period_end
        self.indiv_timeline = True
        

class TwitterKeyPair:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        
class TwitterEvent:
    def __init__(self, name, base_directory = '', separator = 'CityTown'):
        self.name = name
        self.keys = []
        self.activities = []
        self.keywords = []
        self.location = pd.DataFrame(columns = ['CityTown', 'StateTerritory', 'west', 'south', 'east', 'north'])
        self.base_directory = base_directory
        self.read = read()
        self.pull = pull()
        self.check = check()
        self.analysis = analysis()
        self.separator = separator
    
    def add_key(self, keypair):
        if isinstance(keypair, list):
            for k in keypair:
                if isinstance(k, TwitterKeyPair):
                    self.keys.append(k)
                else:
                    warnings.warn("Entry in list is not a TwitterKeyPair object")
                    warnings.warn("Check documentation") 
        elif isinstance(keypair, TwitterKeyPair):
            self.keys.append(keypair)
        else:
            warnings.warn("Key pair inputed is not a TwitterKeyPair or list of TwitterKeyPair objects")
            warnings.warn("Check documentation")

    
    def add_activity(self, activity):
        if isinstance(activity, list):
            for e in activity:
                if isinstance(e, TwitterActivity):
                    self.activities.append(e.__dict__)
                else:
                    warnings.warn("Entry in list is not a TwitterActivity object")
                    warnings.warn("Check documentation") 
        elif isinstance(activity, TwitterActivity):
            self.activities.append(activity.__dict__)
        else:
            warnings.warn("activity inputed is not a TwitterActivity or list of TwitterActivity objects")
            warnings.warn("Check documentation")
            
    def add_keyWords(self, words):
        if isinstance(words, list):
            for w in words:
                self.keywords.append(w)
        else:
            self.keywords.append(words)
        self.keywords = list(set(self.keywords))
            
    def add_timing(self, start, end):
        self.start = start
        self.end = end
            
    def add_location(self,CityTown, StateTerritory,  west, south, east, north):
        self.location = self.location.append(pd.DataFrame({"CityTown": CityTown,
                                                           "StateTerritory": StateTerritory,
                                                           "west": west,
                                                           "south": south, 
                                                           "east": east,
                                                           "north" : north}), 
                                             ignore_index=True)
        
    def print_protests(self):
        self.protest_ids = pd.DataFrame()
        for e in self.activities:
            if e['indiv_timeline'] == False:
                temp_location = self.location.loc[self.location['CityTown'] == e['CityTown'],]
                temp_location.loc[temp_location['StateTerritory'] == e['StateTerritory'],]
                e['west' ] = temp_location['west'][0]
                e['south'] = temp_location['south'][0]
                e['east']  = temp_location['east'][0]
                e['north'] = temp_location['north'][0]
            self.protest_ids = self.protest_ids.append({'ID': e['ID'] , 'CityTown': e['CityTown'], 
                                 'StateTerritory': e['StateTerritory'], 'starting_date': e['starting_date'],
                                 'ending_date': e['ending_date'], 'BestGuess': e['BestGuess'], 
                                 'start': e['period_start'], 'end': e['period_end'],
                                 'west' : e['west'], 'south' : e['south'],
                                 'east' : e['east'], 'north' : e['north']}, ignore_index=True) 
                    
        self.protest_ids = self.protest_ids.dropna()

    
    def upload_from_excel(self, path = "event_template.xlsx"):   
        if not path.endswith(".xlsx"):
            path = self.base_directory + '/event_template.xlsx'
            warnings.warn("Path doesn't Lead to a Excel File")
            print('Using path ' + path)
        elif path == "event_template.xlsx":
            path = self.base_directory + '/event_template.xlsx'
            print('Using path ' + path)
        else:
            print('Using path ' + path)
        data = pd.read_excel(path, sheet_name = "activities") 
        for index, row in data.iterrows():
            row = row.dropna()
            try:
                activity = TwitterActivity(ID = row['ID'], starting_date = row['starting_date'],
                                     ending_date = row['ending_date'], CityTown = row['CityTown'],
                                     StateTerritory = row['StateTerritory'] , Date = row['Date'],
                                     BestGuess = row['BestGuess'])
                if ('period_start' in row.keys() and 'period_end' in row.keys()):
                    activity.add_timing(row['period_start'], row['period_end'])
                self.add_activity(activity)
            except:
                warnings.warn('Could not add activity')
                print(row)
                print('Missing necessary columns')
                print(list(set(['ID','starting_date','ending_date','CityTown', 'StateTerritory','Date','BestGuess']) - set(row.keys())))
                    
                
        time_span = pd.read_excel(path, sheet_name = "time span") 
        self.add_timing(str(time_span.iloc[0]['start time']).replace("\ufeff", "") , str(time_span.iloc[0]['end time']).replace("\ufeff", "") )
      
    
        keywords = [str(x).replace("\ufeff", "") for x in list(pd.read_excel(path, sheet_name = "keywords")['keywords'])] 
        self.add_keyWords(keywords)
    
        location = pd.read_excel(path, sheet_name = "location")
        self.add_location(CityTown = location['CityTown'], StateTerritory = location['StateTerritory'],
                         west = location['west longitude'], south = location['south latitude'],
                         east = location['east longitude'], north = location['north latitude'])
       
        keys = pd.read_excel(path, sheet_name = "keys") 
        
        for i, k in keys.iterrows():
            key = TwitterKeyPair(keys.iloc[i]['key'], keys.iloc[i]['secret'])
            self.add_key(key)
        self.print_protests()
        
    def upload_from_file_structure(self):
        for sep in os.listdir(self.base_directory):
            if ('analysis' not in sep) & ('.DS_Store' not in sep) & (os.path.isdir(self.base_directory + '/' + sep) == True):
                for activity in os.listdir(self.base_directory + '/' + sep):
                    if ('analysis' not in activity) & ('.DS_Store' not in activity):
                        dt = activity.split("_")[1].split("-")
                        e = TwitterActivity(activity, 
                                            dt[1] + ' ' + dt[0] + ' ' + dt[2] + ' 00:00:00',
                                            0, sep, 0, (activity.split(sep + '_')[1].replace("_", " ")), 0)
                        self.add_activity(e)
                        
                    
        
        
