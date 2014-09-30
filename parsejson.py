#! /usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
import pytz
import json


class ParseJson(object):
    """jsonファイルを1時間分パース"""
    def __init__(self):
        self._fileset = []

    def set_fileset(self):
        """ 現時刻から１時間前までのjsonファイル名を取得、フィールドに代入 """
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        hour_ago = now - timedelta(hours=1)
        for i in xrange(0, 60):
            filetime = hour_ago + timedelta(minutes=i)
            filename = filetime.strftime("%Y%m%d%H%M.json")
            self._fileset.append(filename)

    def get_fileset(self):
        """ ファイルセットを取得 """
        return self._fileset

    def load_one_json(self, filename):
        """ filenameのjsonを読み込んで返す """
        with open(filename) as f:
            json_file = json.load(f)
        return json_file

    def parse_text_from_json(self, filename):
        json_file = self.load_one_json(filename)
        return json_file['statuses'][0]['text']

    def load_all_json(self):
        texts = []
        for filename in self._fileset:
            try:
                texts.append(self.parse_text_from_json(filename))
            except:
                continue
        return texts

if __name__ == '__main__':
    hoge = ParseJson()
    hoge.set_fileset()
    print hoge.load_all_json()
