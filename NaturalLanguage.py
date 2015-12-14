# 
# 
# Copyright: Douglas Franklin 
# Organization: Northeastern University
#
#
#  /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# - Natural Language Processing to Detect Potentially Violent Offenders -
#  \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#
# ----------------------------------------------------------------------
# NOTE: MUST USE PYTHON 3 OR LATER (Tested on Python 3.4.3)!!!!!!
import sys
import tfidf
import json
import terms
import math
import argparse
import fileParser
from argparse import RawTextHelpFormatter
from textblob import TextBlob as tb
import pdb

class BlogObject: # Analysis Object that is returned by the analysis function, which allows all relevant data to stay together. 
    def __init__(self, post, author = "", title = ""):
        self.author = author
        self.title = title
        self.post = post

class AnalysisObject: # Analysis Object that is returned by the analysis function, which allows all relevant data to stay together. 
    def __init__(self, namesScore = 0, religionScore = 0, weaponryScore = 0, governmentScore = 0, outputsWordsArray = 0):
        self.outputsWordsArray = outputsWordsArray
        self.namesScore = namesScore
        self.religionScore = religionScore
        self.weaponryScore = weaponryScore
        self.governmentScore = governmentScore
        
def importJSON(inFile):
	with open(inFile) as json_file:
		json_data = json.load(json_file)
		return json_data

def analyzeBlogs(blogList): # Analyze blog with tfidf, and other word analysis. 
    outputWordsArr  = []
    namesCount, religionCount, weaponryCount, governmentCount, wordCount = 0, 0, 0, 0, 0
    for i, blog in enumerate(blogList):
        scores = {}
        wordCount = 0
        print("Top words in document {}".format(i + 1))
        for word in blog.words:
            flag = True
            word = word.lower() # Everything is in lowercase. 
            for punc in terms.punctuation():
                if punc in word:
                    flag = False
            wordCount+=1
            if flag:  
                scores[word] = tfidf.tfidf(word, blog, blogList) # run tfidf
                if word in terms.governmentTerms(): # increment count based on content to find word densities. 
                    governmentCount+=1
                if word in terms.weaponsTerms():
                    weaponryCount+=1
                if word in terms.femaleNames() or word in terms.maleNames():
                    namesCount+=1
                if word in terms.religiousTerms():
                    religionCount+=1
                sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) # sort the words
        for word, score in sorted_words[0:10]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            outputWordsArr.append((word, round(score, 10)))
        print("---------------------------------------------------------")
    # Gathering the density scores of each of these defined features, and creating the returning data type
    analysisOutputs = AnalysisObject(namesCount/wordCount,religionCount/wordCount,weaponryCount/wordCount,governmentCount/wordCount,outputWordsArr)
    return analysisOutputs

def applyWeights(features, weightedFeatures): # Apply weights to the scores in the features object. 
    # Check if a word that is part of the different terms and also in the top-words list. That increases its weight.
    weights = {"names": 2.0, "religion": 5.0, "weaponry": 8.0, "government": 15.0}
    for upperKey in features:
        for lowerKey in features[upperKey]:
            if lowerKey != "words":
                weightedFeatures[upperKey][lowerKey] = features[upperKey][lowerKey] * weights[lowerKey]
    # pdb.set_trace()
    return weightedFeatures

def analyzeNewBlog(blog, goodBlogList, badBlogList, features):
    # Get word densities of the new blog
    namesCount, religionCount, weaponryCount, governmentCount, wordCount = 0, 0, 0, 0, 0
    for word in tb(blog):
        wordCount += 1
        if word in terms.governmentTerms(): # increment count based on content to find word densities. 
            governmentCount += 1
        if word in terms.weaponsTerms():
            weaponryCount += 1
        if word in terms.femaleNames() or word in terms.maleNames():
            namesCount += 1
        if word in terms.religiousTerms():
            religionCount += 1
    analysisOutputs = AnalysisObject(namesCount/wordCount,religionCount/wordCount,weaponryCount/wordCount,governmentCount/wordCount, None)
   
   # Compare to the analyzed ones.
    scores = {"good": 0.0, "bad": 0.0}
    for upperKey in features:
        print ("\nComparing this blog to " + upperKey.upper() + " blogs:\n")
        for lowerKey in features[upperKey]:
            if lowerKey == "words":
                for word in features[upperKey][lowerKey]:
                    if word[0] not in terms.stopWords():
                        if word[0] in blog:
                            print ("Word found in " + upperKey + " blog: " + word[0])
                            scores[upperKey] += word[1] * 100 # If a word is found, update the score relative to its TFIDF score. 
            elif lowerKey == "religion": # This next section is to compare the density of a term of the new blog compared to the density of that term in the analyzed blogs. 
                scores[upperKey] -= abs(features[upperKey][lowerKey] - analysisOutputs.religionScore)
                print ("Religion variance: " + str(features[upperKey][lowerKey] - analysisOutputs.religionScore))
            elif lowerKey == "government":
                scores[upperKey] -= abs(features[upperKey][lowerKey] - analysisOutputs.governmentScore)
                print ("Government variance: " + str(abs(features[upperKey][lowerKey] - analysisOutputs.governmentScore)))
            elif lowerKey == "weaponry":
                scores[upperKey] -= abs(features[upperKey][lowerKey] - analysisOutputs.weaponryScore)
                print ("Weaponry variance: " + str(abs(features[upperKey][lowerKey] - analysisOutputs.weaponryScore)))
            elif lowerKey == "names":
                scores[upperKey] -= abs(features[upperKey][lowerKey] - analysisOutputs.namesScore)
                print ("Names variance: " + str(abs(features[upperKey][lowerKey] - analysisOutputs.namesScore)))
    print ("\nFinal Scores:\n" + "Bad: " + str(scores["bad"]) + "\nGood: " + str(scores["good"]) + "\n")
    if abs(scores["good"] - scores["bad"]) < .5:
        print ("This post does not trend towards 'good; or 'bad'.")
    else:
        if scores["good"] > scores["bad"]:
            print ("This post has been marked as 'good'.")
            goodBlogList.append(tb(blog)) # Add term to the blog list. If this program were running constantly, it would be included in the next baes analysis.
        else: 
            print ("This post has been flagged as 'bad'.")
            badBlogList.append(tb(blog))
    print ("\n---------------------------------------")

def buildNewBlog(blogFile = None, blogAuthor = "", blogTitle = "", blogText = None): # Returns an analyzable object
    newBlog = None
    if blogFile != None:
        if blogText != None:
            print ("[warn] Both commandline and file blogs were found, prioritizing for use of the file")
        newBlog = fileParser.getBlog(blogFile)
    elif blogText != None:
        # build JSON object via blogTitle, blogAuthor, and blogText
        newBlog = BlogObject(blogText, blogAuthor, blogTitle)
    else:
        print ("[err] Error in creating new blog object...")
        return False
    return newBlog

# def analyzeNewBlog(blog):


# Builds the new blog post based on the entry (commandline or txt file)
def main():
    # Takes in commandLine args, and sorts variables if necessary. 
    parser = argparse.ArgumentParser(description='Analyze Blogs.', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-b', '--blog', help='Manually enter the blog text here as a string. Formatted like:\n\nauthor: "authors name"\ntitle: "title"\nblog: "blog text"', default=None)
    parser.add_argument('-a', '--author', help='Enter the authors name as a string', default=None)
    parser.add_argument('-t', '--title', help='Enter the blogs title as a string', default=None)
    parser.add_argument('-i', '--inFile', help='Enter the path to a plain text file with the blog entry in it', default=None)
    args = parser.parse_args()

    # Save variables from commandline args
    newBlogFile = args.inFile
    newBlogText = args.blog
    newBlogAuthor = args.author
    newBlogTitle = args.title
    go = True
    while(go):    
        # The below object is a dictionary of 2 dictionaries, good and bad features, and their relevant metadata. 
        # count is the number of times blogs have been passed through. This is necessary for updates.
        features = {"good":{"count": 0, "words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}, "bad": {"count": 0, "words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}}
        
        json_data = importJSON("Writings/writings.json") # get JSON data, creating a dictionary-like object 
        
        # Declaring lists of writings
        badBlogList = []
        goodBlogList = []
        
        # Analyze the current data in the JSON file. 
        for blog in json_data["writings"]["bad"]:
        	badBlogList.append(tb(blog["post"]))
        for blog in json_data["writings"]["good"]:
        	goodBlogList.append(tb(blog["post"]))
        analysisResults = analyzeBlogs(badBlogList)
        features["bad"]["count"], features["bad"]["words"], features["bad"]["names"], features["bad"]["religion"], features["bad"]["weaponry"], features["bad"]["government"] = len(badBlogList), analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
        analysisResults = analyzeBlogs(goodBlogList)
        features["good"]["count"], features["good"]["words"], features["good"]["names"], features["good"]["religion"], features["good"]["weaponry"], features["good"]["government"] = len(goodBlogList), analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
    
        print("Current writings in database have been analyzed... \nRunning comparisons against provided writing...\n ----------------------------")
        
        newBlog = None
        # Analyze new file
        if newBlogFile is not None:
            newBlog = buildNewBlog(newBlogFile)
        elif newBlogText is not None:
            newBlog = buildNewBlog(None, newBlogAuthor, newBlogTitle, newBlogText)
        
        if newBlog is not None:
            tempFeatures = {"words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}
            analyzeNewBlog(newBlog.post, goodBlogList, badBlogList, features)

        print ("Please enter another file for analysis. or 'quit' to quit.\n")
        newBlogFile = input('File path: ')
        if newBlogFile == "quit" or newBlogFile == "Quit" or newBlogFile == "q":
            go = False
    
    print("Closing program...")
    # pdb.set_trace() # End, check on debug. 
if __name__ == "__main__": main()

