import feedparser
import io
import re


f = io.open('D:/data.txt','r+',encoding='utf-16')
g = io.open('D:/test.txt','r+',encoding='utf-16')
object = []
i = None
for i in g.readlines():
    try:
        object.append(str(i).replace("\n", ""))
    except:
        pass

#print object
source = 0
for newsSource in object:
    d = feedparser.parse(newsSource)
    source += 1
    print "News Source: " + source.__str__()
    #print d
    title = ""
    summary = ""
    link = ""
    date = ""

    for e in d['entries']:
        title = e['title']

        summary = e['summary']
        summary = re.sub('<.*?>', '', summary)

        link = e['links'][0]['href']

        date = e['published']

        f.write("\n\n" + "title: " + title + ";summary: " + summary + ";link: " + link + ";date: " + date + ";")

f.close()

