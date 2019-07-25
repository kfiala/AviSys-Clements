#
# Perform the equivalent of the EditMaster function CREATE MASTER EDIT FILE -- create MASTER.EDT
# Extra bonus, also create Hawaii-only.txt, list of ABA species that are not continental
#
import sys
import binascii

# Command line option is input file name
if len(sys.argv) < 2:	# No command line option
	print("Specify path to MASTER.AVI, e.g. C:\AVI6\datafolder\MASTER.AVI")
	raise SystemExit
else:
	master_file = sys.argv[1]

upper = master_file.upper()
if upper.find("MASTER.UPD") == -1 and upper.find("MASTER.AVI") == -1:
	print("Input file must be either MASTER.UPD or MASTER.AVI")
	raise SystemExit

output_file = "MASTER.EDT"
print("Creating",output_file)

try:
	fh = open(output_file,"w")
except:
	print("Error opening",output_file)
	raise SystemExit

input_file = open(master_file, "rb")
Hawaii = 1<<53
Hawaii_only = []
output = []
region = []

counter = 0
while True:
	taxon = input_file.read(110)	# Read a record of 110 bytes
	if not taxon:
		break

	namelen_byte = taxon[7:8]
	namelen = int(binascii.hexlify(namelen_byte),16)
	name = taxon[8:8+namelen].decode('Windows-1252')	# decode converts byte array to string
	name = name.replace(',','~')

	genuslen_byte = taxon[52:53]
	genuslen = int(binascii.hexlify(genuslen_byte),16)
	genus = taxon[53:53+genuslen].decode('Windows-1252')

	specieslen_byte = taxon[77:78]
	specieslen = int(binascii.hexlify(specieslen_byte),16)
	species = taxon[78:78+specieslen].decode('Windows-1252')

	if not any(c.islower() for c in name):
		family = counter

#	region is 'N' if it should be on the N.A. mode list, 'W' if only on World list
#	For a family heading, start out as 'W' but change to 'N' if an 'N' species is encountered
	statebits = int(binascii.hexlify(taxon[44:52]),16)
	if statebits == 0 or statebits == Hawaii:	# Exclude Hawaii-only
		region.append('W')	# World-only species
		if statebits == Hawaii:
			Hawaii_only.append(name)
	else:
		region.append('N')	# N.A. mode species
		region[family] = 'N'

	newRecord = name + ',' + genus + ',' + species # + ',' + region + ',' + number + "\n"
	output.append(newRecord)
	counter += 1

counter = 0
number = 1
increment = 3
for record in output:
	if any(c.islower() for c in record):
		number += increment
		newRecord = '  ' + record  + ',' + region[counter] + ',' + str(number) + "\n"
	else:
		newRecord = record + ',' + region[counter] + ",0\n"
	fh.write(newRecord)
	counter += 1

fh.close()

# All done with primary task, now write out the Hawaii-only file
try:
	fh = open('Hawaii-only.txt',"w")
except:
	raise SystemExit

for species in Hawaii_only:
	fh.write(species+'\n')
fh.close()

