import urllib.request
import requests
import gzip
from urllib.request import Request, urlopen
import csv
import re

from main import *

# CONST_NAME = "Name"
TITLE_PATTERN = r'\<title\>(.*)\<\/title\>' #Regular Expression Pattern to get movie title
ACTOR_PATTERN = r'\<a href\=\"\/name\/nm\d*\/\"\>\s*(\w+\.?\s?\w*\s?\w*\s?)' # RegExr Pattern to get actor list
CHARACTER_PATTERN = r'\<a href\=\"\/title\/tt\d*\/characters\/nm\d*\" \>(\w*\s*\w*)' # RegExr Pattern to get character list
# CHARACTER_PATTERN2 = r'\<td class\=\"character\"\>\s*(\w*\s?)+\s*' # RegExr Pattern to get character list
CHARACTER_PATTERN2 = r'\<td class\=\"character\"\>\s*(\w+\.?\s?\w*\s?\w*\s?)\s*' # RegExr Pattern to get character list
# \w+(\.\w+)+

PLOT_PATTERN = r'(\/title\/tt\d+\/plotsummary)'
SYNOPSIS_PATTERN = r'(\<ul class\=\"ipl-zebra-list\" id\=\"plot-synopsis-content\"\>(.|\n)*?<\/ul>)' # RegExr Pattern to get synopsis
SUMMARY_PATTERN = r'(\<ul class=\"ipl-zebra-list\"\s+id=\"plot-summaries-content\"\>(.|\n)*?<\/ul>)' # RegExr Pattern to get summary

def getHTMLpages(url):
    """ request url from homepage and return html tag as string """
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf-8")
    fp.close()
    return mystr

def removeDuplicateItem(data):
  return list(dict.fromkeys(data))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

summaryDatabase = [['title', 'spoilerText', 'synopsisText', 'actorList', 'characterList']] #declare database as array
movieHtmlPage = getHTMLpages("https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth") # return html tag from  https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth

urls = re.findall(r'(\/title\/tt\d+\/)',movieHtmlPage) # findall <a href='/title/tt84726782' # return ['/title/tt637834', '/title/tt64721465']

urls = removeDuplicateItem(urls) # delete duplicate item  #['/title/tt12', '/title/tt12', '/title/tt13'] => return ['/title/tt12', '/title/tt13']

# print(urls)
i=0

for url in urls:
    i += 1
    print("{} of {} in progress. Request {} content.".format(i, len(urls), url))
    moviePage = getHTMLpages("https://www.imdb.com" + str(url)) # return html tag from  https://www.imdb.com/movies-in-theaters/title/tt6806448/
    fullcastPage = moviePage.replace('\n', '').replace('\r', '') # HTML pages have new lines is \n and \r

    title = re.findall(TITLE_PATTERN, moviePage) #findall <title>Fast & Furious</title> # return Fast & Furious
    print("Get {} movie HTML page...".format(title))

    actor = re.findall(ACTOR_PATTERN, fullcastPage) # return ['Shaw', 'Hobbs', 'Paul Walker']
    character = re.findall(CHARACTER_PATTERN, fullcastPage) # return ['Shaw', 'Hobbs', 'Paul Walker']
    plotSummaryUrl = re.findall(PLOT_PATTERN, moviePage) # return ['/title/tt4379641/plotsummary']
    print("Find actor, character, plot summary, summary, synopsis...")
    print(actor)

    character = character + re.findall(CHARACTER_PATTERN2, fullcastPage)

    plotSummaryPage = getHTMLpages("https://www.imdb.com" + str(plotSummaryUrl[0]))  # get HTML pages from https://www.imdb.com/title/tt6806448/plotsummary
    summary = re.findall(SUMMARY_PATTERN, plotSummaryPage) # keep summary text as summary string
    synopsis = re.findall(SYNOPSIS_PATTERN, plotSummaryPage) # keep summary text as synopsis string

    summaryDatabase.append([str(title[0]), str(summary[0]), str(synopsis[0]), str(actor), str(character)])

""" Write file """
csv.register_dialect('myDialect',
quoting=csv.QUOTE_ALL,
skipinitialspace=True)
print("Writing file to csv...")

with open('crawler-data.csv', 'w') as f:
    writer = csv.writer(f, dialect='myDialect')
    for row in summaryDatabase:
        print("Write {}.".format(row[0]))
        writer.writerow(row)

f.close()
print('Done!')
