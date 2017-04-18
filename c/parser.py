
from nltk import word_tokenize

def tokenize(tweet):
    tweet = tweet.lower()
    token = word_tokenize(tweet)
    return token