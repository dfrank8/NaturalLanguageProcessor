# from __future__ import division, unicode_literals

import sys
import tfidf
import json
import stopWords
from textblob import TextBlob as tb
import pdb

def importJSON(inFile):
	with open(inFile) as json_file:
		json_data = json.load(json_file)
		return json_data

# Can be queried with json_data["writings"]["good"][0]["post"]

json_data = importJSON("Writings/writings.json")

badBlog1 = tb(json_data["writings"]["bad"][0]["post"])
badBlog2 = tb(json_data["writings"]["bad"][1]["post"])
badBlog3 = tb(json_data["writings"]["bad"][2]["post"])

bloglist = [badBlog1, badBlog2, badBlog3]
# pdb.set_trace()
for i, blog in enumerate(bloglist):
    print("Top words in document {}".format(i + 1))
    for word in blog.words:
    	if word not in stopWords.stopWords():
    		scores = {word: tfidf.tfidf(word, blog, bloglist)}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))