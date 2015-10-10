import re

__author__ = 'bigDaDDy'

import json
import urllib2
import io

err = io.open('D:/errorFile.txt','a',encoding='utf-16')
alreadySaved = io.open('D:/alreadySaved.txt','r+',encoding='utf-16')
f = io.open('D:/data.txt','r+',encoding='utf-16')


url = "http://in.bookmyshow.com/getJSData/?cmd=GETEVENTLIST&f=json&et=CT&rc=NCR"
try:
    req = urllib2.Request(url)
    html = urllib2.urlopen(req).read()
    startup = json.loads(html)
    #with open('D:/dumpData.txt', 'w') as outfile:
    #    json.dump(startup, outfile)

    data = startup

    saved = []
    for i in alreadySaved.read().split('\n'):
        if(i != "\n"):
            saved.append(i[:len(i)])

    print saved

    for val in data["BookMyShow"]["arrEvent"]:
        url = "URL:"+val["FShareURL"]
        if url not in saved:
            print val

            event = "Event:"+val["EventTitle"]

            gen = "Genre:"+val["Genre"]

            showDates = "Dates:"
            for date in val["arrDates"]:
                showDates = showDates+date["ShowDateDisplay"]+","

            region  = ""
            for place in val["arrVenues"]:
                region  = region+"Region:"+place["Region_strName"]+";Venue:"+place["VenueName"]+";Longitude:"+place["VenueLongitude"]+";Latitude:"+place["VenueLatitude"]+","

            image = "Image url:"+val["BannerURL"]

            synopsis = "Event synopsis:"+val["EventSynopsis"].replace("<br/>", "").replace("<strong>", "").replace("</strong>", "")

            f.write("\n\n"+event+";"+gen+";"+url+";"+showDates+";"+region+";"+image+";"+synopsis+";")
            alreadySaved.write("\n\n"+url)
except:
    err.write(url+'\n'.encode('ascii', 'ignore').decode('ascii'))

###############################################################


