#! /usr/bin/env python
# -*- encoding: utf-8 -*-

"""ツイートを取得するクラス

    jsonファイルからツイートの本文を抽出するクラス
"""


from datetime import datetime, timedelta
import pytz
import json

HOUR = 60

class ParseJson(object):
    """jsonファイルを1時間分パース"""
    def __init__(self):
        self._fileset = []

    def set_fileset(self):
        """現時刻から１時間前までのjsonファイル名を取得、フィールドに代入"""
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        hour_ago = now - timedelta(hours=1)
        for i in xrange(HOUR):
            filetime = hour_ago + timedelta(minutes=i)
            filename = filetime.strftime("%Y%m%d%H%M.json")
            self._fileset.append('./tweets/' + filename)

    def get_fileset(self):
        """ファイルセットを取得"""
        return self._fileset

    def load_one_json(self, filename):
        """filenameのjsonを読み込んで返す"""
        tweets = []
        with open(filename) as f:
            for line in f:
                tweets.append(json.loads(line))
        return tweets

    def parse_text_from_json(self, filename):
        """ツイートの本文を抜き出して返す"""
        tweets = self.load_one_json(filename)
        texts = []
        for tweet in tweets:
            texts.append(tweet.get('text').encode('utf-8'))
        return texts

    def load_all_json(self):
        """一時間分のツイート本文を返す"""
        texts = []
        for filename in self._fileset:
            try:
                texts += self.parse_text_from_json(filename)
            except Exception, e:
                print e
                continue
        return texts

if __name__ == '__main__':
    hoge = ParseJson()
    hoge.set_fileset()
    import pprint
    texts = []
    texts += hoge.parse_text_from_json('./tweets/201410010056.json')
    pprint.pprint(texts)
