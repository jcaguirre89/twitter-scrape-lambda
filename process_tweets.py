import re
import string
import unicodedata
import requests

STOPWORDS = requests.get(
    'https://raw.githubusercontent.com/stopwords-iso/stopwords-es/master/raw/node-stopwords-spanish.txt'
).content.decode('utf-8-sig').split('\n')

ENGLISH_STOPWORDS = requests.get(
    "https://gist.githubusercontent.com/sebleier/554280/raw/7e0e4a1ce04c2bb7bd41089c9821dbcf6d0c786c/NLTK's%2520list%2520of%2520english%2520stopwords"
).content.decode('utf-8').split('\n')

MORE_STOPWORDS = [
    '',
    'y',
    'si',
    'no',
    'q',
    'd',
    'ud',
    'son',
    'mas',
    'dice',
    'dijo',
    'este',
    'tambien',
    'asi',
    'ahora',
    'ver',
    'tan',
    'sea',
    'han',
    'dijo',
    'tus',
    'vez',
    'hay',
    'im',
    'go',
    'anything',
    'bring',
    'back',
    'lets',
]

STOPWORDS.extend(MORE_STOPWORDS)
STOPWORDS.extend(ENGLISH_STOPWORDS)
STOPWORDS.extend(list('0123456789'))
STOPWORDS.extend(list('qwertyuiopasdfghjklzxcvbnm'))


def main(data):
    """ receives a list of tweets (dicts) and returns a list with the text, removing stop words """
    tweets = []
    for tweet in data:
        if not tweet['is_retweet']:
            tweets.extend(_clean_sentence(tweet))

    return tweets


def _remove_non_ascii(word):
    return unicodedata.normalize('NFKD', word).encode('ascii',
                                                      'ignore').decode(
                                                          'utf-8', 'ignore')


def _remove_emoji(word):
    """ from this SO thread
    https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python """
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', word)


def _clean_word(word):
    """ returns a clean word """
    # Remove URL
    if word.startswith('http'):
        return ''
    word = _remove_emoji(word)
    word = _remove_non_ascii(word)
    word = word.strip().lower()
    # Replace @ (mentions) with __MENTION__
    word = word.replace('@', 'MENTION')
    # Replace # (hashtag) with __HASHTAG__
    word = word.replace('#', 'HASHTAG')
    # Remove punctuation
    word = word.translate(str.maketrans('', '', string.punctuation))
    word = word.replace('MENTION', '@')
    word = word.replace('HASHTAG', '#')
    return word


def _clean_sentence(tweet):
    """ takes a tweet as a dict and returns a list of clean words """
    text = tweet['text'].replace('\n', ' ').split(' ')
    clean = [_clean_word(word) for word in text]
    clean = [word for word in clean if word not in STOPWORDS]

    return clean
