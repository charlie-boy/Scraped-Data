__author__ = 'bigDaDDy'

import requests
from bs4 import BeautifulSoup
import re
import io
import json

err = io.open('D:/errorList.txt','a',encoding='utf-16')

url = "https://www.zomato.com/"
headers = {'User-Agent' : 'Mozilla/5.0'}
try:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content)
except:
    print "Error 1"
    err.write(url+"\n".encode('ascii', 'ignore').decode('ascii'))

mainpagecountry = soup.findAll("span", {"class":"hp-country-item mt5"})

cities = {}

for country in mainpagecountry:
    tag = country.findAll("div", {"class" : "hp-country-name"})
    print tag[0].contents[0]," ..."
    cityList = country.findAll("a")
    dictionary = {}
    for link in cityList:
        url_rest = link["href"]+"restaurants"
        #print url_rest
        try:
            r_rest = requests.get(url_rest, headers=headers)
            soup_rest = BeautifulSoup(r_rest.content)
        except:
            print "error 2"
            err.write(url+"\n".encode('ascii', 'ignore').decode('ascii'))
        a = soup_rest.findAll("div", {"class": "col-l-3 mtop0 alpha tmargin pagination-number"})
        x = re.findall(r'\d+',str(a[0]))
        dictionary[url_rest] = x[3]

    cities[str(tag[0].contents[0])] = dictionary


###############################################################
# Edit path of file here #

with open('D:/zomatoCityPagestrial.txt', 'a') as outfile:
    json.dump(cities, outfile)

###############################################################