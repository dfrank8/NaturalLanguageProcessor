# from __future__ import division, unicode_literals
import sys
import tfidf
import json
import Terms.terms
from textblob import TextBlob as tb
import pdb

def importJSON(inFile):
	with open(inFile) as json_file:
		json_data = json.load(json_file)
		return json_data

# Can be queried with json_data["writings"]["good"][0]["post"]

json_data = importJSON("Writings/writings.json")
badBlogList = []
goodBlogList = []

# badBlog1 = tb(json_data["writings"]["bad"][0]["post"])
# badBlog2 = tb(json_data["writings"]["bad"][1]["post"])
# badBlog3 = tb(json_data["writings"]["bad"][2]["post"])

# goodBlog1 = tb(json_data["writings"]["good"][0]["post"])
# goodBlog2 = tb(json_data["writings"]["good"][1]["post"])
# goodBlog3 = tb(json_data["writings"]["good"][2]["post"])

for blog in json_data["writings"]["bad"]:
	badBlogList.append(tb(blog["post"]))
for blog in json_data["writings"]["good"]:
	goodBlogList.append(tb(blog["post"]))
# pdb.set_trace()

# Do bad blogs tfidf
for i, blog in enumerate(badBlogList):
    print("Top words in document {}".format(i + 1))
    for word in blog.words:
    	if word not in terms.stopWords():
    		scores = {word: tfidf.tfidf(word, blog, badBlogList)}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

print("---------------------------------------------------------")
# Do good blogs tfidf
for i, blog in enumerate(goodBlogList):
    print("Top words in document {}".format(i + 1))
    for word in blog.words:
    	if word not in stopWords.stopWords():
    		scores = {word: tfidf.tfidf(word, blog, goodBlogList)}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))