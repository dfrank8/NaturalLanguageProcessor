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
        for word, score in sorted_words[0:5]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            outputWordsArr.append((word, round(score, 5)))
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
    # dictionaries are mutable, so this method will update features
    # run analyze blogs as if the new blog was in both, whichever feature is LESS significantly changed, it probably belongs in that one
    varianceScores = {"good": 0.0, "bad": 0.0} # The new entry is analyzed as if it was amongst both parties, which ever one it had the bigger effect on changing, it belongs to the other. 
    goodBlogList.append(tb(blog))
    badBlogList.append(tb(blog))

    featuresAfter = {"good":{"words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}, "bad": {"words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}}
    analysisResults = analyzeBlogs(goodBlogList)
    featuresAfter["good"]["words"], featuresAfter["good"]["names"], featuresAfter["good"]["religion"], featuresAfter["good"]["weaponry"], featuresAfter["good"]["government"] = analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
    analysisResults = analyzeBlogs(badBlogList)
    featuresAfter["bad"]["words"], featuresAfter["bad"]["names"], featuresAfter["bad"]["religion"], featuresAfter["bad"]["weaponry"], featuresAfter["bad"]["government"] = analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore

    for upperKey in featuresAfter:
        total = 0.0
        featureCount = 0 
        for lowerKey in featuresAfter[upperKey]:
            if lowerKey == "words":
                if featuresAfter[upperKey][lowerKey][-5:-1] in features[upperKey][lowerKey]: # This means that the new words were apparent in previous posts
                    varianceScores[upperKey] += 1/len(features[upperKey][lowerKey])
            else:
                varianceScores[upperKey] += featuresAfter[upperKey][lowerKey]/features[upperKey][lowerKey]
            featureCount += 1
        varianceScores[upperKey] /= featureCount

    pdb.set_trace()
    if varianceScores["good"] > varianceScores["bad"]:
        del badBlogList[-1]
        print("This blog has some aspects commonly seen in other writings made by bad people...")
    else:
        del goodBlogList[-1]
        print("This blog is likely written by person who poses no threat to others")

    # Clean up some memory space. 
    del featuresAfter
    del analysisResults



# def updateFeatures(feature, newFeatures):
    # update good and bad features depending on the decision by the alogrithm of which class it falls under.

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
    
    # The below object is a dictionary of 2 dictionaries, good and bad features, and their relevant metadata. 
    # count is the number of times blogs have been passed through. This is necessary for updates.
    features = {"good":{"count": 0, "words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}, "bad": {"count": 0, "words": [], "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}}
    
    # Weighted features are kept in a separate objects since they are highly readable and more interesting to the user. 
    # The metadata from features is applied to weighteFeatures after being multiplied by their respective weights. 
    # Notice that words are ommitted from this object since the words cannot hold weight (since they are words, not numbers)
    # weightedFeatures = {"good":{"names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}, "bad": {"names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}}
    
    json_data = importJSON("Writings/writings.json") # get JSON data, creating a dictionary-like object 
    
    # Declaring lists of writings
    badBlogList = []
    goodBlogList = []
    
    # Analyze the current data in the JSON file. 
    for blog in json_data["writings"]["bad"]:
    	badBlogList.append(tb(blog["post"]))
    for blog in json_data["writings"]["good"]:
    	goodBlogList.append(tb(blog["post"]))

    
    pdb.set_trace()
    analysisResults = analyzeBlogs(badBlogList)
    features["bad"]["count"], features["bad"]["words"], features["bad"]["names"], features["bad"]["religion"], features["bad"]["weaponry"], features["bad"]["government"] = len(badBlogList), analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
    analysisResults = analyzeBlogs(goodBlogList)
    features["good"]["count"], features["good"]["words"], features["good"]["names"], features["good"]["religion"], features["good"]["weaponry"], features["good"]["government"] = len(goodBlogList), analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
    
    # pdb.set_trace()
    # weightedFeatures = applyWeights(features, weightedFeatures)
    # goodScore, badScore = 0.0, 0.0

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
        pdb.set_trace()
        # analyze, decide good or bad, then append to json_object

    # Update and add new data to JSON object

    # Wait

    # Next, check apply weights for the other word types mentioned in the report. 
    # Generate feature weights based on if they appear in the most common words, 
    # relative to if they just appear normally
    
    pdb.set_trace() # End, check on debug. 
if __name__ == "__main__": main()

