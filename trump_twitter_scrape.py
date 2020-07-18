#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 22:14:10 2020

@author: Jacob
"""

import pandas as pd
from datetime import datetime as dt, timedelta 
import GetOldTweets3 as got 
import time

username='realDonaldTrump'
start_date=dt.strptime('09-01-01', '%y-%m-%d').date()
end_date=dt.today().date()+timedelta(days=1)

def get_tweets(username, start_date, end_date):
    """
    Parameters
    ----------
    username : twitter username, string. does not include @
    start_date : date as a datetime date
    end_date : date as a datetime date
    Returns
    -------
    Saves a pandas dataframe of all the tweets to a csv, subject to there being approx <10000 tweets per year
    """
    n=0
    while start_date<=end_date: 
        n+=1
        tweetCriteria=got.manager.TweetCriteria().setUsername(username).setSince(str(start_date)).\
            setUntil(str(start_date+timedelta(days=365)))
            
        tweets=got.manager.TweetManager.getTweets(tweetCriteria)
        print('Scrape %d complete.' % n) 
        
        user_tweets=[[tweet.text, tweet.date, tweet.retweets, tweet.favorites,
              tweet.mentions, tweet.hashtags] for tweet in tweets]
        if n==1:
            tweets_df=pd.DataFrame(user_tweets, columns=['content', 'date', 'retweets', \
                                                         'favorites', 'mentions', 'hashtags'])
            tweets_df.sort_values(by='date', ascending=True, inplace=True)
        else:
            temp_df=pd.DataFrame(user_tweets, columns=['content', 'date', 'retweets', \
                                                         'favorites', 'mentions', 'hashtags'])
            temp_df.sort_values(by='date', ascending=True, inplace=True)
            tweets_df=pd.concat([tweets_df, temp_df])
        
        start_date=start_date+timedelta(days=365)
        print('Step %d complete.' % n)
        print('Starting 10 min rest...')
        time.sleep(601)
        print('...10 min rest complete.')
        
    tweets_df.to_csv('trump_tweets_final.csv')
    print('Done')   


get_tweets(username, start_date, end_date)