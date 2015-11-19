import sys
import math

# These are the basic functions for tf-idf, assigning weights to words at they appear in a writing. 
# http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/

'''
tf(word, blob) computes "term frequency" which is the number of 
times a word appears in a document blob, normalized by dividing by the 
total number of words in blob. We use TextBlob for breaking up the text into words and getting the word counts.
'''
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

'''
n_containing returns the number of documents containing word. 
A generator expression is passed to the sum() function.
'''
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

'''idf(word, bloblist) computes "inverse document frequency" which measures 
how common a word is among all documents in bloblist. The more common 
a word is, the lower its idf. We take the ratio of the total number of 
documents to the number of documents containing word, then take the log of 
that. Add 1 to the divisor to prevent division by zero. Words like "the" and "for" will
be filtered out by this function as non-unique identifiers. 
'''
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

'''
tfidf(word, blob, bloblist) computes the TF-IDF score. 
It is simply the product of tf and idf.
'''
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


# Testing documents:

