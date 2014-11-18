README.txt

Files included:
Scripts:
- main.py
- count_rules.py
- parse.py

Output files (in output folder):
- dev.parses and dev.parses.post -> Parser output for development set without any modifications
- dev_modification1.parses and dev_modification1.parses.post -> Parser output for development set using first modification
- dev_modification2.parses and dev_modification2.parses.post -> Parser output for development set using second modification
- dev_modification3.parses and dev_modification3.parses.post -> Parser output for development set using third modification
- dev_modification_123.parses and dev_modification_123.parses.post -> Parser output for development set using all modifications
- test_modification_123.parses and test_modification_123.parses.post -> Parser output for test set using all modifications (final parser)

Usage:
1. Generate .parsers output:
	python main.py <training_file_preprocessed_unknown> <output_file_parse_rules> <input_strings_to_parse> <parsed_tree_output> <use_modification_1> <use_modification_2> <use_modification_3>
	Eg: python main.py train.trees.pre.unk parseRules dev.strings dev_modification_123.parses True True True

2. Postprocess Tree output:
	python postprocess.py <parsed_tree_output> <postprocessed_parsed_tree_output>
	Eg: python postprocess.py dev_modification_123.parses > dev_modification_123.parses.post

3. Evaluate parser output against gold standard:
	python eval.py <postprocessed_parsed_tree_output> <given_parsed_trees>
	Eg: python eval.py dev_modification_123.parses.post dev.trees
