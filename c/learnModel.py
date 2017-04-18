
### Reference : http://www.nltk.org/book/ch02.html

# from sklearn.linear_model import LinearRegression, LogisticRegression
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.naive_bayes import GaussianNB

import numpy as np
# import pandas as pd
import pickle

import nltk
import re
from nltk.book import *
from buildWordDictionary import buildWordDictionary

##### Train HMM, brute-force method by simply counting the tags
# supervised-learning type training
def train_HMM_bruteForce():

    ### First, Build word dictionary
    buildWordDictionary()


    ### Load training data from available corpus
    print "...Loading training data from chosen corpus..."
    # list(text) of list(sentence) structure
    train1 = nltk.corpus.brown.tagged_sents(tagset='universal')
    train2 = nltk.corpus.nps_chat.tagged_posts(tagset='universal')
    train3 = nltk.corpus.treebank.tagged_sents(tagset='universal')

    train = train1+train2+train3
    length = len(train)


    ### Load tag, word dictionary
    print "...Loading tag & word dictionary..."
    tagList = load_dictionary('tag_univ')
    wordList = load_dictionary('word_univ')
    num_tag_univ = len(tagList)
    num_word_univ = len(wordList)


    ### Initialize matrices of parameters
    prob_tag = np.zeros((1,num_tag_univ))
    prob_word_given_tag = np.zeros((num_word_univ, num_tag_univ))
    prob_transition = np.zeros((num_tag_univ, num_tag_univ))


    ### Training
    print "...Training..."
    # Training method 1 : Sentece by Sentence training
    # (sentences are explicitly differentiated by "."
    # Each train[i] is a (tagged) sentence, given by (word, tag) list
    for i in xrange(0,length):
        first_word = True
        for (word, tag) in train[i]:

            tag_idx_curr = tagList[tag]
            try:
                word_idx = wordList[word]
            except(KeyError):
                word_idx = num_word_univ - 1

            if first_word:
                prob_tag[0, tag_idx_curr] += 1
                prob_word_given_tag[word_idx, tag_idx_curr] += 1
                first_word = False
            else:
                prob_word_given_tag[word_idx, tag_idx_curr] += 1
                prob_transition[tag_idx_curr, tag_idx_prev] += 1

            tag_idx_prev = tag_idx_curr


    # Training method 2 : 2 Setences training((1,2),(3,4),(5,6)...)
    # (sentences differentiated by "." are combined,
    # because web text sometimes doesn't specify "." for each sentence

    # Training method 3 : 2 Setences training((2,3),(4,5),(6,7)...)


    ### Make probability distribtion by normalization
    N = np.sum(prob_tag, axis=1)
    prob_tag = np.divide(prob_tag, N)

    N = np.asarray(np.asmatrix(np.sum(prob_word_given_tag, axis=0)))
    prob_word_given_tag = np.divide(prob_word_given_tag, N)

    N = np.asarray(np.asmatrix(np.sum(prob_transition, axis=0)))
    prob_transition = np.divide(prob_transition, N)


    ### Save the parameter matrices as txt file
    print "Saving the parameters into text files..."
    save_param(prob_tag, 'prob_tag')
    save_param(prob_word_given_tag, 'prob_word_given_tag')
    save_param(prob_transition, 'prob_transition')

    return [prob_tag, prob_word_given_tag, prob_transition]


##### Train HMM, Expectation-Maximization method, iteration required
# unsupervised-learning type training
# Reference : http://www.cs.ubc.ca/~murphyk/Bayes/rabiner.pdf
def train_HMM_EM():

    ### Threshold for the termination of iteration
    threshold = 1e-8

    ### First, Build word dictionary
    buildWordDictionary()

    ### Load tag, word dictionary
    print "...Loading tag & word dictionary..."
    tagList = load_dictionary('tag_univ')
    wordList = load_dictionary('word_univ')
    num_tag_univ = len(tagList)
    num_word_univ = len(wordList)

    ### Initialize matrices of parameters, using brute force estimation
    [prob_tag, prob_word_given_tag, prob_transition] =train_HMM_bruteForce()







def load_dictionary(filename):
    tagList = {}
    idx_count = 0
    with open('./resources/'+filename+'.txt', 'r') as f:
        for line in f:
            tagList.update({line.rstrip('\n'):idx_count})
            idx_count += 1
    return tagList


def save_param(data, filename):
    np.savetxt('./resources/'+filename+'.txt', data, delimiter=' ', fmt = '%.9f')
    return


def train_KeywordExtractor():
    pass


def train_SentimentAnalyzer():
    pass


### Reference : http://stackoverflow.com/questions/10017086/save-naive-bayes-trained-classifier-in-nltk


def save_Classifier():

    f = open('my_classifier_learned', 'wb')
    pickle.dump(classifier, f)
    f.close()

def load_Classifier():
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

if __name__ == "__main__":
    train_HMM()