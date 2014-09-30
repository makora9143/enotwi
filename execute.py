#! /usr/bin/env/ python
# -*-encoding: utf-8 -*-

"""

"""

from tagcloud import TagCloud
from mecabhelper import MecabHelpler
from parsejson import ParseJson


def main():
    parsejson = ParseJson()
    texts = parsejson.load_all_json()

    mecabhelper = MecabHelpler()
    mecabhelper.replace_texts(texts)
    mecabhelper.count_words()
    results = mecabhelper.get_result()

    cloud = TagCloud()
    for word, count in results.items():
        cloud.add_static(word, count)

    print cloud.html_and_css(shuffle=True)


if __name__ == '__main__':
    main()
