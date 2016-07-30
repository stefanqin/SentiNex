#!bin/env/python3
# -*- coding: utf-8 -*-
# Wrapper for sentiment analysis of a given text.

from pprint import pprint
from havenondemand.hodclient import *
from abc_scraper import gen_params

import time


class SentimentAnalyser:
    """Sentiment analysis using the haven on demand API."""

    def __init__(self, api_key, version='v1'):
        self.client = HODClient(apikey=api_key, version=version)

    def text_sentiment(self, text, func=None, **kwargs):
        """Analyses the sentiment of a given text.

        Params:
            text: The text to analyse.
        """
        response_async = self.client.post_request({'text': text}, HODApps.ANALYZE_SENTIMENT,
                                      async=True)
        jobID = response_async['jobID']

        response = self.client.get_job_status(jobID, callback=func, **kwargs)
        while not response:
            response = self.client.get_job_status(jobID, callback=func, **kwargs)

        return response


def main():

    with open('test_text.txt', 'r') as f:
        text = f.read()

    params = gen_params()
    sent = SentimentAnalyser(api_key=params['HavenOnDemand']['api_key'])
    sentiment = sent.text_sentiment(text)

    pprint(sentiment)

if __name__ == '__main__':
    main()
