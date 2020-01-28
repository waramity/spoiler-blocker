import numpy as np
import string
import nltk
import html
import textwrap3
import string
import pandas as pd
import re

from time import time
from generateDictTechniques import *
from array import *
from functools import partial
from collections import Counter
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import csv

""" Technique """

def loadSampleData(filePath):
    """ Load data in file path argument """
    dataFile = open(filePath,'r')
    data = dataFile.read()
    dataFile.close()
    return data

def loadCsv(filePath):
    file=open(filePath, "r")
    reader = csv.reader(file)
    # for line in reader:
    #     t=line[1],line[2]
    #     print(t)
    return reader

def removeIMDb(text):
    # (\s*I+M+D+b+)
    text = re.sub('(\s+I+M+D+b+)', '', text)
    return text

def formattingParagraph(text):
    """ formatting paragraph - remove space front of sentence """
    return textwrap3.dedent(text).strip()

""" Creates a dictionary with slangs and their equivalents and replaces them """
with open('./assets/slang.txt') as file:
    slang_map = dict(map(str.strip, line.partition('\t')[::2])
    for line in file if line.strip())

def convertHtmlUnescape(text):
    """ convert html unescape to special characters"""
    text = html.unescape(text)
    return text

def convertLowercase(text):
    """ convert lowercase """
    text = text.lower()
    return text

def removeBracket(text):
    text = re.sub('\(', '', text)
    text = re.sub('\)', '', text)

    # text = re.sub('\(.*?\)', '', text)
    return text

def removeHtmlTag(text):
    """ remove html tag """
    text = re.sub('<[^>]*>', '', text)
    return text

def removeNewLine(text):
    """ remove \n """
    text = text.replace(r"\n", " ")
    return text

def removeUnicode(text):
    """ remove unicode """
    """ Removes unicode strings like "\u002c" and "x96" """
    text = re.sub(r'(\\x\d+)',r'',text)
    text = text.encode('ascii', 'ignore').decode('unicode_escape')
    return text

def removePunctation(text):
    """ remove all special characters """
    punctuations = '''!-[]{};:'",<>/?@#$%^&*_~'''
    no_punct = ""
    for char in text:
       if char not in punctuations:
           no_punct = no_punct + char
    return no_punct

def removeEmoticons(text):
    """ Removes emoticons from text """
    text = re.sub(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', '', text)
    return text

def removeTwitterUser(text):
    """ remove url """
    text = re.sub('@[^\s]+', 'atUser', text)
    return text

def removeURL(text):
    """ remove url """
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'url', text)
    return text

def removeHashtag(text):
    """ remove hashtag """
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text

def removeNumbers(text):
    """ Removes integers """
    text = ''.join([i for i in text if not i.isdigit()])
    return text

def replaceMultipleSpace(text):
    """ Replace multiple space with one space """
    text = re.sub(r'(\s+){2,}', r' ', text)
    return text

def replaceElongated(word):
    """ Replaces an elongated word with its basic form, unless the word exists in the lexicon """
    repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    repl = r'\1\2\3'
    if wordnet.synsets(word):
        return word
    repl_word = repeat_regexp.sub(repl, word)
    if repl_word != word:
        return replaceElongated(repl_word)
    else:
        return repl_word

def replaceContraction(text):
    """ Replaces contractions from a string to their equivalents """
    contraction_patterns = [ (r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                             (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]
    patterns = [(re.compile(regex), repl) for (regex, repl) in contraction_patterns]
    for (pattern, repl) in patterns:
        (text, count) = re.subn(pattern, repl, text)
    return text

def replaceNegations(text):
    """ Finds "not" and antonym for the next word and if found, replaces not and the next word with the antonym """
    i, l = 0, len(text)
    words = []
    while i < l:
      word = text[i]
      if word == 'not' and i+1 < l:
        ant = replace(text[i+1])
        if ant:
          words.append(ant)
          i += 2
          continue
      words.append(word)
      i += 1
    return words

def removeWhiteSpace(text):
    """ remove white space """
    text = re.sub(r'(\t)', r'', text)
    # text = re.sub(r'(\s+)', r'', text)
    return text

def splitSentences(text):
    """ split sentences """
    text = text.split('.')
    text = [s for s in text if s != '']
    text = [s for s in text if s != ' ']
    return text

def getCharacterList(text):
    characterList = []
    return characterList
