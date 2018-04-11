from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


def get_pos_tag(sentence, word):

    for pairs in pos_tag(word_tokenize(sentence, language="English")):
        if pairs[0] == word:
            return pairs[1]

    return "NA"