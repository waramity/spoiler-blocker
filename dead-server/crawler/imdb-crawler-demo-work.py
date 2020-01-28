import urllib.request
import requests
import gzip
from urllib.request import Request, urlopen
import csv

def getHTMLpages(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf-8")
    fp.close()
    return mystr;
person = [['title', 'mainUrl', 'spoilerUrl', 'spoilerText', 'synopsisText']]
mystr = getHTMLpages("https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth")
import re
urls = re.findall(r'(\/title\/tt\d+\/)',mystr)

print('List of movies in theter for now')
print('======================================')
i = 0
for url in urls:
    i += 1
    print("[" + str(i) + "]: " + ''.join(url[1]))

print('======================================')
movies = input('Choose spoilers what you want: ')

moviePage= getHTMLpages("https://www.imdb.com/"+str(urls[int(movies) - 1][0]))

plotSummary = re.findall(r'(\/title\/tt\d+\/plotsummary\?ref_=tt_stry_pl)', moviePage)

plotSummaryPage = getHTMLpages("https://www.imdb.com/"+str(plotSummary[0]))

start = '<ul class="ipl-zebra-list" id="plot-summaries-content">'
end = '</ul>'

synopsisPattern = r'(\<ul class\=\"ipl-zebra-list\" id\=\"plot-synopsis-content\"\>(.|\n)*?<\/ul>)'

summaryPattern = r'(\<ul class=\"ipl-zebra-list\"\s+id=\"plot-summaries-content\"\>(.|\n)*?<\/ul>)'

pattern = input("synopsis or summary (input 0 or 1): ")

if int(pattern):
    pattern = synopsisPattern
else:
    pattern = summaryPattern

result = re.findall(pattern, plotSummaryPage)

print("Your spoiler:" + ''.join(result[0]))
