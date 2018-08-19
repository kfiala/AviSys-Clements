# Jerry Blinn's simple encryption method

import sys

if len(sys.argv) < 3:   # No command line option
	if len(sys.argv) < 2:
		print("Specify filename and encode or decode")
	else:
		print("Specify encode or decode")
	raise SystemExit

filename = sys.argv[1]
function = sys.argv[2].upper()

outfile = open(filename+'.jerry','wb')

if function == 'ENCODE':
	decode = 0
	infile = open(filename,'r')
elif function == 'DECODE':
	decode = 1
	infile = open(filename,'rb')
else:
	print("Specify encode or decode")
	raise SystemExit

for line in infile:
	output = bytearray('',encoding='ascii')

	if decode==0:
		input = line[0:-1]	# Remove newline (CRLF)
		input = input.encode('Windows-1252') # encode converts string to byte array
	else:
		input = line[0:-2]	# Remove newline (CRLF)

	# Add (or subtract) a masking number to each character.
	# On each line, the masking number starts out as 13 and increases by 3 until it reaches 40, when it resets to 10.
	mask = 10
	for ch in input:
		ch = int(ch)

		mask = mask + 3
		if mask == 40:
			mask = 10

		if decode:
			ch = ch - mask
			if ch < 0:
				ch = 256 + ch
		else:
			ch = ch + mask
			if ch >= 256:
				ch = ch - 256

		output.append(ch)
	output.append(13)
	output.append(10)
	outfile.write(output)
outfile.close()
