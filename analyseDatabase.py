#!/usr/local/Cellar/python3/3.5.2/bin/python3
import os, sys, re

import sentiment_analyser

API_KEY = "2a54637207d6bc412e628d503bade191d575ae68"

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
	sa = SentimentAnalyser(API_KEY)
	reportAnalysis = []

	releases = db.getReleases()
	for r in releases:
		analysis = Analysis()
		for c in db.getComments(r):
			analysis.addComment(sa.text_sentiment(c))
		for a in db.getArticles(r):
			analysis.addArticle(sa.text_sentiment(a))
		
		analysis.addText(sa.text_sentiment(r.getRelease()))
		reportAnalysis.append(analysis)
	for ra in reportAnalysis:
		print(ra)




if __name__ == '__main__':
	main()