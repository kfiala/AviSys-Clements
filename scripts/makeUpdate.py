#
# Create the STATE.SDT file from the state checklists
# and continue to make MASTER.UPD
#
from os import listdir, remove
import binascii
import ABA
import sys

cleanup = True	# If you want STATE.SDT and STATE.SDT.txt to be deleted

if len(sys.argv) < 2:	# If no command-line argument
	extension = '.clb'
else:
	extension = sys.argv[1]	# Checklist file extension is first argument
if extension[0:1] != '.':
	extension = '.' + extension	# Prepend initial '.' if omitted

# Input files in working directory
MASTER_EDT	= 	'MASTER.EDT'

# Input folder of state checklists
STATELIST_DIR =	r'State checklists\\'	# Location of state checklists
COMMENT_CHAR = ';'	# Character that denotes comments in checklist files

# Output files
if extension == '.clb':
	STATE_SDT =			'STATE.SDT'						# Binary file for AviSys
	STATE_SDT_TXT =		'STATE.SDT.txt'					# Readable version of STATE_SDT
else:
	STATE_SDT =			'STATE'+extension+'.SDT'		# Binary file for AviSys
	STATE_SDT_TXT =		'STATE'+extension+'.SDT.txt'	# Readable version of STATE_SDT

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
	anyError = False
	number_lookup = {}
	for record in open(master_edt,'r').readlines():
		field = record.split(',')
		species = field[0].strip()
		if len(species) > 36:
			print('Error: In',MASTER_EDT,'the name',species,'is longer than 36 characters')
			anyError = True
		number = int(field[4].strip())
		if number == 0:
			continue
		number_lookup[species] = number	# name-to-number lookup
		name[number] = species				# number-to-name lookup

	if anyError:
		print('Correct errors and try again')
		raise SystemExit

	if len(number_lookup):
		print("Read",master_edt,"successfully")
	else:
		print("ERROR: Did not read",master_edt)
		raise SystemExit
	return

	
name = {}
readEdit(MASTER_EDT)			# Get taxonomy
ABAlist = ABA.readABAcsv()		# Get ABA list

speciesTable = {}
specieslist = {}
stateCount = 0
nonABA = {}
nonABAcount = 0

# Build the list of states for each species.

for file in listdir(STATELIST_DIR):	# For each state checklist file
	if file.endswith(extension):
		filepath = STATELIST_DIR+file
		state = file[0:5]	# e.g., US-NC
		stateCount += 1
		badSpecies = []

		key = 0
		for species in open(filepath).readlines():
			species = species.strip()
			comment = species.find(COMMENT_CHAR,0)
			if comment != -1:
				species = species[0:comment].strip()	# strip comments
			if species == '':	# Skip over empty lines
				continue
			if species not in ABAlist:	# Species on Clements list but not ABA list
#				print("\n*** State", state, "includes non-ABA species", species)
				badSpecies.append(species)
				nonABAcount += 1
				continue

			if species not in specieslist:
				specieslist[species] = True
				speciesTable[species] = []

			speciesTable[species].append(state)
		if len(badSpecies):
			nonABA[state] = badSpecies
	

# For each species, create the states mask.
output = {}
zerosMask = 0

for species in specieslist:
	states = speciesTable[species]	# List of states where this species is recorded
	mask = zerosMask
	for state in states:	# Make a bit mask of the list of states
		mask |= bits[state]
	if species in number_lookup:
		number = number_lookup[species]
		output[number] = mask
	else:	# Species on ABA list but not Clements list
		stateList = []
		for state in bits:
			if mask & bits[state]:
				stateList.append(state)
		List = ', '.join(stateList)
		print( "\nWarning: ABA species",species, "is not in Clements but listed by", List)

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
if stateCount != 64:
	print("Warning: Expected 64 state checklists, but found",stateCount)
print('')

if len(nonABA):
	print(nonABAcount,'non-ABA species were encountered in',len(nonABA),'states')
	try:
		fh = open('non-ABA.txt',"w")
	except:
		raise SystemExit

	for state in nonABA:
		for species in nonABA[state]:
			fh.write(state+' '+species+'\n')
	fh.close()

############################################################################
# All done with state checklists. Now continue with the master update file.
# This used to be a separate script.
############################################################################
	

# Input files in working directory
MASTER_EDT	= 	'MASTER.EDT'
STATE_SDT =		'STATE.SDT.txt'

try:
	fh = open('MASTER.UPD',"wb")
except:
	raise SystemExit

mask = {}
checklistMask =  1 << 37 #  2000000000
checklistMask = checklistMask.to_bytes(5,byteorder='big')
nullMask = int(b'0000000000000000',16).to_bytes(8,byteorder='big')

ABA = 1
ABA = ABA.to_bytes(8,byteorder='little')
World = 0
World = World.to_bytes(8,byteorder='little')
Hawaii = 1<<53
Hawaii = Hawaii.to_bytes(8,byteorder='big')

for record in open(STATE_SDT,'r').readlines():
	field = record.split(' ',1)
	mask[field[1].strip()] = int(field[0],16).to_bytes(8,byteorder='big')

for record in open(MASTER_EDT,'r').readlines():
	field = record.split(',')
	commonName = field[0].strip()
	commonName = commonName.replace('~',',')
	genus = field[1]
	species = field[2]
	regionCode = field[3]
	number=field[4].strip()
	if number == 0:
		isFamily = True
	else:
		isFamily = False

# Generate 110 byte record
#	0x20 byte		[0]	
#	checklist mask	[1] len 4 (zeros)
#   species number	[5] len 2
#	namelen			[7]	len 1
#	commonName		[8]	len 36
#	states mask		[44] len 8
#	genuslen		[52]
#	genus			[53] len 24
#	specieslen		[77]
#	species			[78] len 24
#	fill			[102] len 8 (first byte is ABA flag)

	if isFamily:
		states = nullMask
		if regionCode == 'N':
			region = ABA
		else:
			region = World
	elif commonName in mask:
		if mask[commonName] != Hawaii:
			states = mask[commonName]
			region = ABA
		else:
			states = Hawaii
			region = World
	else:
		states = nullMask
		region = World

	output = checklistMask \
		+ int(number).to_bytes(2,byteorder='little')\
		+ len(commonName).to_bytes(1,byteorder='little')\
		+ commonName.ljust(36).encode('Windows-1252')\
		+ states + len(genus).to_bytes(1,byteorder='little')\
		+ genus.ljust(24).encode('Windows-1252')\
		+ len(species).to_bytes(1,byteorder='little')\
		+ species.ljust(24).encode('Windows-1252')\
		+ region
	fh.write(output)

if cleanup:
	remove('STATE.SDT')
	remove('STATE.SDT.txt')
