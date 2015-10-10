import requests
from bs4 import BeautifulSoup
import itertools
import io
import re
import time
import urllib2
import json

f = io.open('D:/permalinks.txt','r',encoding='utf-16')
a = f.read()
b = a.split(",")
b.pop()
print b

for idx in range(1,11):
    url = "https://letsventure.com/startups?page="+str(idx)
    print "Page",idx," ..."

    headers = {'Cookie': '__utma=160773664.2107002064.1418549956.1419843440.1419855459.7; __utmz=160773664.1419597050.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); auth_token=wLVYRYHsh0Q4PpBrfrxM-g; _letsventure_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTY2ODQ2ZGJhODk0ZDc5MDI4NzhkZTdhMWRmNWY1NTllBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTJQcVV0MzNZOTBKaTBSeUNZeDllV1IrOExpTUJyMmJYdEJpMXBLNVJ5YTA9BjsARg%3D%3D--05a961e6850c7d04e8196ec263c00c96d7e6ebf7; __utmc=160773664'}
    try:
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()
    except:
        pass
    soup = BeautifulSoup(html)

    MainPage_textdata = soup.findAll("section", {"class":"row one-column-layout search-page"})

    for i in MainPage_textdata:
        z = re.findall(r'"permalink":"(.*?)",',str(i["ng-init"].encode('ascii', 'ignore').decode('ascii')))

    for i in z:
        f.write(i+",".encode('ascii', 'ignore').decode('ascii'))


"""
url = "https://letsventure.com/"+b[0]
print url
headers = {'Cookie': '__utma=160773664.2107002064.1418549956.1419843440.1419855459.7; __utmz=160773664.1419597050.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); auth_token=wLVYRYHsh0Q4PpBrfrxM-g; _letsventure_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTY2ODQ2ZGJhODk0ZDc5MDI4NzhkZTdhMWRmNWY1NTllBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTJQcVV0MzNZOTBKaTBSeUNZeDllV1IrOExpTUJyMmJYdEJpMXBLNVJ5YTA9BjsARg%3D%3D--05a961e6850c7d04e8196ec263c00c96d7e6ebf7; __utmc=160773664'}
try:
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
except:
    #err.write(url+'\n'.encode('ascii', 'ignore').decode('ascii'))
    #continue
    pass
soup = BeautifulSoup(html)
print soup


url = "https://letsventure.com/"+startup["permalink"]
try:
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
except:
    pass
soup = BeautifulSoup(html)

#MainPage_textdata = soup.findAll("section", {"class":"row one-column-layout search-page"})

"""
