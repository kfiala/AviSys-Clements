# Return the list of species from the ABA checklist, with any Clements differences substituted.

import csv
import glob
import sys

def readABAcsv():
	try:
		ABAcsv = glob.glob('ABA_Checklist-*.csv')[0]
	except IndexError:
		print('\nError: Did not find ABA checklist file matching name "ABA_Checklist-*.csv"\n')
		raise SystemExit
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise SystemExit
	else:
		print('Using ABA checklist',ABAcsv)

	ABAspecies = []

	(ClementsName,ClementsOnly) = readAOSdiffs('AOS diffs.csv')

	started = False
	with open(ABAcsv,newline='') as csvfile:
		csvreader = csv.DictReader(csvfile,fieldnames=['family','comName','frenchName','sciName','FLBC','ABAcode'])
		for row in csvreader:
			if row['family']:
				started = True
			if not started:
				continue	# Skip over possible header at beginning; any rows before the first family entry
			comName = row['comName']
			if comName == '':
				continue	# In current version, there is no species on rows with family name.
			if row['sciName'] == '':
				print("Missing scientific name for",comName)
#			if len(row['FLBC']) != 4:
#				print("FLBC not correct for",comName)
			if row['ABAcode'] == '':
				print("Missing ABA code for",comName)

			if comName in ClementsName:	# Accommodate species where the Clements name is different from the ABA name.
				ABAspecies.append(ClementsName[comName])
			else:
				ABAspecies.append(comName)

	ABAspecies.extend(ClementsOnly)	# Treat Clements-only species as if they were on the ABA list.

	return ABAspecies

def readAOSdiffs(path):		# List the differences between Clements and ABA nomenclature
	ClementsName = {}
	ClementsOnly = []
	with open(path) as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			if row['ABA']:
				ClementsName[row['ABA']] = row['AviSys']	# Clements name is different from ABA name
			else:
				ClementsOnly.append(row['AviSys'])	# Species is recognized by Clements but not by ABA
	return (ClementsName,ClementsOnly)
