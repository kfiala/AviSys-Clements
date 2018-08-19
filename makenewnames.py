# Prepare the NEWNAMES11.AVI file from NEWNAMES.AVI.CSV

import csv

INPUT = 'NEWNAMES11.AVI.CSV'
OUTPUT = 'NEWNAMES11.AVI'

f = open(OUTPUT,'wb')

counter = 0;

try:
	with open(INPUT,newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			oldname = row[0]
			newname = row[1]
			if (oldname == '#'):
				continue

			oldlenInt = len(oldname)
			oldlenBin = oldlenInt.to_bytes(1, byteorder='little')
			newlenInt = len(newname)
			newlenBin = newlenInt.to_bytes(1, byteorder='little')

			counter+=1
			if counter > 149:
				print("Warning: limit of 149 names exceeded at",oldname,newname)
				counter-=1
				break

			print(oldlenInt, oldname.ljust(40), newlenInt, newname.ljust(40))
			f.write(oldlenBin)
			f.write(str.encode(oldname.ljust(40)))
			f.write(newlenBin)
			f.write(str.encode(newname.ljust(40)))
	print("Processed", counter,"names")
except:
	print("Problem reading",INPUT)
