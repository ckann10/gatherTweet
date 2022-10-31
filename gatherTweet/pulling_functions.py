#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: Oct. 31, 2022

This script introduces the functions used to access the Twitter API and
pull the data from the platform. The most important function in this case is 
get_tweets. The rest are used within the wrapper.

@author: claudiakann
"""
__title__ = 'gatherTweet'
__version__ = '1.0'
__author__ = 'ckann10'
__license__ = 'claudiakann'
__copyright__ = 'Copyright 2022 ckann10'


from TwitterAPI import TwitterRequestError, TwitterConnectionError, TwitterAPI
from datetime import datetime, timedelta
from requests import HTTPError, ConnectionError
import uuid
import json
import os
import time
import dateutil.parser
import pytz
import io
utc=pytz.UTC

class pulling_functions:    
    def __init__(self):
      pass
        
        
    def get_tweets(self, event, 
                   types = [],
                   max_results = 500,
                   tweets_per_file = 1000,
                   expansions = ['author_id', 'in_reply_to_user_id'],
                   tweetfields = ['author_id','created_at', 'geo','entities','public_metrics', 'text','referenced_tweets']):
    
        base_directory = event.base_directory
        APIs, PARAMS = self.version_2_setup(event, max_results, expansions, tweetfields)
        if ('Core' in types) | (types == []):
            print('Finding Core Users')
            self.get_core_users(event, PARAMS, APIs, tweets_per_file)
        if ('CoreTimeline' in types) | (types == []):
            run = 1
            for activity in event.activities:
                sep_value = eval('activity["'+ event.separator+'"]')
                if [x for x in os.listdir(base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + "/Core") if x != ".DS_Store"] == []:
                    print("At least one activity does not have a core")
                    run = 0
                    break
            if run:
                self.get_core_timeline(event, PARAMS, APIs, tweets_per_file)
    
        if ('Echos' in types) | (types == []):
            run = 1
            for activity in event.activities:
                sep_value = eval('activity["'+ event.separator+'"]')
                if [x for x in os.listdir(base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + "/Core") if x != ".DS_Store"] == []:
                    print("At least one activity does not have a core")
                    run = 0
                    break
            if run:
                self.get_echo_users(event, PARAMS, APIs, tweets_per_file)
     
        if ('EchosTimeline' in types) | (types == []):
            run = 1
            for activity in event.activities:
                sep_value = eval('activity["'+ event.separator+'"]')
                if [x for x in os.listdir(base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + "/Echo") if x != ".DS_Store"] == []:
                    print("At least one activity does not have a list of Echos")
                    run = 0
                    break 
            if run:
               self.get_echo_timeline(event, PARAMS, APIs, tweets_per_file) 
    

        if ('Influences' in types) | (types == []):
            run = 1
            for activity in event.activities:
                sep_value = eval('activity["'+ event.separator+'"]')
                if [x for x in os.listdir(base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + "/Core") if x != ".DS_Store"] == []:
                    print("At least one activity does not have a core")
                    run = 0
                    break  
            if run:
                self.get_influence_users(event, PARAMS, APIs, tweets_per_file)
    
    
        if ('InfluencesTimeline' in types) | (types == []):
            run = 1
            for activity in event.activities:
                sep_value = eval('activity["'+ event.separator+'"]')
                if [x for x in os.listdir(base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") + "/Influences") if x != ".DS_Store"] == []:
                    print("At least one activity does not have a list of Influences")
                    run = 0
                    break 
            if run:
                self.get_influences_timeline(event, PARAMS, APIs, tweets_per_file) 

    
    
    def version_2_setup(self, event,
                    max_results = 500,
                    expansions = ['author_id', 'in_reply_to_user_id'],
                    tweetfields = ['author_id','created_at', 'geo',
                              'entities','public_metrics', 'text',
                              'referenced_tweets']):
        
        base_directory = event.base_directory
        if base_directory == "":
            base_directory = os.getcwd()
    
        print('Directory set to ' + base_directory)
        
        exp = ','.join(expansions)
        tw_fields = ','.join(tweetfields)
        PARAMS = {'max_results': max_results,
                  'expansions': exp,
                  'tweet.fields': tw_fields}
        
        APIs = []
        for i in event.keys:
            APIs += [TwitterAPI(i.key,
                  i.secret,
                  auth_type='oAuth2',
                  api_version='2')]
            
        return APIs, PARAMS
        
        
    def get_core_users(self, event, PARAMS, APIs, tweets_per_file = 1000):
        print('core')
        base_directory = event.base_directory
        api_i = 0
        file_prefix = 'twitter-'
        basehashtags = event.keywords
        for activity in event.activities:
            sep_value = eval('activity["'+ event.separator+'"]')
            if not os.path.isdir(base_directory +'/' + sep_value): # create activity folder
                os.mkdir(base_directory +'/' + sep_value) 
            sub_directory = base_directory +'/' + sep_value
            os.chdir(sub_directory)
            base_query = '-is:retweet bounding_box:[' + str(activity['west']) + ' ' + str(activity['south']) + ' ' + str(activity['east']) + ' ' + str(activity['north']) + "]"
            print(base_query)
            PARAMS['query'] = base_query        
            protest_folder = sub_directory + "/" + sep_value + "_" + activity['Date'].replace(" ", "-") #create subactivity folders
            if not os.path.isdir(protest_folder):
                os.mkdir(protest_folder)
            core_folder = protest_folder + "/Core" #create Core user folder
            if not os.path.isdir(core_folder):
                os.mkdir(core_folder)
            os.chdir(core_folder)
            
            # clean up starting and end date to be usable   
            datestart = datetime.strptime(activity['starting_date'], '%d %m %Y %H:%M:%S')
            dateend = datetime.strptime(activity['ending_date'], '%d %m %Y %H:%M:%S')
            PARAMS['end_time'] = dateend.isoformat() + 'Z'
            PARAMS['start_time'] = datestart.isoformat() + 'Z'
            
            #search for all hashtagsf
            for basetag in basehashtags:
                PARAMS['query'] = basetag + ' ' + base_query
                print("Query:" + str(PARAMS['query']))
                out = self.pull_tweets(PARAMS,datestart, APIs, api_i, file_prefix, tweets_per_file)
                api_i = out[3]
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['end_time'] = dateend.isoformat() + 'Z'
                PARAMS['start_time'] = datestart.isoformat() + 'Z'
                time.sleep(3) # prevent too many requests error    
        
        
    def get_core_timeline(self, event, PARAMS, APIs,  tweets_per_file = 1000):
        base_directory = event.base_directory
        api_i = 0
        base_query = 'from:'
        file_prefix = 'twitter-coreTimeline-'
        os.chdir(base_directory)
        
        for activity in event.activities:
            sep_value = eval('activity["'+ event.separator+'"]')
            if activity['indiv_timeline']== True:
                datestart = datetime.strptime(activity['period_start'], '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(activity['period_end'], '%d %m %Y %H:%M:%S')
            else:
                datestart = datetime.strptime(event.start, '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(event.end, '%d %m %Y %H:%M:%S')
    
            print(sep_value + "_" + activity['Date'].replace(" ", "-"))
            layer1_ids = []
            l_ids = []
            temp_dir = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-")
            files = os.listdir(temp_dir)
            if 'Core' in files:
                layer1_ids = self.get_ids(temp_dir + '/Core') 
                print("# of users in Core: "  + str(len(layer1_ids)))
            if 'CoreTimeline' in files:
                l_ids = self.get_ids(temp_dir + 'CoreTimeline')
                print("# of users already collected: "  + str(len(l_ids)))
    
            layer1_ids = layer1_ids.difference(l_ids)
            print("# of users left to be collected: " + str(len(layer1_ids)))
                    
            if not os.path.exists(temp_dir + "/CoreTimeline"):
                os.mkdir(temp_dir + "/CoreTimeline")
            os.chdir(temp_dir + "/CoreTimeline")
    
    
            PARAMS['end_time'] = dateend.isoformat() + 'Z'
            PARAMS['start_time'] = datestart.isoformat() + 'Z'
            
            for user in layer1_ids:
                file_prefix = 'twitter-'
                PARAMS['query'] = base_query +  user
                out = self.pull_tweets(PARAMS,datestart, APIs,api_i, file_prefix, tweets_per_file)
                api_i = out[3]
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['end_time'] = dateend.isoformat() + 'Z'
                PARAMS['start_time'] = datestart.isoformat() + 'Z'
                time.sleep(3)    
    
    
    def get_echo_users(self, event, PARAMS, APIs,  tweets_per_file = 1000):
        base_directory = event.base_directory
        data = []
        count = 0
        id_echo = []
        api_i = 0
        file_prefix = 'twitter-echos-'
        base_query = 'retweets_of:'
        for activity in event.activities:
            sep_value = eval('activity["' + event.separator + '"]')
            # Check Core
            twitter_id_list = []
            folder_path = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-")
            twitter_id_list = list(set(self.get_ids(folder_path + '/Core')))
            if not os.path.isdir(folder_path + '/Echo'):
                os.mkdir(folder_path + '/Echo')
            
            folder_path = folder_path + '/Echo'
            
            for user in twitter_id_list:
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['query'] = base_query + str(user)
                center_date = datetime.strptime(activity['starting_date'], '%d %m %Y %H:%M:%S')
                end_date = center_date + timedelta(days=2)
                start_date = center_date +timedelta(days=-2)
                PARAMS['end_time'] = end_date.isoformat() + 'Z'
                PARAMS['start_time'] = start_date.isoformat() + 'Z'
                print(str(user) + ' tweets')
                new_data = self.pull_tweets(PARAMS,start_date, APIs,api_i, file_prefix, tweets_per_file, echo = True)
                if new_data[1] == 0:
                    print("skip")
                    time.sleep(3)
                    continue
                print(new_data[1])
                count += new_data[1]
                temp_data = new_data[0]
                id_echo.extend(new_data[2])
                api_i = new_data[3]
                print(count)
                if len(temp_data) > 0:
                     data.extend(temp_data) #addresses layer 3a
                if len(data) >= tweets_per_file:
                    timestamp = datetime.strptime(data[-1]["created_at"][:-5], '%Y-%m-%dT%H:%M:%S')
                    file_name = (file_prefix + timestamp.strftime("%Y-%m-%d-%H-%M-%S") +'-' + str(uuid.uuid4()) + '.txt')
                    with io.open(file_name, "w", encoding="utf-8") as f:
                        f.write(json.dumps(data))
                    data = []
                time.sleep(3)
            if len(data) > 0:
                timestamp = datetime.strptime(data[-1]["created_at"][:-5], '%Y-%m-%dT%H:%M:%S')
                file_name = (file_prefix + timestamp.strftime("%Y-%m-%d-%H-%M-%S") +'-' + str(uuid.uuid4()) + '.txt')
                with io.open(file_name, "w", encoding="utf-8") as f:
                        f.write(json.dumps(data))
                with io.open('%s/echo-ids.txt' % (folder_path), "w", encoding="utf-8") as f:
                        for r in id_echo:
                                f.write('%s\n' % (r))   
                                
                                
    def get_echo_timeline(self, event, PARAMS, APIs,  tweets_per_file = 1000):
        base_directory = event.base_directory
        api_i = 0
        base_query = 'from:'
        file_prefix = 'twitter-echoTimeline-'
        os.chdir(base_directory)
        
        for activity in event.activities:
            sep_value = eval('activity["'+ event.separator+'"]')
            if activity['indiv_timeline']== True:
                datestart = datetime.strptime(activity['period_start'], '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(activity['period_end'], '%d %m %Y %H:%M:%S')
            else:
                datestart = datetime.strptime(event.start, '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(event.end, '%d %m %Y %H:%M:%S')
    
            print(sep_value + "_" + activity['Date'].replace(" ", "-"))
            echo_ids = []
            e_ids = []
            temp_dir = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-")
            files = os.listdir(temp_dir)
            if 'Echo' in files:
                with open(temp_dir + "/Echo/echo-ids.txt") as f:
                    x = f.readlines()
                    for a in x:
                        echo_ids.append(int(a))
                    echo_ids = set(echo_ids)
                    print("# of Echo users: "  + str(len(echo_ids)))
            if 'EchoTimeline' in files:
                e_ids = self.get_ids(temp_dir + '/EchoTimeline')
                print("# of users already collected: "  + str(len(e_ids)))
    
            echo_ids = echo_ids.difference(e_ids)
            print("# of users left to be collected: " + str(len(echo_ids)))
                    
            if not os.path.exists(temp_dir + "/EchoTimeline"):
                os.mkdir(temp_dir + "/EchoTimeline")
            os.chdir(temp_dir + "/EchoTimeline")
    
    
            PARAMS['end_time'] = dateend.isoformat() + 'Z'
            PARAMS['start_time'] = datestart.isoformat() + 'Z'
            
            for user in echo_ids:
                PARAMS['query'] = base_query +  str(user)
                out = self.pull_tweets(PARAMS,datestart, APIs,api_i, file_prefix, tweets_per_file)
                api_i = out[3]
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['end_time'] = dateend.isoformat() + 'Z'
                PARAMS['start_time'] = datestart.isoformat() + 'Z'
                time.sleep(3)        
                
    def get_influence_users(self, event, PARAMS, APIs,  tweets_per_file = 1000):
        base_directory = event.base_directory
        data = []
        count = 0
        id_influence = []
        api_i = 0
        file_prefix = 'twitter-influences-'
        base_query = 'is:retweet from:'
        for activity in event.activities:
            sep_value = eval('activity["' + event.separator + '"]')
            # Check Core
            twitter_id_list = []
            folder_path = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-")
            twitter_id_list = list(set(self.get_ids(folder_path + '/Core')))
            if not os.path.isdir(folder_path + '/Influence'):
                os.mkdir(folder_path + '/Influence')
            
            folder_path = folder_path + '/Influence'
            
            for user in twitter_id_list:
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['query'] = base_query + str(user)
                center_date = datetime.strptime(activity['starting_date'], '%d %m %Y %H:%M:%S')
                end_date = center_date + timedelta(days=2)
                start_date = center_date +timedelta(days=-2)
                PARAMS['end_time'] = end_date.isoformat() + 'Z'
                PARAMS['start_time'] = start_date.isoformat() + 'Z'
                print(str(user) + ' retweets')
                new_data = self.pull_tweets(PARAMS,start_date, APIs,api_i, file_prefix, tweets_per_file, influence = True)
                count += new_data[1]
                temp_data = new_data[0]
                id_influence.extend(new_data[2])
                api_i = new_data[3]
                print(count)
                if len(temp_data) > 0:
                     data.extend(temp_data) #addresses layer 3a
                if len(data) >= tweets_per_file:
                    timestamp = datetime.strptime(data[-1]["created_at"][:-5], '%Y-%m-%dT%H:%M:%S')
                    file_name = (file_prefix + timestamp.strftime("%Y-%m-%d-%H-%M-%S") +'-' + str(uuid.uuid4()) + '.txt')
                    with io.open(file_name, "w", encoding="utf-8") as f:
                        f.write(json.dumps(data))
                    data = []
                time.sleep(3)
            if len(data) > 0:
                timestamp = datetime.strptime(data[-1]["created_at"][:-5], '%Y-%m-%dT%H:%M:%S')
                file_name = (file_prefix + timestamp.strftime("%Y-%m-%d-%H-%M-%S") + '-' + str(uuid.uuid4()) + '.txt')
                with io.open(file_name, "w", encoding="utf-8") as f:
                        f.write(json.dumps(data))
                with io.open('%s/influence-ids.txt' % (folder_path), "w", encoding="utf-8") as f:
                        for r in id_influence:
                                f.write('%s\n' % (r))   
                                
    def get_influence_timeline(self, event, PARAMS, APIs,  tweets_per_file = 1000):
        base_directory = event.base_directory
        api_i = 0
        base_query = 'from:'
        file_prefix = 'twitter-influenceTimeline-'
        os.chdir(base_directory)
        
        for activity in event.activities:
            sep_value = eval('activity["'+ event.separator+'"]')
            if activity['indiv_timeline']== True:
                datestart = datetime.strptime(activity['period_start'], '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(activity['period_end'], '%d %m %Y %H:%M:%S')
            else:
                datestart = datetime.strptime(event.start, '%d %m %Y %H:%M:%S')
                dateend = datetime.strptime(event.end, '%d %m %Y %H:%M:%S')
    
            print(sep_value + "_" + activity['Date'].replace(" ", "-"))
            influence_ids = []
            e_ids = []
            temp_dir = base_directory +'/' + sep_value  + "/" + sep_value + "_" + activity['Date'].replace(" ", "-")
            files = os.listdir(temp_dir)
            if 'Influence' in files:
                with open(temp_dir + "/Influence/influence-ids.txt") as f:
                    x = f.readlines()
                    for a in x:
                        influence_ids.append(int(a))
                    influence_ids = set(influence_ids)
                    print("# of Influence users: "  + str(len(influence_ids)))
            
            if 'InfluenceTimeline' in files:
                e_ids = self.get_ids(temp_dir + '/InfluenceTimeline')
                print("# of users already collected: "  + str(len(e_ids)))
    
            influence_ids = influence_ids.difference(e_ids)
            print("# of users left to be collected: " + str(len(influence_ids)))
                    
            if not os.path.exists(temp_dir + "/InfluenceTimeline"):
                os.mkdir(temp_dir + "/InfluenceTimeline")
            os.chdir(temp_dir + "/InfluenceTimeline")
    
    
            PARAMS['end_time'] = dateend.isoformat() + 'Z'
            PARAMS['start_time'] = datestart.isoformat() + 'Z'
            
            for user in influence_ids:
                PARAMS['query'] = base_query +  str(user)
                out = self.pull_tweets(PARAMS,datestart, APIs,api_i, file_prefix, tweets_per_file)
                api_i = out[3]
                if 'until_id' in PARAMS:
                    del PARAMS['until_id']
                PARAMS['end_time'] = dateend.isoformat() + 'Z'
                PARAMS['start_time'] = datestart.isoformat() + 'Z'
                time.sleep(3)                                  
                
                
    def get_ids(self, path):
        ids = []
        for files in os.listdir(path):
            if 'twitter' in files:
                with open(path + "/" + files) as f:
                    file_content = f.read()
                data = json.loads(file_content)
        
                for tweet in data:
                    ids.append(tweet['author_id'])
        return set(ids)
    
    
    
    def pull_tweets(self, PARAMS, datestart, APIs, api_i, file_prefix, tweets_per_file, echo = False, influence = False):

        tweetCount = 0
        more_tweets = True
        data = []
        until_id = None
        first_call = True
        api = APIs[api_i]
        api_tot = len(APIs)
        api_try = 0
        ids = []
        while more_tweets:
            if (echo == True) & (influence == True):
                print('Can"t look for Echos and Influences at the same time, stopping process')
                more_tweets = 0
                break
            last_error = None
            retry = False
            # Searching tweets from REST API with tweet_mode = extended
            # The result contains until_id but not since_id. So use max_id-1 to avoid duplication
            try:
                if not first_call:
                    PARAMS['until_id'] = until_id
               
                response = api.request('tweets/search/all',PARAMS)
                n_tweets = 0
                
                for tweet in response:
                    time_stamp = tweet['created_at']
                    if echo == True:
                        ids.append(tweet['author_id'])
                    elif (influence == True) and ('entities' in tweet) and ('mentions' in tweet['entities']):
                        for indiv in tweet['entites']['mentions']:
                            ids.append(indiv['id'])
                    yourdate = dateutil.parser.parse(time_stamp)
                    datestart = datestart.replace(tzinfo=utc)
                    yourdate = yourdate.replace(tzinfo=utc)
                    if (yourdate < datestart): #check if tweet is in the correct time frame
                        more_tweets = False
                        break
                    data.append(tweet)
                    n_tweets += 1
                    until_id = int(tweet['id']) - 1
            
            
                # start_time and end_time conflict with until_id
                if first_call:
                    first_call = False
                    del PARAMS['start_time']
                    del PARAMS['end_time']
                
                #output tweets into file
                if (echo == False) and (influence == False):
                    if len(data) > tweets_per_file or n_tweets == 0:
                        if len(data) > 0:
                            timestamp = datetime.strptime(data[-1]["created_at"][:-5],
                                                          '%Y-%m-%dT%H:%M:%S')
                            file_name = (file_prefix +
                                          timestamp.strftime("%Y-%m-%d-%H-%M-%S") +
                                          '-' + str(uuid.uuid4()) + '.txt')
                            with open(file_name, 'w') as file:
                                file.write(json.dumps(data))
                            data = []
                            print("{} is saved.".format(file_name))
                if n_tweets == 0:
                    print("No more tweets found.")
                    more_tweets = False
                    continue
                tweetCount += n_tweets
                print("Downloaded {0} tweets".format(tweetCount))
            except IOError as ioe:
                print('[Caught IOError]\n' + str(ioe))
                retry = True
            except HTTPError as he:
                print('[Caught HTTPError]\n' + str(he))
                retry = True
            except ConnectionError as ce:
                print('[Caught ConnectionError]\n' + str(ce))
                retry = True
            except TypeError as te:
                print('[Caught TypeError]\n' + str(te))
                retry = True
            except TwitterConnectionError as tce:
                print('[Caught TwitterConnectionError]\n' + str(tce))
                retry = True
            except TwitterRequestError as tre:
                print('[Caught TwitterRequestError]\n' + str(tre))
                retry = True
            # retry strategy
            if not retry:
                time.sleep(3.01)
                continue
            if not last_error:
                last_error = datetime.now()
                error_count = 0
            if datetime.now() - last_error > timedelta(seconds = 900):
                error_count = 0
            wait = min(0.25 * 2**error_count, 30)
            last_error = datetime.now()
            error_count += 1
            if error_count >= 4:
                api_i = (api_i + 1)%api_tot
                error_count = 0
                api_try += 1
            if api_try > api_tot:
                print('Wait {} seconds before retrying...'.format(wait*10))
                time.sleep(wait*10)
            else:
                print('Wait {} seconds before retrying...'.format(wait))
                time.sleep(wait)
        return (data, tweetCount, ids, api_i)
            

            
        
    
        
        
        
        
        
        
        
        
        
