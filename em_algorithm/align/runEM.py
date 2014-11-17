import sys
import legal_alignments
import em_algorithm

# Input file has text from both files without alignment
input_file = sys.argv[1]
# Output file has text along with alignments
output_alignment_file = sys.argv[2]
# Number of iterations of EM to run
em_iterations = int(sys.argv[3])
# Output probabilities of phoneme pairs
prob_file = sys.argv[4]
# If >0, print decoding after each iteration for the first n word pairs
num_alignments = int(sys.argv[5])

f = open(input_file, 'r')
eng_line = f.readline()
jap_line = f.readline()
blank_line = f.readline()
while jap_line != None and jap_line != '':
	em_algorithm.addWordPair(eng_line, jap_line)
	eng_line = f.readline()
	jap_line = f.readline()
	blank_line = f.readline()
f.close()

# For EM
em_algorithm.EM(em_iterations, num_alignments)
outf = open(output_alignment_file, 'w')
f = open(input_file, 'r')
eng_line = f.readline()
jap_line = f.readline()
blank_line = f.readline()
while jap_line != None and jap_line != '':
	alignment = em_algorithm.getALignment(eng_line, jap_line)
	outf.write(eng_line)
	outf.write(jap_line)
	if alignment != None:
		outf.write(alignment + "\n")
	else:
		outf.write(blank_line)
	eng_line = f.readline()
	jap_line = f.readline()
	blank_line = f.readline()
f.close()
outf.close()

em_algorithm.printPhonemeProbabilities(prob_file)
