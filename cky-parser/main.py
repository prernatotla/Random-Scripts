import sys, time, math
import count_rules
import parse

input_filename = sys.argv[1]
output_file = sys.argv[2]

# Generate and store grammar
count_rules.countRules(input_filename)
rule_dictionary = count_rules.rules_dictionary
count_rules.calculateRuleProbabilities()
rules_probability = count_rules.rules_probability
count_rules.printAllRules(output_file)
count_rules.createTreeOfRules()
tree_rules = count_rules.tree_rules_dictionary
terminal_words = count_rules.terminal_words

# Parsing sentences
data_file = sys.argv[3]
parsed_output = sys.argv[4]

addNP = sys.argv[5]
if addNP == "True":
	addNP = True
else:
	addNP = False
changePreprocess = sys.argv[6]
if changePreprocess == "True":
	changePreprocess = True
else:
	changePreprocess = False
addRulesManually = sys.argv[7]
if addRulesManually == "True":
	addRulesManually = True
else:
	addRulesManually = False

f = open(data_file, 'r')
outf = open(parsed_output, 'w')
sentence = f.readline()
while sentence != None and sentence != '':
	parse.parse_array = {}
	start_time = time.time()
	parse.addNP = addNP
	parse.changePreprocess = changePreprocess
	parse.addRulesManually = addRulesManually
	parsedSentence = parse.parseSentence(tree_rules, sentence, terminal_words)
	timeTaken = math.log(time.time() - start_time)
	sen_length = math.log(len(sentence.split()))
	outf.write(parsedSentence + "\n")
	sentence = f.readline()
	break
f.close()
outf.close()
