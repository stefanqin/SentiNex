#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import json
from abc_scraper import SentimentAnalyser
from pprint import pprint

API_KEY = "dd489551-a005-42a3-988d-7c59b3ad47da"


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
    def addComment(self, report, text):
    	fileName = self.getLatestComment(report)
    	with open(str(self.base + report + "/comments/" + str(fileName)), 'w+') as f:
    		f.write()






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
    sa = SentimentAnalyser(API_KEY)
    reportAnalysis = []

    releases = db.getReleases()
    num = 1
    for r in releases:
        analysis = Analysis()
        for c in db.getComments(r):
            print(c)
            response = sa.text_sentiment(c)
            with open('sample.txt', 'w+') as f:
            	f.write(json.dumps(response, ensure_ascii=False))
            analysis.addComment(response)
         # for a in db.getArticles(r):
         #     response = sa.text_sentiment(a)
         #   analysis.addArticle(response)

        analysis.addText(sa.text_sentiment(db.getRelease(r)))
        reportAnalysis.append(analysis)
        print(num)
        num += 1
    for r in reportAnalysis:
        pprint(r)
    pprint(reportAnalysis[0].comments)
    print('#'*20)
    pprint(reportAnalysis[0].text)

if __name__ == '__main__':
    main()
