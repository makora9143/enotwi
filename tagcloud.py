#! /usr/bin/env python
# -*- encoding: utf-8 -*-

"""タグクラウド生成クラス

PerlのHTML::TagCloud参考
"""

import math
import random

BASE_FONT_SIZE = 12


class TagCloud(object):
    """タグクラウド生成クラス"""
    def __init__(self, levels=24):
        self.counts = {}
        self.urls = {}
        self.levels = float(levels)

    def add(self, tag, url, count):
        """ タグクラウドにタグ（リンクあり）を入れる"""
        self.counts[tag] = count
        self.urls[tag] = url

    def add_static(self, tag, count):
        """ タグクラウドにタグ（リンクなし）を入れる"""
        self.counts[tag] = count

    def css_for_tag(self, level, subclass):
        font = BASE_FONT_SIZE + level
        return ("span.tagcloud%d%s {font-size: %dpx;}\n"
                "span.tagcloud%d%s a{text-decoration: none;}\n"
                % (level, subclass, font, level, subclass))

    def css(self):
        """ cssを返す """
        css = "#htmltagcloud {text-align: center; line-height: 1;}\n"
        for level in xrange(int(self.levels)):
            css += self.css_for_tag(level, '')
        return css

    def tags(self, shuffle=False, limit=None):
        """ 上位limitのタグを返す """
        counts = self.counts.copy()
        urls = self.urls.copy()
        tags = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        if limit:
            tags = tags[0:limit]
        if not tags:
            return tags

        min_tag = math.sqrt(tags[-1][1])
        max_tag = math.sqrt(tags[0][1])

        if max_tag - min_tag == 0:
            min_tag = min_tag - self.levels
            factor = 1
        else:
            factor = self.levels / (max_tag - min_tag)

        if len(tags) < self.levels:
            factor *= len(tags) / self.levels

        tag_items = []
        for tag in tags:
            tag_item = {}
            tag_item['name'] = tag[0]
            tag_item['count'] = tag[1]
            if tag[0] in urls:
                tag_item['url'] = urls[tag[0]]
            else:
                tag_item['url'] = None
            level = (int((math.sqrt(tag_item['count']) - min_tag) * factor))
            tag_item['level'] = level
            tag_items.append(tag_item)
        if shuffle:
            random.shuffle(tag_items)
        return tag_items

    def format_span(self, name, url, level):
        subclass = ""
        span_class = "tagcloud%d%s" % (level, subclass)
        span = "<span class='%s'>" % span_class
        if url:
            span += '<a href="%s">' % url
        span += name
        if url:
            span += '</a>'
        span += '</span>'
        return span

    def html_for_single_tag(self, tags_ref):
        tag_ref = tags_ref[0]
        html = self.format_span(tag_ref['name'], tag_ref['url'], 1)
        return "<div id='htmltagcloud'>%s</div>" % html

    def html_for_multiple_tags(self, tags_ref):
        html = ""
        for tag in tags_ref:
            span = self.format_span(tag['name'], tag['url'], tag['level'])
            html += "%s\n" % span
        return html

    def html_for(self, tags_ref):
        ntags = len(tags_ref)
        if ntags == 0:
            return ""
        if ntags == 1:
            return self.html_for_single_tag(tags_ref)
        return self.html_for_multiple_tags(tags_ref)

    def html_without_categories(self, shuffle, limit):
        html = self.html_for(self.tags(shuffle, limit))
        return html

    def html(self, shuffle=False, limit=None):
        html = self.html_without_categories(shuffle, limit)
        return html

    def html_and_css(self, shuffle=False, limit=None):
        """ html(css埋め込み)を返す """
        html = "<style type='text/css'>%s</style>\n" % self.css()
        html += self.html(shuffle, limit)
        return html
