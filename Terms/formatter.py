import string
import sys

outfile = open("output.txt", 'w')

with open("FemaleNames.txt", 'r') as infile:
	for raw_line in infile:
		line = 'x'.join(raw_line.split())
		first_value = line[0:line.find('x')]
		outfile.write('"' + str(first_value).lower() + '",' + ' ')