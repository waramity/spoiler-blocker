#!/usr/bin/python3
from flask import (Flask, request, jsonify, json)
from flask_cors import CORS
from flask_cors import CORS, cross_origin

import numpy as np
import re
from nltk.translate.bleu_score import sentence_bleu
import pandas as pd

from main import *

from generateDictTechniques import *
from cleanTextTechniques import *
from ast import literal_eval
import ast
import json

app = Flask(__name__)

"""Cross-Origin Resource Sharing (CORS)"""

CORS(app, support_credentials=True)

""" ===== Initialize the data and Variable ===== """
""" Tokenizes a text to its words, removes and replaces some of them """
print("Text preprocessing demo starting...")

""" ===== Declare file path ===== """

csvFile = "./crawler-data.csv" # declare file path


""" ===== Load file ===== """

spoiler_data = loadCsv(csvFile) # loadCSV return as array

""" ========= declare loaded data ========= """
movie_names = []
plots = []
synopsis = []

character_list = []
j = 0

""" ======= loaded data and append to array =========== """
for line in spoiler_data:
    # removeIMDb('Fast & Furious IMDb') => return 'Fast & Furious'
    """ Text preprocessing """
    if j == 0:
        j = j + 1
        continue
    movie_names += (cleanText(removeIMDb(line[0]), 0)) # clean movie title text and keep in movie_names array
    plots.append(cleanText(line[2], 1))
    if line[2].strip('][').split(', ') != ['']:
        character_list.append(line[4].strip('][').split(', '))
        character_list.append('|')


# movie_names = ['Fast & Furious', 'John Wick']
# plots = ['Fast & Furious spoiler cotent', 'John Wick spoiler cotent ']
# character_list =[['Shaw', 'Hobbs'] , ['John', 'Wick'] ]
""" ================== """

"""======= Generate Dictionary ======= """
plots_dict = []
for plot in plots:
    plots_dict.append(generateDictionary(plot, True))
# plots_dict = [['Fast','Furious','spoiler', 'cotent'], ['John', 'Wick', 'spoiler', 'cotent ']]

""" ================== """

def getItemFromArray(arr, length):
    finishedArr = []
    j = 0
    for i in range(length):
        if j == 0:
            j = j + 1
            continue;
        finishedArr.append(arr[i])

    return finishedArr

plot = plots_dict[1]

""" URL for request """
""" Send the content from google news, twitter, facebook """
# GET http://localhost:5000/get-movie-names
# return string ['Fast & furious', 'John Wick']

THRESHOLD = 5

def compareThreshold(score):
    if score > THRESHOLD:
        return 'Not spoil'
    return 'Spoil'

""" POST method """
""" content.js send spoil_suspect & movie_id as POST request and return bleu score back to content.js to block feed """
# for i in range(len(plots_dict[19])):
#     print("{}: {}".format(i, plots_dict[19][i]))

hypothesis = ['This', 'is', 'cat']
reference = ['This', 'is', 'a', 'cat']
references = [reference] # list of references for 1 sentence.
list_of_references = [references] # list of references for all sentences in corpus.
list_of_hypotheses = [hypothesis] # list of hypotheses that corresponds to list of references.
# np.set_printoptions(suppress=True)
np.set_printoptions(suppress=True)  #float, 2 units
                                               #precision right, 0 on left

a = np.array([nltk.translate.bleu_score.corpus_bleu(list_of_references, list_of_hypotheses)])   #notice how index 2 is 30

# np.array([nltk.translate.bleu_score.corpus_bleu(list_of_references, list_of_hypotheses)])
print(a)
# print(np.array([nltk.translate.bleu_score.corpus_bleu(list_of_references, list_of_hypotheses)]))
# print(nltk.translate.bleu_score.sentence_bleu(references, hypothesis))

def compareSentence(plots_dict, spoil_dict):
    max_score = 0
    for i in range(len(plots_dict)):
        # print("{}: {}: {}".format(i, [plots_dict[i]], spoil_dict))
        plot = [plots_dict[i]]
        curr_score = sentence_bleu(plot, spoil_dict)
        if curr_score > max_score:
            max_score = curr_score
        # print()
        # print("Score: {}".format(sentence_bleu(plot, spoil_dict)))
    return max_score


@app.route('/get-spoil-and-send-score', methods = ['POST'])
@cross_origin(supports_credentials=True)
def response_score():
    if request.method == "POST":
        spoil_suspect = request.form.get('spoil_suspect', None)
        movie_id = request.form.get('movie_id', None)
        spoil_suspect = cleanText(spoil_suspect, 1)
        # print("Clean spoil suspect to plain text: {}".format(spoil_suspect))

        spoil_dict = generateDictionary(spoil_suspect, False)
        # print("Generate dictionary: {}".format(spoil_dict))
        # for i in range(len(plots_dict[int(movie_id) + 1])):
        #     print("{}: {}".format(i, plots_dict[int(movie_id) + 1][i]))

        # score = corpus_bleu(plots_dict[int(movie_id) + 1], spoil_dict)

        # score = sentence_bleu(plots_dict[int(movie_id) + 1], spoil_dict)
        score = compareSentence(plots_dict[int(movie_id) + 1], spoil_dict)
        spoil = compareThreshold(score)
        # print(s.replace('a', ''))
        spoil_text = str(score).replace('e-', '')
        print("BLEU score: {}".format(spoil_text))
        spoil_float = float(spoil_text)/10
        print("BLEU score: {}".format(spoil_float))
    return "{}".format(spoil_float)

     # parse integer to strings # 12 integer => "12" string

""" GET method """
""" Send movie list to popup.js """
@app.route('/get-movie-names', methods = ['GET'])
def response_movie_name():
    if request.method == "GET":
        # return str(getItemFromArray(movie_names, len(movie_names)))  # parse array to strings # [1, 2, 3] array  => "[1, 2, 3]" strin
        return str(getItemFromArray(movie_names, len(movie_names)))  # parse array to strings # [1, 2, 3] array  => "[1, 2, 3]" strin

    return 'ERROR MOVIE NAMES NOT FOUND!!!'


""" Send character-names to content.js """
@app.route('/get-character-names', methods = ['GET'])
def response_character_name():
    if request.method == "GET":
        # print(getItemFromArray(character_list, 10))
        return str(getItemFromArray(character_list, len(character_list)))
    return 'ERROR MOVIE NAMES NOT FOUND!!!'
