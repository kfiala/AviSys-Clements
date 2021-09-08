# Create the bandcode files
# Input files:
masterEDT = 'master.edt'
EXCEPTIONS = 'bandcode.exceptions.csv'
# Output files:
BANDSEL = 'BANDSEL.new.AVI'
BANDCODE = 'BANDCODE.new.AVI'
bandcode = {}
# Read through MASTER.EDT and pick out North American species
for line in open(masterEDT).readlines():
	if not ',W,' in line and not ',N,0\n' in line:	# Exclude World species and all family entries.
		# Get common name and break it down into lowercase words
		name = line.split(',')[0]
		name = name.strip()                       # e.g., Eastern Screech-Owl
		lower = name.lower()                      # eastern screech-owl
		words = lower.replace('-',' ')            # eastern screech owl
		words = words.split(' ')                  # ['eastern', 'screech', 'owl']
		count = len(words)                        # 3
		# Generate a band code
		if count == 1:
			code = words[0][0:4]
		elif count == 2:
			code = words[0][0:2] + words[1][0:2]
		elif count == 3:
			name = name.split(' ')
			if len(name) > 1 and '-' in name[1]:
				code = words[0][0:2] + words[1][0:1] + words[2][0:1]  # easo eastern screech-owl
			else:
				code = words[0][0:1] + words[1][0:1] + words[2][0:2]  # rwbl red-winged blackbird
		else:
			code = words[0][0:1] + words[1][0:1] + words[2][0:1] + words[3][0:1]

		if code in bandcode:
			bandcode[code].append(lower)
		else:
			bandcode[code] = [lower]
# At this point, bandcode[] has an array for each generated band code.
# The array may contain a unique species or multiple species having the same generated band code.
# Make a simple list of the band codes in codes.
codes = list(bandcode.keys())
codes.sort()

f = open(BANDSEL,'w')
for code in codes:
	if len(bandcode[code]) > 1:
		for lower in bandcode[code]:
			f.write(code + ' ' + lower + '\n')
			code = '    '
		f.write('-\n')
f.close()


# Process the list of alternative codes that resolve collisions
import csv
specials = {}
started = False
with open(EXCEPTIONS) as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		if not started:	# skip header row
			started = True
			continue
		if not row:	# skip empty row
			continue
		else:
			basecode = row[0].strip()
		if not basecode:
			continue
		species = row[1].strip()
		if basecode in codes:
			if basecode not in bandcode:
				print(basecode,'is listed as a duplicate in',EXCEPTIONS,'but is not currently a duplicate code; skipping')
				continue
			dups = bandcode[basecode]
			if species in dups:
				offset = dups.index(species)
				del bandcode[basecode][offset]
				dups = bandcode[basecode]
				if len(dups) == 0:
					del bandcode[basecode]
				for code in row[2:]:
					code.strip()
					if code:
						specials[code] = species
					else:
						continue

			else:
				print(basecode,species,"was found in",EXCEPTIONS,"but is no longer in the taxonomy.")
		else:
			print(basecode,"was found in",EXCEPTIONS,"but is no longer a valid code.")

for code in specials:
	bandcode[code] = [specials[code]]

codes = list(bandcode.keys())
codes.sort()

outfile = open(BANDCODE,'w')

for code in codes:
	name = bandcode[code]
	if name:
		outfile.write(code + ' ' + name[0] + '\n')
outfile.close()	
