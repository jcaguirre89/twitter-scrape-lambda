# -*- coding: utf-8 -*-
from collections import namedtuple
import json
import twitter

Tweet = namedtuple('Tweet', [
    'date', 'timestamp', 'id', 'text', 'user_handle', 'user_id',
    'followers_count', 'favorite_count', 'retweet_count', 'is_retweet', 'city',
    'country'
])


def get_tweets(api, start_id, parameters):
    """
    A generator that fetches all tweets with the given parameters, starting
    from the latest one and going back until the `start_id` is reached.


    :param start_id: `int`. A Twitter ID that marks the oldest tweet to fetch. The open Twitter
    search API only returns up to around a week of history
    :param parameters: a dictionary with parameters that will be given to the `GetSearch` method of
    the `python-twitter` library. Must include at least one of the following keys: `term`, `geocode`,
    or `raw_query`.
    :return: yields a namedtuple corresponding to a tweet.
    """
    start_id = int(start_id)
    latest_tweets = api.GetSearch(**parameters)
    if not latest_tweets:
        return []
    last_id = latest_tweets[-1].id
    for tweet in latest_tweets:
        yield tweet

    while last_id >= start_id:
        parameters['max_id'] = last_id - 1
        results = api.GetSearch(**parameters)
        if len(results):
            for tweet in results:
                yield tweet
            last_id = results[-1].id
            print(f'last seen: {last_id} @ {results[-1].created_at}')
        else:
            break


def main(api,
         comma_sep_terms,
         lang='en',
         start_id='1064630780150239238',
         max_size=1000):
    """
    Run the get_tweets generator and return as a list of dicts
    """

    # Build parameters dict
    parameters = {
        'term': _build_search_term(comma_sep_terms),
        'count': 100,
        'include_entities': False,
        'lang': lang,
    }

    # Return will be an array of dicts
    output = []
    for tweet in get_tweets(api, start_id, parameters):
        tweet_record = _process_tweet(tweet)
        output.append(tweet_record)
        # Only return given number of latest tweets
        if len(output) > max_size:
            return output

    return output


def _build_search_term(comma_sep_terms):
    """
    Takes a string of comma-separated terms to be searched
    and returns it as one string as the API expects it
    """
    entries = comma_sep_terms.split(',')
    if len(entries) == 1:
        # Single term to search
        return entries[0]
    return ' OR '.join(entries)


def _process_tweet(tweet):
    """ Receives a Tweet from the Search API and processes it """

    text = tweet.full_text.replace('\n', ' ')
    is_retweet = True if text.startswith('RT') else False
    try:
        city = tweet.place['name']
        country = tweet.place['country']
    except TypeError:
        city = None
        country = None

    tweet_instance = Tweet(tweet.created_at, tweet.created_at_in_seconds,
                           tweet.id, tweet.full_text, tweet.user.screen_name,
                           tweet.user.id, tweet.user.followers_count,
                           tweet.favorite_count, tweet.retweet_count,
                           is_retweet, city, country)

    return dict(tweet_instance._asdict())
