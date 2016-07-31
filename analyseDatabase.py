#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import requests

from abc_scraper import gen_params, SentimentAnalyser
from pprint import pprint

params = gen_params()


class FileDatabase:
    def __init__(self):
        self.base = "database/"

    def getReleases(self):
        r = []
        for f in os.listdir(self.base):
            if re.match('^\.', f):
                continue
            r.append(f)
        return r

    def getRelease(self, name):
        lines = []
        with open(self.base + name + "/" + "release.txt", 'r+') as f:
            lines = f.readlines()
        return ''.join(lines)

    def getArticles(self, name):
        r = []
        for f in os.listdir(self.base + name + "/articles/"):
            if re.match('^\.', f):
                continue
            with open(self.base + name + "/articles/" + f, 'r+') as f:
                lines = f.readlines()
            r.append(''.join(lines))
        return r

    def getComments(self, name):
        r = []
        for f in os.listdir(self.base + name + "/comments/"):
            if re.match('^\.', f):
                continue
            with open(self.base + name + "/comments/" + f, 'r+') as f:
                for l in f.readlines():
                    r.append(l)
        return r


class Analysis:
    def __init__(self):
        self.comments = []
        self.text = []
        self.articles = []

    def addComment(self, a):
        self.comments.append(a)

    def addArticle(self, a):
        self.articles.append(a)

    def addText(self, a):
        self.text.append(a)


def main():
    db = FileDatabase()
    sa = SentimentAnalyser(HPE_api_key=params['HavenOnDemand']['api_key'],
                           IBM_api_key=params['Watson']['api_key'],
                           sent_used='IBM')
    reportAnalysis = []

    releases = db.getReleases()
    num = 1
    for r in releases:
        analysis = Analysis()
        num_comments = 1
        for c in db.getComments(r):
            print('COMMENT_NUM:', num_comments)
            if num_comments <= 5:
                try:
                    response = sa.text_sentiment(c)
                    analysis.addComment(response)
                except requests.exceptions.ConnectionError:
                    print('TIMEOUT:', num_comments)
                    num_comments += 1
                    continue
                num_comments += 1
            else:
                break
        for a in db.getArticles(r):
            response = sa.text_sentiment(a)
            analysis.addArticle(response)

        analysis.addText(sa.text_sentiment(db.getRelease(r)))
        reportAnalysis.append(analysis)
        print(num)
        num += 1
    for r in reportAnalysis:
        pprint(r)
    pprint(reportAnalysis[0].comments)
    print('#'*20)
    pprint(reportAnalysis[0].text)
    sent.output_json(sentiment, 'ABC_sent.json')

if __name__ == '__main__':
    main()
