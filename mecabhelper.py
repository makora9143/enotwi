#! /usr/bin/env python
# -*- encoding: utf-8 -*-

"""

"""

from MeCab import Tagger

class MecabHelpler(object):
	"""docstring for MecabHelpler"""
	def __init__(self, dic="mecabrc"):
		self.mecab = Tagger(dic)
		self._data = []
		self._words = {}

	def add_text(self, text):
		self._data.append(text)

	def get_texts(self):
		return self._data

	def parse_to_node(self):
		return self.mecab.parseToNode('\n'.join(self._data))

	def count_words(self):
		node = self.parse_to_node()
		while node:
		    word = node.surface
    		if node.posid >=36 and node.posid <=67:
        		if not self._words.has_key(word):
        			self._words[word] = 0
        		self._words[word] += 1
    		node = node.next

	def show_result(self): 
		for word,count in self._words.items():
    		print word, count	

   	def get_result(self):
   		return self._words