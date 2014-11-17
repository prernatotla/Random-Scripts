def getValidAlignments(eng_len, jap_len):
	allAlignments = []
	#print eng_len, jap_len
	if eng_len>0 and jap_len>0 and jap_len>=eng_len:
		if eng_len == 1:
			allAlignments.append([1]*jap_len)
			return allAlignments
		i = 1
		while i<jap_len:
			subAlignments = getValidAlignments(eng_len-1, jap_len-i)
			for sub_align in subAlignments:
				#print sub_align
				align = [1]*jap_len
				j = 0
				while j<len(sub_align):
					align[i+j] = sub_align[j]+1
					j += 1
				allAlignments.append(align)
			i += 1
	return allAlignments

def printAllValidAlignments(eng, jap):
	eng = eng.replace('\"', '')
	eng_seq = eng.split()
	jap = jap.replace('"', '')
	jap_seq = jap.split()
	allAlignments = getValidAlignments(len(eng_seq), len(jap_seq))
	# Print output
	print eng_seq, jap_seq
	for alignment in allAlignments:
		print alignment
	print ""
