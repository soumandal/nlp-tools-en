from nltk.tokenize import word_tokenize
import numpy
import pickle
import math

# polarity tag
#
# neu - 0
# pos - 1
# neg - 2

with open("ADJ_SOCAL.pkl", "rb") as f:
    ADJ = pickle.load(f)

with open("ADV_SOCAL.pkl", "rb") as f:
    ADV = pickle.load(f)

with open("NOU_SOCAL.pkl", "rb") as f:
    NOU = pickle.load(f)

with open("VRB_SOCAL.pkl", "rb") as f:
    VRB = pickle.load(f)

with open("INT_SOCAL.pkl", "rb") as f:
    INT = pickle.load(f)


def SOCAL_SCORE(word):
    for x in range(4):
        MAX = 0
        if word in ADJ:
            MAX = int(ADJ[word][0])
        if word in ADV:
            if math.fabs(int(ADV[word][0])) > math.fabs(MAX):
                MAX = int(ADV[word][0])
        if word in NOU:
            if math.fabs(int(NOU[word][0])) > math.fabs(MAX):
                MAX = int(NOU[word][0])
        if word in VRB:
            if math.fabs(int(VRB[word][0])) > math.fabs(MAX):
                MAX = int(VRB[word][0])
        if word in INT:
            return float(INT[word][0])
    return MAX


def SOCAL(sen):
    tokens = word_tokenize(sen)
    SOCAL_DIS = []
    count = 0
    for word in tokens:
        try:
            SOCAL_DIS.append(SOCAL_SCORE(word))
        except KeyError:
            pass
    while count < len(SOCAL_DIS) - 1:
        if type(SOCAL_DIS[count]) == float and type(SOCAL_DIS[count + 1]) == int and SOCAL_DIS[count + 1] != 0:
            if SOCAL_DIS[count] > 0 and SOCAL_DIS[count + 1] > 0:
                SOCAL_DIS[count + 1] += SOCAL_DIS[count]
                SOCAL_DIS[count] = 0
                count += 2
                continue
            if SOCAL_DIS[count] < 0 and SOCAL_DIS[count + 1] > 0:
                SOCAL_DIS[count + 1] += SOCAL_DIS[count]
                SOCAL_DIS[count] = 0
                count += 2
                continue
            if SOCAL_DIS[count] > 0 and SOCAL_DIS[count + 1] < 0:
                SOCAL_DIS[count + 1] -= SOCAL_DIS[count]
                SOCAL_DIS[count] = 0
                count += 2
                continue
            if SOCAL_DIS[count] < 0 and SOCAL_DIS[count + 1] < 0:
                SOCAL_DIS[count + 1] = math.fabs(SOCAL_DIS[count] + SOCAL_DIS[count + 1])
                SOCAL_DIS[count] = 0
                count += 2
                continue
        count += 1
    if sum(SOCAL_DIS) > 0:
        return 1
    if sum(SOCAL_DIS) < 0:
        return 2
    return 0



positive_emoticons = ['😏', '😬', '😀', '😆', '😃', '😄', '😉', '😁', '😍', '😙', '😚', '😅', '😘', '😗', '🙂', '😊', '🙃', '😂', '😋', '🤗', '😜', '😛', '😝', '🤑', '😌', '\U0001f920', '😇', '\U0001f923', '\U0001f921', '😎', '😮']
negative_emoticons = ['😣', '😖', '😓', '😭', '😢', '😒', '😩', '😑', '😞', '😔', '😫', '😩', '😪', '😟', '😠', '😡', '\U0001f925', '😨', '😧', '😦', '😰', '😕', '😐', '😪', '🤒', '😷', '\U0001f922', '👿', '😥', '🙄', '😱']

def emotion_score(sen):
    pos_count, neg_count = 0, 0
    for token in word_tokenize(sen):
        if token in positive_emoticons:
            pos_count += 1
        if token in negative_emoticons:
            neg_count += 1
    if pos_count == neg_count:
        return 0
    if pos_count > neg_count:
        return 1
    if neg_count > pos_count:
        return 2
    return 0

def emotiocon_location(sen):
    pos_loc, neg_loc = [], []
    tokens = word_tokenize(sen)
    for index, token in enumerate(tokens):
        if token in positive_emoticons:
            pos_loc.append(index)
            continue
        if token in negative_emoticons:
            neg_loc.append(index)
            continue
    if max(pos_loc + neg_loc) in pos_loc:
        return 1
    if max(pos_loc + neg_loc) in neg_loc:
        return 2
    return 0

def emotiocon_location_mean(sen):

    pos_loc, neg_loc = [], []
    tokens = word_tokenize(sen)
    for index, token in enumerate(tokens):
        if token in positive_emoticons:
            pos_loc.append(index)
            continue
        if token in negative_emoticons:
            neg_loc.append(index)
            continue
    if numpy.mean(pos_loc) == numpy.mean(neg_loc):
        return 0
    if numpy.mean(pos_loc) > numpy.mean(neg_loc):
        return 1
    if numpy.mean(neg_loc) > numpy.mean(pos_loc):
        return 2
    return 0


def check_character_emoticon(sentence):

    pos_char_emoticons = [":)", ":‑)", ":3", ":-3", ":]", ":-]",
                          ":>", ":->", "8)", "8-)", ":}", " :-}",
                          ":o)", ":c)", ":^)", "=]", "=)", " :-))",
                          ":D", ":‑D", "8D", "8‑D", "xD", "x‑D",
                          "XD", "X‑D", "=D", "=3", ":')", ":'‑)",
                          ":*", ":-*", ":×", ";)", ";‑)", "*)",
                          "*-)", ";]", ";‑]", ";^)", ":‑,", ";D",
                          ":P", ":‑P", "XP", "X‑P", "xp", "x‑p",
                          ":p", "=p", ">:P", "O:)", "O:‑)", "0:3",
                          "0:‑3", "0:)", "0:‑)", "0;^)", "|;‑)", "|‑O",
                          ":-)", "(:", ":p", "(Y)"]

    neg_char_emoticons = [":(", ":‑(", ":c", ":‑c", ":<", ":‑<",
                          ":[", ":‑[", ":-||", ">:[", ":{", ":@",
                          ">:(", ":'(", ":'‑(", "D‑':", "D:<", "D:",
                          "D8", "D;", "D=", "DX", ":/", ":‑/",
                          ":\\", "=/", "=\\", ":|", ":‑|", ":$",
                          ">:)", ">:‑)", "}:)", "}:‑)", "3:)", "3:‑)",
                          ":‑J", "%‑)", "%)", "<:‑|", "-_-", ":|",
                          ":'("]

    pos_count, neg_count = 0, 0
    tokens = word_tokenize(sentence)
    # token is emoticon
    for token in tokens:
        if token in pos_char_emoticons:
            pos_count += 1
        if token in neg_char_emoticons:
            neg_count += 1
    # 2 char emoticons
    for index, token in enumerate(tokens[:-1]):
        for pos_emoticon in pos_char_emoticons:
            if pos_emoticon == tokens[index] + tokens[index + 1]:
                pos_count += 1
    for index, token in enumerate(tokens[:-1]):
        for neg_emoticon in neg_char_emoticons:
            if neg_emoticon == tokens[index] + tokens[index + 1]:
                neg_count += 1
    # 3 char emoticons
    for index, token in enumerate(tokens[:-2]):
        for pos_emoticon in pos_char_emoticons:
            if pos_emoticon == tokens[index] + tokens[index + 1] + tokens[index + 2]:
                pos_count += 1
    for index, token in enumerate(tokens[:-2]):
        for neg_emoticon in neg_char_emoticons:
            if neg_emoticon == tokens[index] + tokens[index + 1] + tokens[index + 2]:
                neg_count += 1
    # 4 char emoticons
    for index, token in enumerate(tokens[:-3]):
        for pos_emoticon in pos_char_emoticons:
            if pos_emoticon == tokens[index] + tokens[index + 1] + tokens[index + 2] + tokens[index + 3]:
                pos_count += 1
    for index, token in enumerate(tokens[:-3]):
        for neg_emoticon in neg_char_emoticons:
            if neg_emoticon == tokens[index] + tokens[index + 1] + tokens[index + 2] + tokens[index + 3]:
                neg_count += 1

    return pos_count, neg_count
