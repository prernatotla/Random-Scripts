import legal_alignments

phoneme_counts = {}
phoneme_probabilities = {}
word_pairs = []

# Returns a space-seperated string given an array
def getStringFromArray(seq):
	ret_string = ""
	for phoneme in seq:
		ret_string += phoneme + " "
	ret_string = ret_string.strip()
	return ret_string

# Get all associated word pairs. Each pair has an English sequence of phonemes and it's associated Japanese sequence
def addWordPair(eng_line, jap_line):
	eng_line = eng_line.replace('"', '')
	eng_seq = eng_line.split()
	jap_line = jap_line.replace('"', '')
	jap_seq = jap_line.split()
	word_pairs.append({'eng':eng_seq, 'jap':jap_seq})

def getJapaneseSequence(alignment, jap_seq, index):
	seq = []
	i = 0
	while i<len(jap_seq):
		if alignment[i] == index:
			seq.append(jap_seq[i])
		i += 1
	return seq

# Get the probability that a given English-Japanese sequence pair has a certain alignment
def getAlignmentProbability(eng_seq, jap_seq, alignment):
	probability = 1
	i = 0
	while i<len(eng_seq):
		eng_phoneme = eng_seq[i]
		jap_phoneme = getStringFromArray( getJapaneseSequence(alignment,jap_seq,i+1) )
		prob_jap_eng = 0
		if eng_phoneme in phoneme_probabilities and jap_phoneme in phoneme_probabilities[eng_phoneme]:
			prob_jap_eng = phoneme_probabilities[eng_phoneme][jap_phoneme]
		probability *= prob_jap_eng
		i += 1
	return probability

# Append fractional counts of phoneme pairs calculated from a given word pair 
def getFractionalCounts(eng_seq, jap_seq, iteration):
	# get all valid alignments
	allAlignments = legal_alignments.getValidAlignments(len(eng_seq), len(jap_seq))
	# get probability of all alignments
	align_probabilities = []
	normalized_align_probabilities = []
	for alignment in allAlignments:
		if iteration == 0:
			prob = float(1/ float(len(allAlignments)))
			normalized_align_probabilities.append(prob)
		else:
			prob = getAlignmentProbability(eng_seq, jap_seq, alignment)
			align_probabilities.append(prob)
	# normalize probabilities
	if iteration > 0:
		total_prob = 0
		for prob in align_probabilities:
			total_prob += prob
		for prob in align_probabilities:
			prob = float(float(prob) / float(total_prob))
			normalized_align_probabilities.append(prob)
	# increment fractional counts
	i = 0
	while i<len(allAlignments):
		j = 0
		while j<len(eng_seq):
			eng_phoneme = eng_seq[j]
			jap_phoneme = getStringFromArray( getJapaneseSequence(allAlignments[i], jap_seq, j+1) )
			if eng_phoneme in phoneme_counts:
				if jap_phoneme in phoneme_counts[eng_phoneme]:
					phoneme_counts[eng_phoneme][jap_phoneme] += normalized_align_probabilities[i]
				else:
					phoneme_counts[eng_phoneme][jap_phoneme] = normalized_align_probabilities[i]
			else:
				phoneme_counts[eng_phoneme] = {}
				phoneme_counts[eng_phoneme][jap_phoneme] = normalized_align_probabilities[i]
			j += 1
		i += 1

# Normalize fractional counts to get fractional probabilities
def getFractionalProbabilities():
	for eng_phoneme in phoneme_counts:
		total_count = 0
		for jap_seq in phoneme_counts[eng_phoneme]:
			total_count += phoneme_counts[eng_phoneme][jap_seq]
		for jap_seq in phoneme_counts[eng_phoneme]:
			prob = float(float(phoneme_counts[eng_phoneme][jap_seq]) / float(total_count))
			if eng_phoneme in phoneme_probabilities:
				phoneme_probabilities[eng_phoneme][jap_seq] = prob
			else:
				phoneme_probabilities[eng_phoneme] = {}
				phoneme_probabilities[eng_phoneme][jap_seq] = prob

# main function to run EM algorithm
def EM(max_iterations, num_output):
	iteration = 0
	while iteration < max_iterations:
		print "********************** ITERATION " + str(iteration+1) + " **********************"
		for eng_phoneme in phoneme_counts:
			for jap_str in phoneme_counts[eng_phoneme]:
				phoneme_counts[eng_phoneme][jap_str] = 0
		for pair in word_pairs:
			getFractionalCounts(pair['eng'], pair['jap'], iteration)
		getFractionalProbabilities()
		printed_index = 0
		while printed_index < num_output:
			word_pair = word_pairs[printed_index]
			eng_line = getStringFromArray(word_pair['eng'])
			jap_line = getStringFromArray(word_pair['jap'])
			alignment = getALignment(eng_line, jap_line)
			if alignment != None:
				print "English word: " + eng_line
				print "Japanese word: " + jap_line
				print "\tMost probable alignment: " + str(alignment)
			printed_index += 1
		iteration += 1

# Get the most probable alignment given phoneme probabilities
def getALignment(eng_line, jap_line):
	eng_line = eng_line.replace('\"', '')
	eng_seq = eng_line.split()
	jap_line = jap_line.replace('"', '')
	jap_seq = jap_line.split()
	allAlignments = legal_alignments.getValidAlignments(len(eng_seq), len(jap_seq))
	max_prob = 0
	max_prob_align = None
	for alignment in allAlignments:
		prob = getAlignmentProbability(eng_seq, jap_seq, alignment)
		if prob > max_prob:
			max_prob = prob
			max_prob_align = alignment
	if max_prob > 0:
		max_prob_align_str = ""
		for i in max_prob_align:
			max_prob_align_str += str(i) + " "
		max_prob_align_str.strip()
		return max_prob_align_str
	return None

# Print phoneme probabilities to a file (used to build WFST)
def printPhonemeProbabilities(output_file):
	f = open(output_file, 'w')
	for eng_phoneme in phoneme_probabilities:
		for jap_phoneme in phoneme_probabilities[eng_phoneme]:
			if phoneme_probabilities[eng_phoneme][jap_phoneme] >= 0.01:
				f.write('' + eng_phoneme + '|' + jap_phoneme + '|' + str(phoneme_probabilities[eng_phoneme][jap_phoneme]) + '\n')
	f.close()
