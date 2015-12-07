import string
import sys
import re

'''
File should be a text file that follows this format:
Line #
---------------------------------------------------
  1 |author: Jane Doe
  2 |title: My time in Prague
  3 |post: I went to Prague when I was 18...
---------------------------------------------------
** Please note that the post needs to be programmatically 1 line. 
'''


class BlogObject: # Analysis Object that is returned by the analysis function, which allows all relevant data to stay together. 
    def __init__(self, post, author = "", title = ""):
        self.author = author
        self.title = title
        self.post = post

def getBlog(inFile):
	outfile = open("output.txt", 'w')
	with open(inFile, 'r') as infile:
		count = 0
		author = None
		title = None
		post = None
		for raw_line in infile:
			if(re.match("author: ",raw_line)):
				line = str(raw_line).replace("author: ", "")
				print("It worked! author = " + " " + line)
				author = line
			if(re.match("title: ",raw_line)):
				line = str(raw_line).replace("title: ", "")
				print("It worked! title = " + " " + line)
				title = line
			if(re.match("post: ",raw_line)):
				line = str(raw_line).replace("post: ", "")
				print("It worked! post = " + " " + line)
				post = line
		if(post == None):
			print("[err] Issue reading text file. No content in 'post'")
			return False
		else:
			if(author == None):
				print("[warn] No author")
			if(title == None):
				print("[warn] No title")
			newBlog = BlogObject(post, author, title)
			return newBlog
	print ("[err] Failed to create blog post from file")
	return False



