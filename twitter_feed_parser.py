#!/usr/bin/env python
# encoding: utf-8

'''
This Python 3.6 script will parse a twitter feed and return the 10 words
that the user uses the most, in the form of a pie chart

Just type in the username of the account you want to visualize after the prompt

@author: Yannick Le Roux https://github.com/YannickLeRoux
@created: July 20th 2017
@inspired by @yanofsky https://github.com/yanofsky

'''

import tweepy # https://github.com/tweepy/tweepy

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""




def get_all_tweets(screen_name):
    '''
    this function comes from https://gist.github.com/yanofsky/5436496
    Get all the tweets from a specific user: screen_name via API
    Twitter only allows access to a users most recent 3240 tweets with this method
    Returns a string of all tweets
    '''

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []	

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before", oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print ("...", len(alltweets), "tweets downloaded so far")
	
    text_tweets = " ".join([tweet.text for tweet in alltweets])
    return text_tweets

def wordCount(strng, blacklist):
    '''
    input: a string
    output: a dict with the count of each word in the string
    '''
    wordcount = {}
    
    for word in strng.split():
        if len(word) < 3 or word.lower() in blacklist or '@' in word or '#' in word:
            continue
        if word.lower() not in wordcount:
            wordcount[word.lower()] = 1
        else:
            wordcount[word.lower()] += 1
    return wordcount # its a dict

def top10words(word_dict):
    '''
    input: a dict {word:count word}
    output: a sorted list of tuples word,count for the 
    10 highest values of count
    '''
    from collections import Counter
    d = Counter(word_dict)
    return d.most_common(10) 

def visualize_keywords(count_tuples_list):
    '''
    draws a pie chart from a list of tuples (label, size)
    '''
    import matplotlib.pyplot as plt
    import datetime
    fig = plt.figure()
    fig.suptitle('@' +str(user_name) + ' 10 Most Used Words on Twitter\n'+ str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    plt.axis("equal")
    plt.pie([sizes for labels, sizes in count_tuples_list], shadow=True, startangle=90)
    plt.legend([labels +': '+ str (sizes) for labels, sizes in count_tuples_list], loc="best")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    user_name = input('Type in the username of the account you want to parse(q to quit): ')
         
    # this file contains words that are not useful for this data analysis
    with open ('blacklist.txt','r') as b:
        blacklist= b.read().split()
    
    alltweets = get_all_tweets(user_name)
    word_dict = wordCount(alltweets, blacklist)
    keywords_dict = top10words(word_dict)
    visualize_keywords(keywords_dict)

