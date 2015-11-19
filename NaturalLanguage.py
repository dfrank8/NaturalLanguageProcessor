import sys
import tfidf
import json
import pdb

def importJSON(inFile):
	with open(inFile) as json_file:
		json_data = json.load(json_file)
	pdb.set_trace()
	
# Can be queried with json_data["writings"]["good"][0]["post"]

importJSON("Writings/writings.json")