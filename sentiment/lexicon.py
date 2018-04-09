from nltk.tokenize import word_tokenize
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