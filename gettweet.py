#! /usr/bin/env python
#-*- encoding: utf-8 -*-

"""GetTweet

    江ノ島近郊ツイート取得モジュール
"""

import json
import os
from time import localtime, strftime, sleep
from tweepy.streaming import Stream
from tweepy.auth import OAuthHandler
from twitteroauth import TwitterOauth


def log_message(level, message):
    """ログメッセージを表示する"""
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    logmsg = t + ' [' + level + ']: ' + message
    return logmsg 


def get_oauth():
    """Twitterの認証を得る"""
    oauth = TwitterOauth()
    consumer_key = oauth.get_consumer_key()
    consumer_secret = oauth.get_consumer_secret()
    access_key = oauth.get_access_key() 
    access_secret = oauth.get_access_secret()
    oauth = OAuthHandler(consumer_key, consumer_secret)
    oauth.set_access_token(access_key, access_secret)
    return oauth


def crawling(latlngs, root_dir):
    """latlngの範囲内のツイートをroot_dir下に保存する"""
    start_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print log_message('INFO', 'crawling start')
    oauth = get_oauth()
    streming = Stream(oauth, StreamWrapper(root_dir), secure=True)
    streming.filter(locations=latlngs)


def get_tweet(latlngs, root_dir='tweets/'):
    """ ツイート取得 """
    print log_message('INFO', 'process start')
    while True:
        try:
            crawling(latlngs, root_dir)
        except Exception, e:
            print log_message('ERR', str(e))
            sleep(10)



if __name__ == '__main__':
    zenkoku = [139, 20.42,
               148.75, 45.42,
               132, 20.42,
               139, 39,
               129, 20.42,
               132, 35, 
               122.93, 20.42,
               129, 33]
    enoshima = []
    get_tweet(zenkoku)
