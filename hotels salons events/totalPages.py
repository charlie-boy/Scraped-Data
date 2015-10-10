__author__ = 'bigDaDDy'

import requests
from bs4 import BeautifulSoup
import re
import json
import itertools

url_zoot = 'http://www.zootout.com'
try:
    r = requests.get(url_zoot, timeout=5)
    soup = BeautifulSoup(r.content)
except:
    pass
mainPageObjects = soup.findAll("div", {"class": "citybox india"})
for a in itertools.izip_longest(mainPageObjects):
    b = a[0].contents

cities = {}
for value in b:
    if value != '\n':
        cities[(value.string).encode('ascii','ignore').lower().split()[0]] = None

print cities

#############################################################
#  Cities can be hardcoded here into the dictionary cities  #
#############################################################

for city in cities:
    print city
    url = 'http://www.zootout.com/'+city.lower()
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.content)

    except Exception as e:
        print(e)
        continue

    mainPageObjects = soup.findAll("a", {"class":"sigma-link"})
    #print mainPageObjects
    objects = {}
    for val in mainPageObjects:
        if str(val).find("restaurant")>0:
            objects["restaurant"]= None
            continue
        if str(val).find("hotels")>0:
            objects["hotels"]= None
            continue
        if str(val).find("salons")>0:
            objects["salons"] = None
            continue
        if str(val).find("events")>0:
            objects["events"] = None
            continue
        if str(val).find("attractions")>0:
            objects["attractions"] = None
            continue
    print objects
    for obj in objects:
        if obj == "restaurant":
            url_rest = 'http://www.zootout.com/'+city+'/'+obj+'/'+obj+'s'
        else:
            url_rest = 'http://www.zootout.com/'+city+'/'+obj+'/'+obj

        try:
            r_rest = requests.get(url_rest, timeout=5)
            soup_rest = BeautifulSoup(r_rest.content)

        except Exception as e:
            print(e)
            continue

        m = (soup_rest.findAll("span", {"class":"asset_icon pagecon pageconRR"}))
        pages = re.findall(r'\d+',str(m))
        if pages == []:
            actualPages = 1
        else:
            actualPages = int(pages[0])

        print obj," : ",actualPages
        objects[obj] = actualPages

    cities[city] = objects

###############################################################
# Edit path of file here #

with open('D:/data.txt', 'a') as outfile:
    json.dump(cities, outfile)

###############################################################