__author__ = 'bigDaDDy'

import io
import urllib2
from bs4 import BeautifulSoup
import re
import string
import time

f = io.open('D:/publTest.txt','r+',encoding='utf-16')
g = io.open('D:/errors.txt','r+',encoding='utf-16')
h = io.open('D:/citations.txt','r+',encoding='utf-16')
i = io.open('D:/books.txt','r+',encoding='utf-16')

alphabets = list(map(chr, range(97, 123)))+list(map(chr, range(65, 91)))
otherChar = [':', ' ']
check = otherChar
uncheck = alphabets+[" "]

def getGoogleAuthors(getAuthors):
    authors = getAuthors.split(",")
    finalAuthors = []
    for auth in authors:
        names = auth.split()
        for i in range(len(names)):
            if len(names[i])<=1:
                names.remove(names[i])

            finalAuthors.append(names[i])
    return finalAuthors

def isAuthorPresent(authors, text):
    for a in authors:
        if(a in text):
            return True
    return False

def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]


def getReadableData(data):
    val = ''.join(data.findAll(text=True))
    for d in data.findAll('span'):
        s = d.find(text=True)
        val = val.strip(s)

    val = unicode.join(u'',map(unicode, val))
    value = re.sub('<.*?>', '', val)
    if(value[0] == " "):
        value = value[1:]
    return value

def getReadableAuthor(author):
    auth = ''.join(author.findAll(text=True))
    auth = re.sub('<.*?>', '', auth)
    return auth


def splittingValues(values):
    t = []
    for val in values:
        for i in val:
            t.append(i)
    return t

def clearString(str):
    finalString = ""
    for i in str:
        if i in check:
            finalString += "+"
        else:
            finalString += i
    return finalString

def deleteForeignLetters(str):
    finalString = ""
    for i in str:
        if i in uncheck:
            finalString += i
        else:
            finalString += ""
    return finalString

def getSpecificCitation(data):
    try:
        book = data.find("span", {"class": "gs_ctc"})
        print book
    except:
        pass
    result = data.nextSibling.nextSibling
    result = unicode.join(u'',map(unicode,result))
    citations = re.findall(r'Cited by (.*?)<', result)
    if len(citations) == 0:
        try:
            result = data.nextSibling.nextSibling.nextSibling
            result = unicode.join(u'\n',map(unicode,result))
            citations = re.findall(r'Cited by (.*?)<', result)
        except:
            pass
    if len(citations) == 0:
        citations = ["0"]
    return citations[0]

def download(url):
    try:
        response = opener.open(url)
    except Exception:
        # tb = traceback.format_exc()
        print 'Error: Could not Retrieve Count, access error'
        return -1
    return response


def result(title, authors, authorName):
    try:
        topic = clearString(title)
        url = 'https://scholar.google.co.in/scholar?q='+topic+authorName
        response = download(url)
        html = response.read()
        soup = BeautifulSoup(html)
    except:

        topic = deleteForeignLetters(title)
        topic = clearString(topic)
        url = 'https://scholar.google.co.in/scholar?q='+topic+authorName
        response = download(url)
        html = response.read()
        soup = BeautifulSoup(html)

        try:
            rightLink = soup.find("a", {"class": "gs_pda"})
            #print rightLink["href"]
            url = 'https://scholar.google.co.in' + rightLink["href"]
            response = download(url)
            html = response.read()
            soup = BeautifulSoup(html)
        except:
            pass


    data = soup.findAll("h3", {"class": "gs_rt"})
    auth = soup.findAll("div", {"class": "gs_a"})
    citations = re.findall(r'Cited by (.*?)<', html)

    finalCitation = -1
    errorType = -1

    if len(data) == 0:
        errorType = 2
        #continue
        pass

    elif (len(data) == 1):
        if(isAuthorPresent(authors, getReadableAuthor(auth[0]))):
            finalCitation = getSpecificCitation(data[0])
        else:
            errorType = 1

    else:
        for i in range(len(data)):
            value = getReadableData(data[i])
            distance = levenshteinDistance(value.lower(), title.lower())
            #print value.lower()
            #print title.lower()
            #print "distance: "+distance.__str__()
            if(distance <= 3):
                if(isAuthorPresent(authors, getReadableAuthor(auth[i]))):
                    finalCitation = getSpecificCitation(data[i])
                    errorType = -1
                    break
                else:
                    errorType = 1
            else:
                errorType = 2

    return finalCitation, errorType



# setup downdloader
proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8123"})
opener = urllib2.build_opener()  #i(proxy_support)
opener.addheaders = [('Cookie', "PREF=ID=1111111111111111:FF=0:LD=en:TM=2395775713:LM=1435150273:S=PC3tAF-5euX6St7V; NID=69=KSD0jp-OaiBX89tFDhB010j9_B9FTWIDJVKuV0Vw7akm1KOfDsZXREUjb2Vfih0JXLoME7yaLA-w1Tg3FK2nMFJJTpvspvINeF3FCtTfWWQGfcHLKOFciXxGziB_gbTepmNew8VWackoWNs7mxF-DaRwQnsN0ZfSBhk04fOuYxk961T_3qmODalS0uOd9OWZR4HkVELT1QHMSfCIvUbS_pTlNLHP1HmqSEC5STICiaQ4X4sBFbG_CAUspaW3wHxYQgkNnacuMFXXQZNEpvV9Bs0yTT9RuGxL3NOGHASuGGnn4ttkpeE; GSP=LM=1432800529:S=B_hX-jsaU0r0xik3; SID=DQAAALoBAAArwprUDPqc0tFbj5CH0TdvcDWiq4Ha7GzqKdz6CVQpfGJju12Q-qaQG1Jqp7CYrs0DSERgtXzpecbY5YYaatVObQ9COo1EbdzWqHAw2vGIQ8YSTXMy75-ZyFrPLAR23EY_BWvj2tGWuSy-lbBaRSuehYKSOkiJTMUbW77d14Lt3i6fqZ9vZ4rqXJIOrN_OBn6F2G-MDpjnJ0kzDjC1dt5z5SPHVI7zYiGmOMBfAZOkdRnc0awtyFwv49gfJCI1NbbbEPyQ9rbeHoxGFmqd_mHrCf2VQ9I8UqNaLy4A6fNvH_plcChP6W-9UQBCHg0js0_p-9QGmGGniRxNGMaxVJ6-WBu_2TBVT5HdZQXJfGDfkLcqIOvx3ouFnV1Qkhxt7Kl6WT_yqbOuDSVCVkSb66bfy2PYJNiKhyENj3WlDGNe7BXOhdmXaHmWp40zfNEoSTXcKAqIWLgdyga26d9M9SQ8Uow4n1TIWan7BCM3ZHPe36RiSLuxch20FK8qkYl2rV2agxm-zJsq6WLAxj7LP2axFtR0ZJXUE2GK92ulO1G54deBWqx8Y6FSMO8dysnVNUN-kO7BE1YUf6uPrru_v7Sk; HSID=A79SL1G1f2qDL89Pk; SSID=Auz-wMgvmvFnXaP8w; APISID=krLHtF2ytvVoBuMp/AKEiBKg9Bybj6LlSB; SAPISID=2xGBXrVP-ONJ4eyX/A7AISzEoxcTgAs_h5")]

lines = f.readlines()

for l in range(len(lines)):
    if l%4 == 0:
        initialTime = time.time()

        title = lines[l]
        getAuthors = lines[l+1]
        title = title.replace("\n", "")
        if(title[len(title)-1] == "."):
            title = title[0:len(title)-1]
        print "Title : " + title

        authors = getGoogleAuthors(getAuthors)
        auth = getAuthors.split(",")
        authorName = ""

        print getAuthors

        try:
            finalCitation, errorType = result(title, authors, authorName)
        except:
            time.sleep(600)

        if(finalCitation == -1):
            auth[0] = deleteForeignLetters(auth[0])
            auth[0] = clearString(auth[0])
            authorName = "+"+auth[0]
            try:
                finalCitation, errorType = result(title, authors, authorName)
            except:
                time.sleep(600)

        if(finalCitation == -1 and len(auth) > 1):
            getAuthors.replace(",", " ")
            getAuthors = deleteForeignLetters(getAuthors)
            getAuthors = clearString(getAuthors)
            authorName = "+"+getAuthors
            try:
                finalCitation, errorType = result(title, authors, authorName)
            except:
                time.sleep(600)

        if errorType == 1:
            g.write("Title:"+title+";Problem:Author didn't match"+"\n\n".encode('ascii', 'ignore').decode('ascii'))
        elif errorType == 2:
            g.write("Title:"+title+";Problem:Title didn't match"+"\n\n".encode('ascii', 'ignore').decode('ascii'))
        print "Citation : " + finalCitation.__str__() + "\n"
        if finalCitation >= 0:
            h.write("Title:" + title + ";Citation:" + finalCitation.__str__()+"\n\n".encode('ascii', 'ignore').decode('ascii'))

        finalTime = time.time()
        delay = finalTime - initialTime
        if delay > 1:
            pass
        else:
            time.sleep(1-delay)