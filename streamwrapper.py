#! /usr/bin/env python
#-*- encoding: utf-8 -*-

"""StreamWrapper

    tweepy.StreamListenerをよしなに扱うためのクラス
"""

import json
import os
from time import localtime, strftime
from tweepy.streaming import StreamListener


class StreamWrapper(StreamListener):
    """StreamListenerのラッパークラス"""
    def __init__(self, dirname):
        self.dirname = dirname
        if not os.path.isdir(self.dirname):
            os.mkdir(self.dirname)

    def on_data(self, data):
        """json形式の確認とファイルに書き出し"""
        if data.startswith("{"):
            json_data = json.loads(data)
            if json_data['id_str'] and json_data['geo']:
                self.output_to_file(data)

    def output_to_file(self, data):
        """json形式でファイルに出力"""
        json_file = ("%s%s.json"
                    % (self.dirname, strftime("%Y%m%d%H%M", localtime())))
        with open(json_file, 'a') as f:
            f.write(data)



# End of Line.
