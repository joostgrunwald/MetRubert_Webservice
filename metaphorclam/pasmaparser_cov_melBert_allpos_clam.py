##############
# dependencies#
##############
import warnings
from lxml import etree
from io import BytesIO
import os
import sys

##############
# USER INPUT #
##############
try:
    directory_name = sys.argv[1]
    main(directory_name)
except:
    print("no directory name was given")


#GLOBALS
sentence_number = 0
word_number = 0
sentence = ""

###########
# FUNCTIONS#
###########
warnings.filterwarnings("ignore")


def findpos(child_of_child):
    """ This function finds the right pos tag

    Args:
        child_of_child (xml element): the xml element to retrieve the postag from

    Returns:
        string: the pos tag saved in a capital string
    """
    # we maken een postag aan
    pos_tag = "empty"

    # ? Het correct taggen van werkwoorden, zelfstandige en bijvoeglijke naamwoorden.
    if "WW(" in child_of_child.get("postag"):
        pos_tag = "VERB"
    elif "N(" in child_of_child.get("postag"):
        pos_tag = "NOUN"
    elif "ADJ(" in child_of_child.get("postag"):
        pos_tag = "ADJ"

    # ? Het correct taggen van voornaamwoorden
    elif "VNW(" in child_of_child.get("postag") and "adv-pron" in child_of_child.get(
        "postag"
    ):
        pos_tag = "ADV"
    elif "VNW(" in child_of_child.get("postag") and "prenom" in child_of_child.get(
        "postag"
    ):
        pos_tag = "DET"
    elif (
        "VNW(" in child_of_child.get("postag")
        and "pron" in child_of_child.get("postag")
        and child_of_child.get("word").lower() != "het"
    ):
        pos_tag = "PRON"

    # ? Het correct taggen van bijwoorden, lidwoorden en nummers
    elif "BW(" in child_of_child.get("postag"):
        pos_tag = "ADV"
    elif "LID(" in child_of_child.get("postag"):
        pos_tag = "DET"

    return pos_tag


def writeoutput(pos, word, index, f, sentence):
    global word_number
    word_number = word_number + 1

    #! Calculate and write output
    if str(sentence) != "NONE" and sentence[:3] == "'' ":
        sentence = sentence[3:]
        index = str(int(index)-1)

    words = sentence.split()

    word = word.replace(" ","")
    word = word.replace(",,","")
    word = word.replace("''","")
    word = word.replace(",","")

    index = int(index)

    #check bounds of index
    if index < len(words):
        if words[index] == word:
            i = 1
        elif words[index] == word and index > 0 and words[index-1] == word:
            index = index - 1
        elif index + 1 < len(words) and words[index+1] == word:
            index += 1

        elif words[index] == word[1:]:
            i = 1
        elif index + 1 < len(words) and words[index+1] == word[1:]:
            index += 1
        elif index > 0 and words[index-1] == word[1:]:
            index = index - 1

        elif words[index].replace(",","") == word:
            index = index
        elif words[index].replace("\"","") == word:
            index = index
        elif words[index] == word.replace("\"",","):
            index = index
        elif words[index] == word.replace("\"",""):
            index = index

        elif index > 0 and words[index-1].replace(",","") == word:
            index = index - 1
        elif index > 0 and words[index-1].replace("\"","") == word:
            index = index - 1
        elif index > 0 and words[index-1] == word.replace("\"",","):
            index = index - 1
        elif index > 0 and words[index-1] == word.replace("\"",""):
            index = index - 1

        elif index + 1 < len(words) and words[index+1].replace(",","") == word:
            index += 1
        elif index + 1 < len(words) and words[index+1].replace("\"","") == word:
            index += 1
        elif index + 1 < len(words) and words[index+1] == word.replace("\"",","):
            index += 1
        elif index + 1 < len(words) and words[index+1] == word.replace("\"",""):
            index += 1

        elif words[index] == word[0:len(words[index])]:
            i = 1
        elif index > 0 and words[index-1] == word[0:len(words[index-1])]:
            index = index - 1
        elif index + 1 < len(words) and words[index+1] == word[0:len(words[index+1])]:
            index += 1

        elif words[index].replace(",","") == word.replace("\"",""):
            i = 1

        elif index > 0 and words[index-1].replace("'","") == word:
            index = index - 1

        elif index > 0 and words[index-1].replace("'","") == word.replace("'",""):
            index = index - 1

        elif index > 0 and words[index-1].replace("'","").replace(",","") == word:
            index = index - 1

            #else:
                #print(word)
                #print(words[index])
                #if index > 0:
                #    print(words[index-1])
                #print("OTHER CASE")
    elif index == len(words):
        index = index - 1

    output = "COV_fragment01" + " " + str(word_number) + "\t" + "0" + "\t" + sentence + "\t" + pos + "\t" + str(index)

    f.write(output + "\n")


def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


##################
# GLOBAL VARIABLES#
##################
def main(directory_name):
    sentence = ""

    filenumber = 0
    parser = etree.XMLParser(ns_clean=True, remove_comments=True)

    subdirectories = directory_name

    outputfile = f'{subdirectories}/dev.tsv'
    print(outputfile)

    with open(outputfile, "w", encoding="utf-8") as f:
        f.write("index      label   sentence        POS     w_index" + "\n")

        for alpino_file in os.listdir(subdirectories):
            if os.path.isdir(os.path.join(subdirectories, alpino_file)):

                dir = os.path.join(subdirectories, alpino_file)

                for filename in os.listdir(dir):
                    if filename.endswith(".xml"):

                        filenumber = filenumber + 1

                        filedirectory = f'{dir}/{filename}'
                        tree = etree.parse(filedirectory, parser)
                        root = tree.getroot()

                        sentence = ""

                                            ############################################
                                            # PART 1: get obj subj verb and sent number #
                                            ############################################
                        for alpino_ds in root.iter("alpino_ds"):
                            for top in alpino_ds:

                                # We test the sentence id's
                                sent_id = top.get("sentid")
                                if str(sent_id) != "None":
                                    sentence = top.text

                                    # ? Fix the sentence we just received
                                    # escape csv problems
                                    sentence = sentence.replace("\n", "")
                                                                    # sentence fixes
                                    if sentence[:1] == " ":
                                        sentence = sentence[1:]

                                    if sentence[:1] == " ":
                                        sentence = sentence[1:]

                                    if sentence[:1] == " ":
                                        sentence = sentence[1:]

                                    sentence = sentence.replace("''", "")

                                    sentence = sentence.replace(" ,,", " ")

                                    sentence = sentence.replace(",,", " ")

                                    sentence = sentence.replace("\"", "")

                                    sentence = sentence.replace(" , ", ", ")

                                    sentence = sentence.replace(" \\ ", "\\")

                                    sentence = sentence.replace(" / ","/")

                                    sentence = sentence.replace(" :",":")

                                    sentence = sentence.replace(",, ","")

                                    if sentence[:1] == " ":
                                        sentence = sentence[1:]

                                    sentence = sentence.replace(" , ", ", ")
                                    sentence = sentence.replace(" ; ", "; ")
                                    sentence = sentence.replace(" .", ".")
                                    sentence = sentence.replace(" : ", ": ")
                                    sentence = sentence.replace(" ( ", " (")
                                    sentence = sentence.replace(" ) ", ") ")
                                    sentence = sentence.replace(" )", ")")
                                    sentence = sentence.replace(" ',", "',")
                                    if sentence[:2] == "' ":
                                        sentence = "'" + sentence[2:]

                                    qtcount = sentence.count(" ' ")
                                    if qtcount in [2, 4, 6]:
                                        sentence = sentence.replace(" ' ", " '", 1)
                                        sentence = sentence.replace(" ' ", "' ", 1)

                                    else:
                                        sentence = sentence.replace(" ' "," '",1)

                                    sentence = sentence.replace(" '.","'.")
                            for top in alpino_ds:
                                for smain in top:
                                                                    ############
                                                                    # MAIN LEVEL#
                                                                    ############
                                    for child in smain:
                                        child_of_child = child.get("postag")
                                        if str(child_of_child) != "None":  # empty

                                            pos = findpos(child)
                                            if pos != "empty":
                                                # get word
                                                word = child.get("word")
                                                index = child.get("begin")
                                                # call output function
                                                writeoutput(pos, word, index, f, sentence)

                                                                            #########
                                                                            # LEVEL 2#
                                                                            #########

                                        for childx in child:
                                            child_of_child = childx.get("postag")
                                            if str(child_of_child) != "None":  # empty

                                                pos = findpos(childx)
                                                if pos != "empty":
                                                    # get word
                                                    word = childx.get("word")
                                                    index = childx.get("begin")
                                                    # call output function
                                                    writeoutput(pos, word, index, f, sentence)

                                                                                    #########
                                                                                    # LEVEL 3#
                                                                                    #########

                                            for childy in childx:
                                                child_of_child = childy.get("postag")
                                                if str(child_of_child) != "None":  # empty

                                                    pos = findpos(childy)
                                                    if pos != "empty":
                                                        # get word
                                                        word = childy.get("word")
                                                        index = childy.get("begin")
                                                        # call output function
                                                        writeoutput(pos, word, index, f, sentence)

                                                                                            #########
                                                                                            # LEVEL 4#
                                                                                            #########

                                                for childz in childy:
                                                    child_of_child = childz.get("postag")
                                                    if str(child_of_child) != "None":  # empty

                                                        pos = findpos(childz)
                                                        if pos != "empty":
                                                            # get word
                                                            word = childz.get("word")
                                                            index = childz.get("begin")
                                                            # call output function
                                                            writeoutput(pos, word, index, f, sentence)

                                                                                                    #########
                                                                                                    # LEVEL 5#
                                                                                                    #########

                                                    for childa in childz:
                                                        child_of_child = childa.get("postag")
                                                        if str(child_of_child) != "None":  # empty

                                                            pos = findpos(childa)
                                                            if pos != "empty":
                                                                # get word
                                                                word = childa.get("word")
                                                                index = childa.get("begin")
                                                                # call output function
                                                                writeoutput(pos, word, index, f, sentence)

                                                                                                            #########
                                                                                                            # LEVEL 6#
                                                                                                            #########

                                                        for childb in childa:
                                                            child_of_child = childb.get("postag")
                                                            if str(child_of_child) != "None":  # empty

                                                                pos = findpos(childb)
                                                                if pos != "empty":
                                                                    # get word
                                                                    word = childb.get("word")
                                                                    index = childb.get("begin")
                                                                    # call output function
                                                                    writeoutput(pos, word, index, f, sentence)

                                                                                                                    #########
                                                                                                                    # LEVEL 7#
                                                                                                                    #########

                                                            for childc in childb:
                                                                child_of_child = childc.get(
                                                                    "postag"
                                                                )
                                                                if str(child_of_child) != "None":  # empty

                                                                    pos = findpos(childc)
                                                                    if pos != "empty":
                                                                        # get word
                                                                        word = childc.get("word")
                                                                        index = childc.get("begin")
                                                                        # call output function
                                                                        writeoutput(pos, word, index, f, sentence)

                                                                                                                            ##########
                                                                                                                            # LEVEL 8#
                                                                                                                            ##########

                                                                for childd in childc:
                                                                    child_of_child = childd.get(
                                                                        "postag"
                                                                    )
                                                                    if str(child_of_child) != "None":  # empty

                                                                        pos = findpos(childd)
                                                                        if pos != "empty":
                                                                            # get word
                                                                            word = childd.get("word")
                                                                            index = childd.get("begin")
                                                                            # call output function
                                                                            writeoutput(pos, word, index, f, sentence)

                                                                                                                                    ###########
                                                                                                                                    # LEVEL 9 #
                                                                                                                                    ###########

                                                                    for childe in childd:
                                                                        child_of_child = childe.get(
                                                                            "postag"
                                                                        )
                                                                        if str(child_of_child) != "None":  # empty

                                                                            pos = findpos(childe)
                                                                            if pos != "empty":
                                                                                # get word
                                                                                word = childe.get("word")
                                                                                index = childe.get("begin")
                                                                                # call output function
                                                                                writeoutput(pos, word, index, f, sentence)

                                                                                                                                            ############
                                                                                                                                            # LEVEL 10 #
                                                                                                                                            ############
                                                                        for childf in childe:
                                                                            child_of_child = childf.get(
                                                                                "postag"
                                                                            )
                                                                            if str(child_of_child) != "None":  # empty

                                                                                pos = findpos(childf)
                                                                                if pos != "empty":
                                                                                    # get word
                                                                                    word = childf.get("word")
                                                                                    index = childf.get("begin")
                                                                                    # call output function
                                                                                    writeoutput(pos, word, index, f, sentence)

                                                                            for childg in childf:
                                                                                child_of_child = childg.get(
                                                                                    "postag"
                                                                                )
                                                                                if str(child_of_child) != "None":  # empty

                                                                                    pos = findpos(childg)
                                                                                    if pos != "empty":
                                                                                        # get word
                                                                                        word = childg.get("word")
                                                                                        index = childg.get("begin")
                                                                                        # call output function
                                                                                        writeoutput(pos, word, index, f, sentence)

