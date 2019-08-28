# -*- coding: utf-8 -*-
import json
import os
import twitter
from get_tweets import main as get_tweets
from process_tweets import main as process_tweets


def handler(event, context):
    """ Main function called by AWS """
    # Make standard headers used by all responses
    standard_headers = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "'OPTIONS,POST'",
            "Content-Type": "application/json",
        },
    }

    # handle development vs production
    if 'httpMethod' in event:
        # Production
        # Handle CORS
        if event['httpMethod'] == 'OPTIONS':
            return dict(statusCode=200,
                        body=json.dumps({'message': 'CORS Allowed'}),
                        **standard_headers)

        # Extract body from event and handle missing data/params
        body = json.loads(event['body'])
        if 'terms' not in body:
            return dict(statusCode=400,
                        body=json.dumps(
                            {'message': 'missing terms in request body'}),
                        **standard_headers)

        lang = body['lang'] if 'lang' in body else None
        max_size = body['max_size'] if 'max_size' in body else 1000
        terms = body['terms']

    else:
        # Development
        terms = event.get('terms')
        lang = event.get('lang', None)
        max_size = 100

    print({'terms': terms, 'lang': lang})

    api_key = (
        os.environ.get('CONSUMER_KEY'),
        os.environ.get('CONSUMER_SECRET'),
        os.environ.get('ACCESS_TOKEN'),
        os.environ.get('ACCESS_TOKEN_SECRET'),
    )

    api = twitter.Api(*api_key,
                      sleep_on_rate_limit=True,
                      tweet_mode='extended')
    data = get_tweets(api, terms, lang=lang, max_size=max_size)

    output = process_tweets(data)

    # Remove words in terms from response
    test_terms = [word.strip().lower() for word in terms.split(',')]
    test_terms.extend([f'#{word}' for word in test_terms])
    output = [word for word in output if word not in test_terms]

    return dict(statusCode=200, body=json.dumps(output), **standard_headers)
