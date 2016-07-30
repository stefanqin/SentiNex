#!bin/env/python3
# -*- coding: utf-8 -*-
# Scrapes articles from the ABC dataset and analyses collective sentiment.

"""
TODO:
    Exception handling.
    multiprocessing

Notes:
    We use REST API queries over a hard-copy CSV file as it contains more
    information.
"""

from configparser import ConfigParser
from collections import defaultdict
from pprint import pprint
from multiprocessing import Pool

import json
import requests
import csv
import sys

class ArticleGatherer:
    """Collects all articles related to a given topic."""
    def __init__(self, url: str, api_version: str, csv_file: str,
                 topics: dict, selection: dict, method: str = 'NUM' ) -> None:
        """
        Initialises an Article Gathering object based on the given parameters.

        Params:
            url: The api url.
            api_version: The api_version.
            csv_file: The name of the csv file to scrape metadata from.
            topics: The topics to cover.
            selection: The relevant parameters to use in conjuction with
                selection method.
            method (optional): The selection method to choose articles from.

        TODO:
            Change method depending on selected params. If method not selected,
                or 'ALL', parse the entirety of the CSV file.
        """
        self.url = url
        self.api_version = api_version
        self.topics = topics
        self.csv_file = csv_file
        self.method = method
        self.article_metadata = 'article_metadata.json'

        # Parameters for choosing articles
        if self.method == 'DATE':
            self.lower_date = selection['lower_date']
            self.upper_date = selection['upper_date']
        elif self.method == 'NUM':
            self.num = int(selection['num_articles'])
        elif self.method == 'ALL':
            NotImplemented
        else:
            # Raise an exception.
            NotImplemented

        # Create a persistent connection
        self.s = requests.Session()

    def read_csv(self) -> dict:
        """Parse the excel file."""
        row_num = 0
        article = {}
        article_list = []

        with open(self.csv_file, newline='') as csvfile:
            metadata = csv.DictReader(csvfile, dialect='excel')
            for row in metadata:
                # Skip headers
                if self.method == 'NUM':
                    if row_num >= 1 and row_num <= self.num:
                        # print(row_num, row)
                        article_list.append({
                            'dt_hour': row['dt_hour'],
                            'contentid': row['contentid'],
                            'traffic': row['traffic']
                        })
                row_num += 1
            # pprint(article_list)

        return article_list

    def save_to_file(self, article_list: str) -> None:
        """Writes a given article list to a file for easy access.

        Params:
            article_id: The article to analyse.
        """
        # We must define a dictionary as JSON requires initial field to be a
        # dict.
        article_metadata = {'list':[]}
        with open(self.article_metadata, 'w') as f:
            for article in article_list:
                article_url = self.url + self.api_version + \
                    '/{!s}'.format(article['contentid'])
                r = requests.get(article_url)
                content = r.json()
                article_metadata['list'].append(content)
            json.dump(article_metadata, f, indent=1)

    def relevant_articles(self, article_list: dict) -> dict:
        """Get a list of the relevant articles."""
        # ot_articles = on_topic_articles
        ot_articles = defaultdict(list)

        with open(self.article_metadata, 'r') as f:
            article_list = json.load(f)

            for topic in self.topics:
                for article in article_list['list']:
                    if self.on_topic(article, topic):
                        ot_articles[topic].append(article['title'])
            pprint(ot_articles)

    def on_topic(self, article: dict, topic: str):
        """Determine whether an article is on topic.

        Params:
            article: The article to analyse.
            topic: The topic to search for.
        """
        keywords = []

        unformatted_keywords = article['keywords'].split(',')
        for word in unformatted_keywords:
            keywords.append(word.strip().lower())

        topic_keywords = self.topics[topic].split(',')
        intersect = list(set(keywords) & set(topic_keywords))

        # Change depending on relevance.
        if len(intersect) > 2:
            print(article['title'])
            return True
        return False

    def find_content(self):
        """Get the content of the specified articles.

        Note:
            Since there are a large number of articles, we get the content, and
                then analyse. The alternative is to first store all the content,
                however this may lead to a very large file size and unintended
                result.
        """
        NotImplemented


class SentimentAnalysis:
    """Analyses collective sentiment of the given articles."""
    NotImplemented

def gen_params() -> dict:
    """Generate params based on .ini file."""
    params = defaultdict(lambda: defaultdict(dict))
    config = ConfigParser()
    config.read('params.ini')

    for section in config.sections():
        for key in config[section]:
            params[section][key] = config[section][key]

    return params

def main():

    params = gen_params()
    articles = ArticleGatherer(
        url=params['General']['url'],
        api_version=params['General']['api_version'],
        csv_file=params['General']['csv_file'],
        topics=params['Topics'],
        selection=params['Selection'],
        method=params['Selection']['method']
    )
    chosen = articles.read_csv()
    try:
        if sys.argv[1] == '-s':
            print('SAVING ARTICLES...')
            articles.save_to_file(chosen)
    except IndexError:
        pass

    articles.relevant_articles(chosen)

if __name__ == '__main__':
    main()