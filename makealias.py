# Create an AviSys alias file (Walias.avi or Alias.avi)
import sys
import csv

folder = 'jump tables\\'

# Get command line args: WORLD/N.A., option
if len(sys.argv) > 1:
	geo = sys.argv[1].upper()
	if len(sys.argv) > 2:
		option = sys.argv[2].upper()
	else:
		option = ''
else:
	geo = ''

if geo == 'ABA' or geo == 'NA':
	geo = 'N.A.'
if geo != 'WORLD' and geo != 'N.A.':
	print("Specify WORLD or N.A.")
	raise SystemExit

if option != '' and option != 'BLANKS':
	print(option,"is not a valid option. Maybe 'BLANKS'?")
	raise SystemExit

if option == 'BLANKS':
	pad = ' '
else:
	pad = chr(0)


if geo == 'WORLD':
	l1 = 19
	l2 = 30
	infile = folder + 'Walias.input.csv'
	avifile = folder + 'Walias.avi'
	minlen = 51*21	# 1071 
else:
	l1 = 18
	l2 = 18
	infile = folder + 'Alias.input.csv'
	avifile = folder + 'Alias.avi'
	minlen = 38*30	# 1140 

translation_table = str.maketrans('\\', ' ')
binary = bytearray()
with open(infile,newline='') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		alias = row[0]
		name = row[1]
		if alias[0:1] == '*':
			continue	# comment
		alen = len(alias)
		nlen = len(name)
		name = name.translate(translation_table)	# support for leading blanks

		binary.append(alen)
		binary.extend(alias.ljust(l1,pad).encode('Windows-1252'))
		binary.append(nlen) 
		binary.extend(name.ljust(l2,pad).encode('Windows-1252'))

length = len(binary)
while length < minlen:
	binary.append(0)
	length += 1

f = open(avifile,'wb')
f.write(binary)
f.close()