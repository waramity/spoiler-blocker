import nltk
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import numpy as np
import math
import pandas as pd

from cleanTextTechniques import *

def loadSampleData(filePath):
    """ Load data in file path argument """
    dataFile = open(filePath,'r')
    data = dataFile.read()
    dataFile.close()
    return data

def tokenize(text):
    """ Tokenize text """
    return nltk.word_tokenize(text)

""" Part-of-speech tagging for lemmatize """
def posTaggingForLem(text):
    POS_tag = nltk.pos_tag(text)
    return POS_tag

def convertVBtoJJ(POS_tag, vb_docs):
    """ Convert verb 2,3 to verb 1 """
    wanted_POS = ['VBN', 'VBD','VBG']
    for i, word in enumerate(POS_tag):
        if word[1] in wanted_POS:
            if vb_docs.loc[vb_docs[word[1]] == word[0], 'JJ'] is not None:
                sub_vb = vb_docs.loc[vb_docs[word[1]] == word[0], 'JJ']
                if len(sub_vb) > 0:
                    POS_tag[i] = (sub_vb.get_values()[0], 'JJ')
    return POS_tag

""" lemmatization """
def lemmatization(POS_tag):
    wordnet_lemmatizer = WordNetLemmatizer()
    adjective_tags = ['JJ','JJR','JJS']
    lemmatized_text = []
    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun
    return lemmatized_text

""" Part-of-speech tagging for filtering """
def posTaggingForFiltering(lemmatized_text):
    POS_tag = nltk.pos_tag(lemmatized_text)
    return POS_tag

""" Part-of-speech based for filtering to create stopword list และคัดเฉพาะ POS tagging จาก wanted_POS list """
def posBasedFiltering(POS_tag):
    stopwords = []
    wanted_POS = ['RB', 'VB','VBG', 'VBN', 'VBZ', 'PRP','NN','NNS','NNP','NNPS','JJ','JJR','JJS', 'VBD','VBG', 'VBP','FW']
    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])
    punctuations = list(str(string.punctuation))
    stopwords = stopwords + punctuations
    return stopwords

""" เอา list stopword จาก posBasedFiltering มารวมกับ list ของ long_stopwords.txt """
def completeStopwordGeneration(stopwords):
    stopword_file = open("./assets/long_stopwords.txt", "r")
    lots_of_stopwords = []
    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))
    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)
    return stopwords_plus
    #Stopwords_plus contain total set of all stopwords
""" remove all stopword """
def removingStopwords(lemmatized_text, stopwords_plus):
    processed_text = []
    for word in lemmatized_text:
        if word not in stopwords_plus:
            processed_text.append(word)
    return processed_text
