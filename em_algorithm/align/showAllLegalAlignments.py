import sys
import legal_alignments

input_file = sys.argv[1]
num_input = int(sys.argv[2])

f = open(input_file, 'r')
index = 0
line_count = 0
eng_line = f.readline()
jap_line = f.readline()
blank_line = f.readline()
i = 0
while i<num_input and blank_line != None and blank_line != '':
	legal_alignments.printAllValidAlignments(eng_line, jap_line)
	eng_line = f.readline()
	jap_line = f.readline()
	blank_line = f.readline()
	i += 1
f.close()