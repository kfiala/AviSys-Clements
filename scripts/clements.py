# Reads Clements checklist CSV and MASTER.OLD.EDT and generates six files:
#
# MASTER.EDT        Input to EditMaster.exe
# subspecies.txt    Content to be encrypted as SSDATA.AVI
# newnames.txt      List of names from Clements that were not in MASTER.OLD.EDT
# lostnames.txt     List of names from MASTER.OLD.EDT that are not in Clements
# longnames.txt     List of names that need to be shortened to meet the 36 character limit
# changes.csv       Summary of taxonomic changes in Clements checklist

import glob
import sys

#  input files:
try:
	CLEMENTS = glob.glob('Clements-Checklist*.csv')[0]	# New Clements spreadsheet in CSV format
except IndexError:
	print('\nError: Did not find Clements checklist file matching name "Clements-Checklist*.csv"\n')
	raise SystemExit
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
print('Using Clements',CLEMENTS)
OLDEDT = 'MASTER.OLD.EDT'	# Renamed copy of MASTER.EDT for the old AviSys level

# Output files
MASTEREDT =			open('MASTER.EDT','w')
SUBSPECIESFILE =	open('subspecies.txt','w')
NEWNAMES =			open('newnames.txt','w')
LOSTNAMES =			open('lostnames.txt','w')
LONGNAMES =			open('longnames.txt','w')
CHANGES = 			open('changes.csv','w', newline='')

csvFields = ['sort','Clements change','text for website','category','English name','scientific name','range','order','family','extinct']

from clementsFunctions import setExtinctKeep

exKeep = setExtinctKeep()

# Edit the old MASTER EDT and construct name lookups
ABAstatus = {}
lostName = {}

try:
	for line in open(OLDEDT).readlines():
		token = line.split(',')
		common = token[0].strip()
		AviSysSequence = token[4].rstrip()
		ABAstatus[common] = token[3]
		lostName[common] = 'F' if AviSysSequence == '0' else 'S'	# Family or Species name
except FileNotFoundError:
	print('Error:',OLDEDT,'does not exist. Cannot continue.')
	raise SystemExit
except:
    print("Unexpected error while opening:",OLDEDT,sys.exc_info()[0])
    raise

subspeciesOutput = []
counter = 1
prevfam = ''

import csv
CSVwriter = csv.DictWriter(CHANGES,fieldnames=csvFields)

with open(CLEMENTS) as csvfile:
	csvreader = csv.DictReader(csvfile,fieldnames=csvFields)
	headerSeen = False
	for row in csvreader:
		if not headerSeen:
			headerSeen = True
			CSVwriter.writeheader()
			continue
		sort = row['sort']
		change = row['Clements change']
		text = row['text for website']
		category = row['category']
		common = row['English name']
		scientific = row['scientific name']
		range = row['range']
		order = row['order']
		family = row['family']
		extinct = row['extinct']

		text = text.replace("’","'")	# ASCII single quotes
		common = common.replace("’","'")
		range = range.replace("’","'")

		sci = scientific
		groupPos = sci.find('[')
		if groupPos >= 0:
			group = sci[groupPos:]
			sci = sci[:groupPos]
		else:
			group = ''
		sci = sci.split()
		genus = sci[0]
		if len(sci) >= 2:
			species = sci[1]
			if len(sci) > 2:
				subspecies = sci[2]
			else:
				subspecies = group
		else:
#			print('Short sci:',sci,'at line',sort)	# These are all "forms"
#			species = ''
#			subspecies = ''
			pass

#  Skip most extinct species
		if extinct and not common in exKeep:
#			print('Skipping extinct',common,genus,species,subspecies)
			continue

#  Process the record according to its 'category'

		if category == 'species':
# 			Flush the accumulated subspecies data. If there is only one datum,
# 			that means no subspecies so do nothing.
			if len(subspeciesOutput) > 1:
				for line in subspeciesOutput:
					SUBSPECIESFILE.write(line+'\n')
			subspeciesOutput = ['o '+common+'  '+genus+' '+species]	# Restart accumulating subspecies data for this species

			g = genus[0]
			s = species[0]
			initials = '-- '+g+'. '+s+'.'

# The record contains both species and family. Only if it's a new family, process family.
			if family != prevfam:	# New family
				prevfam = family
#				family = family.upper()
#				order = order.upper()
				famnames = family.split('(')
				scifam = famnames[0]
				engfam = famnames[1].rstrip()
				engfam = engfam.rstrip(')')
				engfam = engfam.replace(',','~')
				scifam = scifam.upper()
				engfam = engfam.upper()

				if engfam in ABAstatus:
					ABA = ABAstatus[engfam]
					del lostName[engfam]	# This name is in the new taxonomy; not lost
				else:
					ABA = 'W'	#  This family is not in the old MASTER.EDT. Mark it non-ABA and record it as a new name.
					NEWNAMES.write('F '+engfam+'\n')

# 				Format the family entry line, and insert it
				MASTEREDT.write(engfam+','+order.upper()+','+scifam+','+ABA+',0\n'.upper())

# 				Warn about long names that we will have to fix manually
				if len(engfam) > 36: 	LONGNAMES.write('Family name > 36 chars: '+engfam+'\n')
				if len(order) > 24: 	LONGNAMES.write('Order name > 24 chars: '+order+'\n')
				if len(scifam) > 24: 	LONGNAMES.write('Family name > 24 chars: '+scifam+'\n')

# 			Now deal with the species in the record
			if common in ABAstatus:
				ABA = ABAstatus[common]
				del lostName[common]	# This name is in the new taxonomy; not lost
			else:
				ABA = 'W' # This species is not in the old MASTER.EDT. Mark it non-ABA and record it as a new name.
				NEWNAMES.write('S '+common+'\n')
			counter += 3	# Set the AviSys sequence number
			outputLine = '  '+common+','+genus+','+species+','+ABA+','+str(counter)+'\n'
#			print(outputLine)
			MASTEREDT.write(outputLine) # Format the MASTER.EDT record and insert it

#			Warn about long names that we will have to fix manually
			if len(common) > 36:	LONGNAMES.write('Common name > 36 chars: '+common+'\n')
			if len(genus) > 24:		LONGNAMES.write('Genus name > 24 chars: '+genus+'\n')
			if len(species) > 24:	LONGNAMES.write('Species name > 24 chars: '+species+'\n')

		elif category == 'subspecies':
			subspeciesOutput.append(initials+' '+subspecies) # Accumulate info on subspecies
		elif category == 'group (monotypic)':
			string = initials + ' * ' + subspecies
			groupPos = common.find('(')
			if groupPos > -1:
				string += ' ' + common[groupPos:]
			subspeciesOutput.append(string)
		elif category == 'group (polytypic)':
			groupPos = common.find('(')
			if groupPos > -1:
				group = common[groupPos:]
			else:
				group = ''
			if subspecies.find('/') > -1:
				string = initials + ' *2 ' + subspecies
				if group:
					string += ' ' + group
				subspeciesOutput.append(string)


			elif subspecies.find('[') > -1:
				groupPos = subspecies.find('[')
				string = initials + ' *> ' + subspecies[groupPos:]
				if group:
					string += ' ' + group
				subspeciesOutput.append(string)
			else:
				print('Cannot parse line',sort)
				break
		elif category in ['slash','spuh','hybrid','domestic','form','intergrade']:
			pass
		else:
			print('Unknown category ',category,' for line',sort)
			break
		delete = category != 'species' or change in ['new group','range','sequence'] or (not change and not text)
		if not delete:
			CSVwriter.writerow({'sort':sort,'Clements change':change,'text for website':text,'category':category,
				'English name':common,'scientific name':scientific,
				'range':range,'order':order,'family':family,'extinct':extinct})

# Create new file in which to list names that are only in the old data
for name,type in lostName.items():
	LOSTNAMES.write(type+' '+name+ '\n')


