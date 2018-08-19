#
# Create the STATE.SDT file from the state checklists
#
from os import listdir
import binascii
import ABA

# Input files in working directory
MASTER_EDT	= 	'MASTER.EDT'
GRANDFATHER	= 	'grandfather.SDT.txt'

# Input folder of state checklists
STATELIST_DIR =	r'State checklists\txt\\'	# Location of state checklists from eBird

# Output files
STATE_SDT =			'STATE.SDT'								# Binary file for AviSys
STATE_SDT_TXT =	'STATE.SDT.txt'						# Readable version of STATE_SDT
GF_ONLY_SPECIES =	'GF_not_eBird_by_species.txt'	# Checklist entries in grandfather but not eBird, by species
GF_ONLY_STATE =	'GF_not_eBird_by_state.txt'		# Checklist entries in grandfather but not eBird, by state

bits = {
		'US-VT' : 1      ,    # VT 0000000000000001
		'US-VA' : 1 << 1 ,    # VA 0000000000000002
		'US-WA' : 1 << 2 ,    # WA 0000000000000004
		'US-WV' : 1 << 3 ,    # WV 0000000000000008
		'US-WI' : 1 << 4 ,    # WI 0000000000000010
		'US-WY' : 1 << 5 ,    # WY 0000000000000020
		'CA-YT' : 1 << 6 ,    # YT 0000000000000040
		'CA-NU' : 1 << 7 ,    # NU 0000000000000080
		'CA-QC' : 1 << 8 ,    # QC 0000000000000100
		'US-RI' : 1 << 9 ,    # RI 0000000000000200
		'CA-SK' : 1 << 10 ,   # SK 0000000000000400
		'US-SC' : 1 << 11 ,   # SC 0000000000000800
		'US-SD' : 1 << 12 ,   # SD 0000000000001000
		'US-TN' : 1 << 13 ,   # TN 0000000000002000
		'US-TX' : 1 << 14 ,   # TX 0000000000004000
		'US-UT' : 1 << 15 ,   # UT 0000000000008000
		'CA-NT' : 1 << 16 ,   # NT 0000000000010000
		'CA-NS' : 1 << 17 ,   # NS 0000000000020000
		'US-OH' : 1 << 18 ,   # OH 0000000000040000
		'US-OK' : 1 << 19 ,   # OK 0000000000080000
		'CA-ON' : 1 << 20 ,   # ON 0000000000100000
		'US-OR' : 1 << 21 ,   # OR 0000000000200000
		'US-PA' : 1 << 22 ,   # PA 0000000000400000
		'CA-PE' : 1 << 23 ,   # PE 0000000000800000
		'CA-NB' : 1 << 24 ,   # NB 0000000001000000
		'US-NH' : 1 << 25 ,   # NH 0000000002000000
		'US-NJ' : 1 << 26 ,   # NJ 0000000004000000
		'US-NM' : 1 << 27 ,   # NM 0000000008000000
		'US-NY' : 1 << 28 ,   # NY 0000000010000000
		'CA-NL' : 1 << 29 ,   # NL 0000000020000000
		'US-NC' : 1 << 30 ,   # NC 0000000040000000
		'US-ND' : 1 << 31 ,   # ND 0000000080000000
		'US-MA' : 1 << 32 ,   # MA 0000000100000000
		'US-MI' : 1 << 33 ,   # MI 0000000200000000
		'US-MN' : 1 << 34 ,   # MN 0000000400000000
		'US-MS' : 1 << 35 ,   # MS 0000000800000000
		'US-MO' : 1 << 36 ,   # MO 0000001000000000
		'US-MT' : 1 << 37 ,   # MT 0000002000000000
		'US-NE' : 1 << 38 ,   # NE 0000004000000000
		'US-NV' : 1 << 39 ,   # NV 0000008000000000
		'US-IN' : 1 << 40 ,   # IN 0000010000000000
		'US-IA' : 1 << 41 ,   # IA 0000020000000000
		'US-KS' : 1 << 42 ,   # KS 0000040000000000
		'US-KY' : 1 << 43 ,   # KY 0000080000000000
		'US-LA' : 1 << 44 ,   # LA 0000100000000000
		'US-ME' : 1 << 45 ,   # ME 0000200000000000
		'CA-MB' : 1 << 46 ,   # MB 0000400000000000
		'US-MD' : 1 << 47 ,   # MD 0000800000000000
		'US-CT' : 1 << 48 ,   # CT 0001000000000000
		'US-DE' : 1 << 49 ,   # DE 0002000000000000
		'US-DC' : 1 << 50 ,   # DC 0004000000000000
		'US-FL' : 1 << 51 ,   # FL 0008000000000000
		'US-GA' : 1 << 52 ,   # GA 0010000000000000
		'US-HI' : 1 << 53 ,   # HI 0020000000000000
		'US-ID' : 1 << 54 ,   # ID 0040000000000000
		'US-IL' : 1 << 55 ,   # IL 0080000000000000
		'US-AL' : 1 << 56 ,   # AL 0100000000000000
		'US-AK' : 1 << 57 ,   # AK 0200000000000000
		'CA-AB' : 1 << 58 ,   # AB 0400000000000000
		'US-AZ' : 1 << 59 ,   # AZ 0800000000000000
		'US-AR' : 1 << 60 ,   # AR 1000000000000000
		'CA-BC' : 1 << 61 ,   # BC 2000000000000000
		'US-CA' : 1 << 62 ,   # CA 4000000000000000
		'US-CO' : 1 << 63     # CO 8000000000000000
}


def readEdit(master_edt):	# Read MASTER_EDT; get species names and numbers and create lookup tables
	global name, number_lookup	# lookup tables are used globally

	number_lookup = {}
	for record in open(master_edt,'r').readlines():
		field = record.split(',')
		species = field[0].strip()
		number = int(field[4].strip())
		if number == 0:
			continue
		number_lookup[species] = number	# name-to-number lookup
		name[number] = species				# number-to-name lookup

	if len(number_lookup):
		print("Read",master_edt,"successfully")
	else:
		print("ERROR: Did not read",master_edt)
		raise SystemExit
	return


def readGrandfather():	# Read grandfather.SDT.txt (list of species on state checklists but possibly not in eBird)
	global number_lookup, grandfather

	grandfather = {}
	for record in open(GRANDFATHER).readlines():
		commonName = record[17:].strip()	# Common name starts in column 18
		if commonName in number_lookup:
			grandfather[number_lookup[commonName]] = int(record[0:16],16)	# Hex bit mask is in columns 1-16.
		else:
			print(commonName,"found in",GRANDFATHER,"but not in",MASTER_EDT)
	if len(grandfather) == 0:
		print("ERROR: Did not read",GRANDFATHER,"successfully.")
		raise SystemExit
	else:
		print("Read",GRANDFATHER,"successfully")
	return

def delta_report_by_species(GFonly): # For each species, report the states for which it is only on the grandfather list
	global bits, name

	stateList = sorted(bits.keys())	# Get the list of state codes that are keys for the bits dictionary; sort them

	delta_report = {}

	for number in sorted(GFonly.keys()):	# Go through the GFonly dictionary, in sorted key order
		states = []
		for state in stateList:	# Go through the states, keeping a list of states whose GFonly bit is set for this species
			if GFonly[number] & bits[state] != 0:
				states.append(state)
		if len(states):
			delta_report[number] = name[number].ljust(32) + " " + ','.join(states) + '\n'

	f = open(GF_ONLY_SPECIES,'w')
	for number in sorted(delta_report.keys()):
		f.write(delta_report[number])
	f.close()
	return


def delta_report_by_state(GFonly):
# For each state, report the species that are only on the grandfather list for that state
	global bits, name

	stateList = sorted(bits.keys())	# Get the list of state codes that are keys for the bits dictionary; sort them
	GFonlyNumbers = sorted(GFonly.keys())	# Get the list of species numbers

	delta_report = []

	for state in stateList:				# For each state
		for number in GFonlyNumbers:	# For each GFonly species
			if GFonly[number] & bits[state]:	# List species in GFonly for this state
				delta_report.append(state + ' ' + name[number] + '\n')

	f = open(GF_ONLY_STATE,'w')
	for line in delta_report:
		f.write(line)
	f.close()
	return

	
name = {}
readEdit(MASTER_EDT)			# Get taxonomy
ABAlist = ABA.readABAcsv()	# Get ABA list
readGrandfather()				# Get grandfather list
GFonly = {}

table = {}
specieslist = {}

# Build the list of states for each species.

for file in listdir(STATELIST_DIR):	# For each state checklist .txt file
	if file.endswith(".txt"):
		filepath = STATELIST_DIR+file
		state = file[0:5]	# e.g., US-NC

		key = 0
		for species in open(filepath).readlines():
			species = species.strip()
			if species not in ABAlist:	# Species on Clements list but not ABA list
				print("\n*** State", state, "has eBird record of non-ABA species", species)
				continue

			if species not in specieslist:
				specieslist[species] = True
				table[species] = []

			table[species].append(state)
	

# For each species, create the eBird states mask and OR with the grandfather mask.
output = grandfather.copy()	# Start with a copy of the grandfather list; we'll add eBird lists to it.
zerosMask = 0

for species in specieslist:
	states = table[species]	# List of states where this species is recorded
	mask = zerosMask
	for state in states:	# Make a bit mask of the list of states
		mask |= bits[state]
	if species in number_lookup:
		number = number_lookup[species]
		output[number] = mask
		if number in grandfather:
			GFonly[number] = grandfather[number] & ~ mask	# grandfather mask and not eBird mask
			output[number] |= grandfather[number]				# Combine the masks
			del grandfather[number]									# Won't need it again
	else:	# Species on ABA list but not Clements list
		stateList = []
		for state in bits:
			if mask & bits[state]:
				stateList.append(state)
		List = ', '.join(stateList)
		print( "\n***",species, "is not in",MASTER_EDT,"but eBird reports for", List)

# Generate the new STATE.SDT file
fileText = open(STATE_SDT_TXT,'w')	# Human readable
fileBin  = open(STATE_SDT,'wb')		# AviSys readable

for number in sorted(output.keys()):
	mask = output[number]
	binMask = mask.to_bytes(8, byteorder='big')
	fileBin.write(int(number).to_bytes(2, byteorder='little'))
	fileBin.write(binMask)
	asciiMask = binascii.hexlify(binMask)
	line = asciiMask.decode('utf-8') + ' ' + name[number] + '\n'
	fileText.write(line)
fileText.close()
fileBin.close()

if grandfather:
#	print('Grandfathered species not in any eBird list:')
	for number in grandfather:
#		print(name[number])
		GFonly[number] = grandfather[number]

delta_report_by_species(GFonly)
delta_report_by_state(GFonly)

print('')