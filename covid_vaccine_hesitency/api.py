"""
Emily Giverts
CSE 163 AC

A file that accesses the twitter API, queries 1000 public tweets, and stores
information such as tweet text and user location within a CSV file.
"""

import tweepy
import pandas as pd

consumer_key = '8wUJBK1HDSCl7QEelgfctdB0A'
consumer_secret = 'TPlOBhSW8kwYbr8iHgW7sAPKyloSAWiXoB2FqYOhCgYvhlKFns'
access_token = '2891397858-tARckCXsqVbdLJh0oiPjK8fE0SiLnMeLO45eClA'
access_token_secret = 'VUsBAtsX9rE5dXbV3xjWjaJz5tXTK2pog0E8BJB2lZTJM'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

text_query = 'vaccine deep state'
max_tweets = 1000

# Creation of query method using parameters

tweets = tweepy.Cursor(api.search, q=text_query).items(max_tweets)


# Pulling information from tweets iterable object
tweets_list = [[tweet.text, tweet.user.location] for tweet in tweets]

# Creation of dataframe from tweets_list
tweets_df = pd.DataFrame(tweets_list)
tweets_df.to_csv('covid_vaccine_hesitency/main_data/newapidata.csv', index=False, header=True)

