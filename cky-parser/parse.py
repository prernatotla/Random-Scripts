import math

parse_array = {}
addNP = False
changePreprocess = False
transformGrammar = False
addRulesManually = False

def initializeParseArray(word_array):
	length = len(word_array)
	for i in range(0,length):
		parse_array[i] = {}
		for j in range(i, length):
			# Each tag in tags will have tag,probability,back_pointer_index,back_pointer_tag
			parse_array[i][j] = {'word':None, 'tags':[]}
	for i in range(0,length):
		parse_array[i][i]['word'] = word_array[i].lower()
		
def parseSentence(grammar, sentence, terminal_words):
	words = sentence.split()
	lowercase_words = []
	for word in words:
		lowercase_words.append(word.lower())
	words = lowercase_words
	sen_len = len(words)
	words = replaceUnknown(words, terminal_words)
	initializeParseArray(words)
	if addRulesManually == True:
		grammar = addGrammarRules(grammar)
	for i in range(1, sen_len+1):
		generateTags(grammar, i)
	treeString = getTreeString(0,sen_len-1, 'TOP')
	if addNP == True and treeString == "":
		initializeParseArray(words)
		for i in range(0,sen_len):
			parse_array[i][i]['tags'].append({'tag':'NP', 'probability':math.log(0.001), 'back_pointer_index':-1, 'back_pointer_left_tag':None, 'back_pointer_right_tag':None})
	for i in range(1, sen_len+1):
		generateTags(grammar, i)
	treeString = getTreeString(0,sen_len-1, 'TOP')
	print parse_array[0][sen_len-1]['tags']
	return treeString

def addGrammarRules(grammar):
	if 'VBZ' in grammar:
		if '\'s' not in grammar['VBZ']:
			grammar['VBZ']['\'s'] = {}
			grammar['VBZ']['\'s']['_'] = 0.001
	return grammar

def replaceUnknown(words, terminal_words):
	processed_words = []
	for word in words:
		if word in terminal_words:
			processed_words.append(word)
		else:
			processed_words.append('<unk>')
	return processed_words

def getTagsFromGrammar(grammar, left, right):
	tags = []
	if right == None:
		right = '_'
	for tag in grammar:
		if left in grammar[tag]:
			if right in grammar[tag][left]:
				prob = math.log(grammar[tag][left][right])
				tags.append({'tag':tag, 'probability':prob, 'back_pointer_index':-1, 'back_pointer_left_tag':None, 'back_pointer_right_tag':None})
	return tags

def generateTags(grammar, length):
	for i in range(0,len(parse_array)-length+1):
		if length == 1:
			tags = getTagsFromGrammar(grammar, parse_array[i][i]['word'], None)
			for tag in tags:
				parse_array[i][i]['tags'].append(tag)
			if changePreprocess == True:
				for tag in tags:
					if '_' in tag['tag']:
						subtags = tag['tag'].split('_')
						for subtag in subtags:
							found = False
							for tag2 in tags:
								if tag2['tag'] == subtag:
									found = True
							if found == False:
								newTag = {'tag':subtag, 'probability':math.log(0.0001), 'back_pointer_index':tag['back_pointer_index'], 'back_pointer_left_tag':tag['back_pointer_left_tag'], 'back_pointer_right_tag':tag['back_pointer_right_tag']}
								parse_array[i][i]['tags'].append(newTag)
			# end if changePreprocess
		else:
			tags = []
			for j in range(i+1, i+length):
				left_tags = parse_array[i][j-1]['tags']
				right_tags = parse_array[j][i+length-1]['tags']
				for left in left_tags:
					for right in right_tags:
						temp_tags = getTagsFromGrammar(grammar, left['tag'], right['tag'])
						for temp_tag in temp_tags:
							temp_tag['back_pointer_index'] = j
							temp_tag['back_pointer_left_tag'] = left['tag']
							temp_tag['back_pointer_right_tag'] = right['tag']
							#prob = temp_tag['probability'] * left['probability'] * right['probability']
							prob = temp_tag['probability'] + left['probability'] + right['probability']
							temp_tag['probability'] = prob
							found = False
							for tag in tags:
								if tag['tag'] == temp_tag['tag']:
									found = True
									if temp_tag['probability'] > tag['probability']:
										tags.remove(tag)
										tags.append(temp_tag)
							if found == False:
								tags.append(temp_tag)
			for tag in tags:
				parse_array[i][i+length-1]['tags'].append(tag)
			if changePreprocess == False:
				for tag in tags:
					if '_' in tag['tag']:
						subtags = tag['tag'].split('_')
						for subtag in subtags:
							found = False
							for tag2 in tags:
								if tag2['tag'] == subtag:
									found = True
							if found == False:
								prob = tag['probability'] + math.log(0.01)
								newTag = {'tag':subtag, 'probability':prob, 'back_pointer_index':tag['back_pointer_index'], 'back_pointer_left_tag':tag['back_pointer_left_tag'], 'back_pointer_right_tag':tag['back_pointer_right_tag']}
								parse_array[i][i+length-1]['tags'].append(newTag)

def getTreeString(i,j,parent_tag):
	treeString = ""
	tags = parse_array[i][j]['tags']
	for tag in tags:
		if tag['tag'] == parent_tag:
			back_pointer = tag['back_pointer_index']
			if back_pointer == -1:
				# Terminal case
				treeString = "(" + parent_tag + " " + parse_array[i][j]['word'] + ")"
			else:
				# left -> i, back_pointer-1 ; right -> back_pointer, j-1
				left_child = tag['back_pointer_left_tag']
				left_treeString = getTreeString(i, back_pointer-1, left_child)
				right_child = tag['back_pointer_right_tag']
				right_treeString = getTreeString(back_pointer, j, right_child)
				treeString = "(" + parent_tag + " " + left_treeString + " " + right_treeString + ")"
			break
	return treeString

