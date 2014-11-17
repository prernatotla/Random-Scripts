Files included:
- legal_alignments.py -> Given the number of phonemes in the English and Japanese sequence, gets all possible valid legal alignments.
- showAllLegalAlignments.py -> Main file to run legal_alignments.py
- em_algorithm.py -> All function needed to run EM algorithm of phoneme sequence alignment
- runEM.py -> Runs the EM algorithm for specified input file
- alignmentAccuracy.py -> Measures the accuracy of learned alignments with gold standard

Commands:
1. To print all legal alignments of word pairs from a file
python showAllLegalAlignments.py <unsupervised_data_file> <top_n_word_pairs_to_display>

2. To run EM algorithm
python runEM.py <input_unsupervised_data_file> <output_alignment_file> <number_of_iterations> <output_probability_phoneme_mapping_file> <number_of_word_pair_alignments_to_display>
In the above command, if the number of word pair alignments to display is <= 0, the files will be created but no alignments will be printed to console output.

3. To measure accuracy of alignment
python alignmentAccuracy.py <gold_standard_alignment_file> <learned_alignment_file>
