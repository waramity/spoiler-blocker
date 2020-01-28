from generateDictTechniques import *
from cleanTextTechniques import *

vb_docs = pd.read_csv('./assets/verbs-all.csv')

""" main function for text preprocessing """
""" Clean text """
def cleanText(data, split):
    sentences = []
    for line in data.split('\n'):
        """ ===== Noise removal ===== """
        # print("Noise removal process starting...")
        line = removeHtmlTag(line)
        # print("Remove HTML Tags: {}".format(line))
        line = convertHtmlUnescape(line)
        # print("Convert HTML Unescape: {}".format(line))
        line = removeUnicode(line)
        # print("Remove unicode: {}".format(line))
        line = removeTwitterUser(line)
        # print("Remove twitter user: {}".format(line))
        line = removeURL(line)
        # print("Remove URL: {}".format(line))
        line = removeHashtag(line)
        # print("Remove hashtag: {}".format(line))
        line = removeNewLine(line)
        # print("Remove new line: {}".format(line))

        """ ===== Remove main ===== """
        line = removeBracket(line)
        # print("Remove bracket: {}".format(line))
        line = removePunctation(line)
        # print("Remove punctation: {}".format(line))
        line = removeEmoticons(line) # removes emoticons from text
        # print("Remove emoticons: {}".format(line))
        line = convertLowercase(line)
        # print("Convert lower case: {}".format(line))
        line = removeNumbers(line)
        # print("Remove numbers: {}".format(line))
        line = removeWhiteSpace(line)
        # print("Remove white space: {}".format(line))

        if split:
            sentences += splitSentences(line)
        else:
            sentences += [line]
        # print(line)
    return sentences


""" Generate Dictionary """
def generateDictionary(sentences, isDict):
    tokenize_dict = []
    dict = []
    lemma_dict = []
    remove_stopword_dict = []
    replaced_pronoun_dict = []
    tokenize_dict = []
    stemmed_dict = []

    for sentence in sentences:
        tokenize_text = tokenize(sentence)
        tokenize_dict += tokenize_text
        POS_tag = posTaggingForLem(tokenize_text)
        # print("posTaggingForLem: " + str(POS_tag))
        POS_tag = convertVBtoJJ(POS_tag, vb_docs)
        # print("convertVBtoJJ: " + str(POS_tag))
        lemmatized_text = lemmatization(POS_tag)
        # print("lemmatization: " + str(lemmatized_text))
        lemma_dict += lemmatized_text
        POS_tag = posTaggingForFiltering(lemmatized_text)
        # print("posTaggingForFiltering: " + str(POS_tag))
        stopwords = posBasedFiltering(POS_tag)
        # print("posBasedFiltering: " + str(stopwords))
        stopwords_plus = completeStopwordGeneration(stopwords)
        removed_stopword = removingStopwords(lemmatized_text, stopwords_plus)

        if isDict:
            replaced_pronoun_dict.append(removed_stopword)
        else:
            replaced_pronoun_dict += removed_stopword

    return replaced_pronoun_dict
