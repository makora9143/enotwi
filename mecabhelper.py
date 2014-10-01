#! /usr/bin/env python
# -*- encoding: utf-8 -*-

u"""MecabHelpler MeCabで名詞を抜き出すためのクラス


"""

from MeCab import Tagger


class MecabHelpler(object):
    u"""docstring for MecabHelpler"""
    def __init__(self, dic="mecabrc"):
        self.mecab = Tagger(dic)
        self._data = []
        self._words = {}

    def add_text(self, text):
        u"""text一文を追加する"""
        self._data.append(text)

    def replace_texts(self, texts):
        u"""text複数文を差し替える"""
        self._data = texts

    def get_texts(self):
        u"""保持している文を返す"""
        return self._data

    def parse_to_node(self):
        u"""形態素解析する"""
        return self.mecab.parseToNode('\n'.join(self._data))

    def count_words(self):
        u"""単語の頻出数をカウントする"""
        node = self.parse_to_node()
        while node:
            word = node.surface
            if node.posid >= 36 and node.posid <= 67:
                if not word in self._words:
                    self._words[word] = 0
                self._words[word] += 1
            node = node.next

    def show_result(self):
        u"""結果を表示する"""
        for word, count in self._words.items():
            print word, count

    def get_result(self):
        return self._words

if __name__ == '__main__':
    mecab = MecabHelpler()
    mecab.add_text("Webデザインの流行りを知るために、トレンド感のある配色や洗練"
                   "されたレイアウトをつくり上げるために、"
                   "知っておきたいことや方法など。")
    mecab.count_words()
    mecab.show_result()
