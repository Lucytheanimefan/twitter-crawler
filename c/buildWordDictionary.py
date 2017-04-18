
### Reference : http://www.nltk.org/book/ch02.html

import nltk
import re
# from nltk.book import *

##### Build word dictionary
def buildWordDictionary():

    # natural word
    word_list1 = set(w.lower() for w in nltk.corpus.brown.words())
    # word from web
    word_list2 = set(w.lower() for w in nltk.corpus.webtext.words())
    # union of those two sets
    word_list = sorted(word_list1.union(word_list2))

    # remove all the words that contains non-alphabet letters
    word_list_trim = []
    for word in word_list:
        temp = trim(word)
        if len(temp)!=len(word):
            continue
        else:
            word_list_trim.append(temp)

    # Special mark
    word_list_mark = ["$", "A$", "C$", "HK$", "M$", "NZ$", "S$", "U.S.$", "US$",
                      "'", "''", "(", "[", "{", ")", "]", "}", ",", "--", ".", "!", "?",
                      ":", ";", "...", "&",
                      "%", "*", "+", "<", "=", ">", "@", "A[fj]", "U.S", "U.S.S.R", "*", "**", "***",
                      "`", "``"]
    # Name of entities fall into this category
    word_ENTITY = ["__ENTITY"]

    # Total word list
    word_list_trim = word_list_trim + word_list_mark + word_ENTITY

    # Write word list as txt file
    with open('./resources/word_univ.txt', 'w') as f:
        num_word_univ = len(word_list_trim)
        for i in xrange(0,num_word_univ):
            if i!=(num_word_univ-1):
                f.write(word_list_trim[i]+'\n')
            else:
                f.write(word_list_trim[i])


def trim(word):

    trimmed = re.sub(r'[^a-zA-Z]', '', word)
    trimmed.strip()

    return trimmed


if __name__ == "__main__":
    buildWordDictionary()