#
# Rewrite MASTER.UPD (or MASTER.AVI) while blank-padding all strings to replace slack junk
#
import sys
import binascii

# Default to update MASTER.UPD
if len(sys.argv) < 2:	# No command line option, use MASTER.UPD
	master_file = "MASTER.UPD"
else:	# Do update for file given on command line
	master_file = sys.argv[1]

if (master_file.upper() != "MASTER.UPD" and master_file.upper() != "MASTER.AVI"):
	print("Specify either MASTER.UPD or MASTER.AVI")
	raise SystemExit

extension = master_file[-3:].upper()

newmaster_file = "remaster." + extension

print("Cleaning up",master_file,"into",newmaster_file)

#keepChecklists = (extension == 'AVI')
keepChecklists = True	# Experimental and disabled. Clears checklist bits.

if keepChecklists:
	mask = 1 << 37
	bytes1 = mask.to_bytes(5, byteorder='big')

try:
	fh = open(newmaster_file,"wb")
except:
	print("Error opening",newmaster_file)
	raise SystemExit

input_file = open(master_file, "rb")
while True:
	taxon = input_file.read(110)	# Read a record of 110 bytes
	if not taxon:
		break

	if keepChecklists:
		bytes1 = taxon[0:5]
	bytes4 = taxon[102:]
	statebits = taxon[44:52]

	species_number = taxon[5:7]

	namelen_byte = taxon[7:8]
	namelen = int(binascii.hexlify(namelen_byte),16)
	name = taxon[8:8+namelen].decode('Windows-1252')	# decode converts byte array to string

	genuslen_byte = taxon[52:53]
	genuslen = int(binascii.hexlify(genuslen_byte),16)
	genus = taxon[53:53+genuslen].decode('Windows-1252')

	specieslen_byte = taxon[77:78]
	specieslen = int(binascii.hexlify(specieslen_byte),16)
	species = taxon[78:78+specieslen].decode('Windows-1252')

	padName = name.ljust(36).encode('Windows-1252')	# encode converts string to byte array
	padGenus = genus.ljust(24).encode('Windows-1252')
	padSpecies = species.ljust(24).encode('Windows-1252')
	newRecord = bytes1 + species_number + namelen_byte + padName + statebits + genuslen_byte + padGenus + specieslen_byte + padSpecies + bytes4

	fh.write(newRecord)

fh.close()
