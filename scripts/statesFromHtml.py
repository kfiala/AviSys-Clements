# Extract state bird lists from eBird state checklists downloaded as html
import os
import glob
import ABA

def parseFile(filename,ABAspecies):
# This function reads one downloaded html state checklist and parses out the species list.
	birdlist = []
	infile = open(filename,encoding='ascii',errors='ignore')
	for line in infile:
#		First, find the one line that identifies the geographic region.
#		The string that we are looking for changes from time to time--need to check for changes before each run.
		esub = line.find('action="/region/')	# The line that contains the location code can be recognized by this string.
		if esub == -1:
			continue
		subnational = line[esub+len('action="/region/'):]	# The country-state code will immediately follow this string
		tokens = subnational.split('"')	# Truncate at the first quotation mark
		subnational = tokens[0]
		break	# Stop once we have found the line

	for line in infile:	# Continue reading the rest of the file to pick out species entries.
#		Entries that represent species will be identified by a single class "species-name"
#		Some entries have more than one class; hence no closing quote after the first class name.
#		But we don't want those entries; they will be things like class="species-name species-name--spuh", so require close quote.
		if line.find('class="species-name"') > -1:
			token = line.split('>')	# Split out the species name between a '>' and '<'
			name = token[1].split('<')
			species = name[0]
			if species in ABAspecies:	# Only accept species that are on the ABA list.
				birdlist.append(species)
			else:
#				print('Non-ABA:',species)
				pass
	return (subnational,birdlist)


ABAspecies = ABA.readABAcsv()

# Call parseFile for each downloaded checklist file in the path
path = 'State checklists'
inPath = path+r'\html\\'
outPath = path+r'\txt\\'
for filename in os.listdir(inPath):
	if filename.endswith(".html"):
		filepath = inPath+filename
		(subnational,birdlist) = parseFile(filepath,ABAspecies)
		if not birdlist: break
		# Write the list of species to a new .txt file
		outfile = open(outPath + subnational+'.txt','w')
		for species in birdlist:
			outfile.write(species+'\n')
		outfile.close()



