import sys

gold_standard_file = sys.argv[1]
EM_alignment_file = sys.argv[2]

f1 = open(gold_standard_file, 'r')
f2 = open(EM_alignment_file, 'r')

total_count = 0
matched_count = 0

gold_eng = f1.readline()
em_eng = f2.readline()
gold_jap = f1.readline()
em_jap = f2.readline()
gold_align = f1.readline()
em_align = f2.readline()
while gold_align != None and gold_align != '' and em_align != None and em_align != '':
	gold_seq = gold_eng.split()
	em_seq = em_eng.split()
	if len(gold_seq) != len(em_seq):
]		total_count += len(gold_seq)
	else:
		i = 0
		while i < len(em_seq):
			if gold_seq[i] == em_seq[i]:
				matched_count += 1
			total_count += 1
			i += 1
	gold_eng = f1.readline()
	em_eng = f2.readline()
	gold_jap = f1.readline()
	em_jap = f2.readline()
	gold_align = f1.readline()
	em_align = f2.readline()
f1.close()
f2.close()

print "Alignment accuracy: " + str( float( float(matched_count) / float(total_count) ) )
