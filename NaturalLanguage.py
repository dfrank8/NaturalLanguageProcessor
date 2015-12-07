# NOTE: MUST USE PYTHON 3!!!!!!
import sys
import tfidf
import json
import terms
import argparse
from argparse import RawTextHelpFormatter
from textblob import TextBlob as tb
import pdb


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

def analyzeBlog(blogList): # Analyze blog with tfidf, and other word analysis. 
    outputWordsArr  = []
    namesCount, religionCount, weaponryCount, governmentCount, wordCount = 0, 0, 0, 0, 0
    for i, blog in enumerate(blogList):
        print("Top words in document {}".format(i + 1))
        for word in blog.words:
            word = word.lower() # Everything is in lowercase. 
            wordCount+=1
            if word not in terms.stopWords(): # check if word is stop words, ignore it if it is
                scores = {word: tfidf.tfidf(word, blog, blogList)} # run tfidf
            if word in terms.governmentTerms(): # increment count based on content to find word densities. 
                governmentCount+=1
            if word in terms.weaponsTerms():
                weaponryCount+=1
            if word in terms.femaleNames() or word in terms.maleNames():
                namesCount+=1
            if word in terms.religiousTerms():
                religionCount+=1
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) # sort the words
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            outputWordsArr.append((word, round(score, 5)))
        print("---------------------------------------------------------")
    # Gathering the density scores of each of these defined features, and creating the returning data type
    analysisOutputs = AnalysisObject(namesCount/wordCount,religionCount/wordCount,weaponryCount/wordCount,governmentCount/wordCount,outputWordsArr)
    return analysisOutputs

# def applyWeights(feature): # Apply weights to the scores in the features object. 
    # Check if a word that is part of the different terms and also in the top-words list. That increases its weight. 

# def updateFeatures(feature, newFeatures):
    # update good and bad features depending on the decision by the alogrithm of which class it falls under.

def buildNewBlog(blogFile, blogAuthor, blogTitle, blogText, jsonObject):
    if(blogFile == None):
        

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
    blogFile = args.inFile
    blogText = blog
    # The below object is a dictionary of 2 dictionaries, good and bad features, and their relevant metadata. 
    features = {"good":{"words": [], "punctuation": 0.0, "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}, "bad": {"words": [], "punctuation": 0.0, "names": 0.0, "religion": 0.0, "weaponry": 0.0, "government": 0.0}}
    json_data = importJSON("Writings/writings.json") # get JSON data, creating a dictionary-like object 
    
    # Declaring lists of writings
    badBlogList = []
    goodBlogList = []
    
    # Analyze the current data in the JSON file. 
    for blog in json_data["writings"]["bad"]:
    	badBlogList.append(tb(blog["post"]))
    for blog in json_data["writings"]["good"]:
    	goodBlogList.append(tb(blog["post"]))


    
    analysisResults = analyzeBlog(badBlogList)
    features['bad']['words'], features['bad']['names'], features['bad']['religion'], features['bad']['weaponry'], features['bad']['government'] = analysisResults.outputsWordsArray, analysisResults.namesScore, analysisResults.religionScore, analysisResults.weaponryScore, analysisResults.governmentScore
    analysisResults2 = analyzeBlog(goodBlogList)
    features['good']['words'], features['good']['names'], features['good']['religion'], features['good']['weaponry'], features['good']['government'] = analysisResults2.outputsWordsArray, analysisResults2.namesScore, analysisResults2.religionScore, analysisResults2.weaponryScore, analysisResults2.governmentScore
    
    # Apply weights

    # Analyze new file

    # Update and add new data to JSON object

    # Wait

    # Next, check apply weights for the other word types mentioned in the report. 
    # Generate feature weights based on if they appear in the most common words, 
    # relative to if they just appear normally
    
    pdb.set_trace() # End, check on debug. 
if __name__ == "__main__": main()

