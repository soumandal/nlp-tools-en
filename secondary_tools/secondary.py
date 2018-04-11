# Input  : Sentence - Sentence in which word location is to be found out
#          Word - Word for which location is to be found in the sentence
# Output : Location of word in sentence

# Algorithm
# Step 01 - Input sentence and word
# Step 01 - Divide sentence into three parts
# Step 02 - If word is in part one return 1, end
# Step 03 - If word is in part two return 2, end
# Step 04 - If word is in part three return 3, end
# Step 05 - Else return 0, end

from nltk.tokenize import word_tokenize

def word_region(sentence, word):

    tokens = word_tokenize(sentence)

    part_one = tokens[:len(tokens)//3]  # 0 -> len/3
    part_two = tokens[len(tokens)//3:2*len(tokens)//3]  # len/3 -> 2*len/3
    par_three = tokens[2*len(tokens)//3:]  # 2*len/3 -> end

    if word in part_one:
        return 1
    elif word in part_two:
        return 2
    elif word in par_three:
        return 3
    else:
    	return 0