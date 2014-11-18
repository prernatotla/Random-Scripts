rules_dictionary = {}
rules_probability = {}
tree_rules_dictionary = {} # root -> left_child -> right_child
terminal_words = []

def countRules(input_filename):
	f = open(input_filename, 'r')
	line = f.readline()
	while line != None and line != '':
		line = line.strip()
		if line[0] != '(' and line[-1] != ')':
			print "Tree string is not formatted correctly - root sentence not enclosed in ()"
			line = f.readline()
			continue
		# Strip first ( and last )
		line = line[1:-1]
		root = line.split(' ',1)[0]
		line = (line.split(' ',1)[1]).strip()
		parseBrackets(line, root)
		line = f.readline()
	f.close()

def parseBrackets(treeString, root):
	child1 = ""
	child2 = ""
	if treeString.count('(') == treeString.count(')') == 0:
		root = root.strip()
		treeString = treeString.strip().lower()
		# Found terminal word, store
		if treeString not in terminal_words and treeString != '<unk>':
			terminal_words.append(treeString)
		# Terminal rule
		if root in rules_dictionary:
			if treeString in rules_dictionary[root]:
				rules_dictionary[root][treeString] += 1
			else:
				rules_dictionary[root][treeString] = 1
		else:
			rules_dictionary[root] = {}
			rules_dictionary[root][treeString] = 1
	elif treeString.count('(') == treeString.count(')') == 1:
		treeString = treeString[1:-1]
		parseBrackets(treeString.split()[1], treeString.split()[0])
	else:
		splitString = treeString.replace(')', ')::')
		splitString = splitString.split('::')
		i = 0
		split1 = None
		split2 = None
		while i<len(splitString)-1:
			split1 = ' '.join(splitString[:i])
			split2 = ' '.join(splitString[i:])
			if split1.count('(') == split1.count(')') and split1.count('(') > 0 and split2.count('(') > 0:
				break
			else:
				split1 = None
				split2 = None
			i += 1
		split1 = split1.strip()
		split2 = split2.strip()
		if split1 == None and split2 == None:
			print "No split point found"
		else:
			split1 = split1.strip()
			split1 = split1[1:-1]
			child1 = split1.split(' ',1)[0]
			parseBrackets(split1.split(' ',1)[1], split1.split(' ',1)[0])
			split2 = split2.strip()
			split2 = split2[1:-1]
			child2 = split2.split(' ',1)[0]
			parseBrackets(split2.split(' ',1)[1], split2.split(' ',1)[0])
			root = root.strip()
			child1 = child1.strip()
			child2 = child2.strip()
			# Non-terminal rule
			child_string = child1 + ' ' + child2
			if root in rules_dictionary:
				if child_string in rules_dictionary[root]:
					rules_dictionary[root][child_string] += 1
				else:
					rules_dictionary[root][child_string] = 1
			else:
				rules_dictionary[root] = {}
				rules_dictionary[root][child_string] = 1

def calculateRuleProbabilities():
	for root_tag in rules_dictionary:
		rules_probability[root_tag] = {}
		total = 0
		for tag in rules_dictionary[root_tag]:
			total += rules_dictionary[root_tag][tag]
		for tag in rules_dictionary[root_tag]:
			rules_probability[root_tag][tag] = float( float(rules_dictionary[root_tag][tag]) / float(total) )

def printAllRules(output_file):
	f = open(output_file, 'w')
	for root_tag in rules_probability:
		for tag in rules_probability[root_tag]:
			f.write(root_tag + ' -> ' + tag + ' # ' + str(rules_probability[root_tag][tag]) + '\n')
	f.close()

def createTreeOfRules():
	for root_tag in rules_probability:
		tree_rules_dictionary[root_tag] = {}
		for tag in rules_probability[root_tag]:
			tags = tag.split()
			left_tag = tags[0]
			right_tag = "_" #No right child (terminal node)
			if len(tags) > 1:
				right_tag = tags[1]
			if left_tag in tree_rules_dictionary[root_tag]:
				if right_tag not in tree_rules_dictionary[root_tag][left_tag]:
					tree_rules_dictionary[root_tag][left_tag][right_tag] = rules_probability[root_tag][tag]
			else:
				tree_rules_dictionary[root_tag][left_tag] = {}
				tree_rules_dictionary[root_tag][left_tag][right_tag] =  rules_probability[root_tag][tag]


