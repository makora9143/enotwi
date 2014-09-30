#! /usr/bin/env python
#-*- encoding: utf-8 -*-

"""GetTweet
江ノ島近郊ツイート取得モジュール

"""

import json
import os
from time import localtime, strftime, sleep
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler


class AbstractListener(StreamListener):
    """StreamListenerのラッパー"""
    def __init__(self, dirname):
        self.dirname = dirname
        if not os.path.isdir(self.dirname):
            os.mkdir(self.dirname)

    def on_data(self, data):
        """ json形式の確認とファイルに書き出し """
        if data.startswith("{"):
            json_data = json.loads(data)
            if json_data['id_str'] and json_data['geo']:
                self.output_to_file(data)

    def output_to_file(self, data):
        """ json形式でファイルに出力 """
        json_file = ("%s%s.json"
                    % (self.dirname, strftime("%Y%m%d%H%M", localtime())))
        with open(json_file, 'a') as f:
            f.write(data)


def log_message(level, message):
    t = strftime("%Y-%m-%d %H:%M:%S", localtime())
    str = t + ' [' + level + ']: ' + message
    return str


def get_oauth():
    consumer_key = ''
    consumer_secret = ''
    access_key = ''
    access_secret = ''
    consumer_key = 'c6a9NIWzkHIs5Lxo7wgc9w'
    consumer_secret = 'Xf7gAMCrZMq6AkgUk7uGMeSIbtYUDGzOsZ8pz1CXE'
    access_key = '133119533-YqpDDbh466kTcs8cSaSuvIKC0JY63F1vrp2O1cJ7'
    access_secret = '9aqYuxTVJi2fsbMrBoL5UcMBPyfUjMERLvScRP6pyQ'
    oauth = OAuthHandler(consumer_key, consumer_secret)
    oauth.set_access_token(access_key, access_secret)
    return oauth


def start_crawl(latlngs, dirname):
    start_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print log_message('INFO', 'crawling start')
    oauth = get_oauth()
    streming = Stream(oauth, AbstractListener(dirname), secure=True)
    streming.filter(locations=latlngs)


def get_tweet(latlngs, dirname='tweets/'):
    """ ツイート取得 """
    print log_message('INFO', 'process start')
    while True:
        try:
            start_crawl(latlngs, dirname)
        except Exception, e:
            print log_message('ERR', str(e))
            sleep(10)

def main():
    get_tweet([
        139, 20.42, 148.75, 45.42, 132,
        20.42, 139, 39, 129, 20.42, 132, 35, 122.93, 20.42,
        129, 33])


if __name__ == '__main__':
    main()

# End of Line.
