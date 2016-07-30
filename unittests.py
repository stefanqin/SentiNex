#!/bin/env/python3
# -*- coding: utf-8 -*-
# Test suite for the abc_scraper module

from abc_scraper import gen_params, ArticleGatherer, SentimentAnalysis
from pprint import pprint
import json


def main():

    with open('test_text.txt', 'r') as f:
        text = f.read()

    params = gen_params()
    """
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
    """
    sent = SentimentAnalysis(
        api_key=params['Watson']['api_key']
    )
    pprint(sent.text_sentiment(text))

if __name__ == '__main__':
    main()
