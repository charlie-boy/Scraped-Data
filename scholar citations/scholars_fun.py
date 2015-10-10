import sys
import urllib2
import re
import io
from bs4 import BeautifulSoup
import time

f = io.open('D:/citations2.txt','r+',encoding='utf-16')

def download(url):
    try:
        response = opener.open(url)
    except Exception:
        # tb = traceback.format_exc()
        print 'Error: Could not Retrieve Count, access error'
        return -1
    return response


# setup downdloader
proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8123"})
opener = urllib2.build_opener()  #i(proxy_support)
opener.addheaders = [('Cookie', "PREF=ID=1111111111111111:FF=0:LD=en:TM=1395775713:LM=1435150273:S=PC3tAF-5euX6St7V; NID=69=KSD0jp-OaiBX89tFDhB010j9_B9FTWIDJVKuV0Vw7akm1KOfDsZXREUjb2Vfih0JXLoME7yaLA-w1Tg3FK2nMFJJTpvspvINeF3FCtTfWWQGfcHLKOFciXxGziB_gbTepmNew8VWackoWNs7mxF-DaRwQnsN0ZfSBhk04fOuYxk961T_3qmODalS0uOd9OWZR4HkVELT1QHMSfCIvUbS_pTlNLHP1HmqSEC5STICiaQ4X4sBFbG_CAUspaW3wHxYQgkNnacuMFXXQZNEpvV9Bs0yTT9RuGxL3NOGHASuGGnn4ttkpeE; GSP=LM=1432800529:S=B_hX-jsaU0r0xik3; SID=DQAAALoBAAArwprUDPqc0tFbj5CH0TdvcDWiq4Ha7GzqKdz6CVQpfGJju12Q-qaQG1Jqp7CYrs0DSERgtXzpecbY5YYaatVObQ9COo1EbdzWqHAw2vGIQ8YSTXMy75-ZyFrPLAR23EY_BWvj2tGWuSy-lbBaRSuehYKSOkiJTMUbW77d14Lt3i6fqZ9vZ4rqXJIOrN_OBn6F2G-MDpjnJ0kzDjC1dt5z5SPHVI7zYiGmOMBfAZOkdRnc0awtyFwv49gfJCI1NbbbEPyQ9rbeHoxGFmqd_mHrCf2VQ9I8UqNaLy4A6fNvH_plcChP6W-9UQBCHg0js0_p-9QGmGGniRxNGMaxVJ6-WBu_2TBVT5HdZQXJfGDfkLcqIOvx3ouFnV1Qkhxt7Kl6WT_yqbOuDSVCVkSb66bfy2PYJNiKhyENj3WlDGNe7BXOhdmXaHmWp40zfNEoSTXcKAqIWLgdyga26d9M9SQ8Uow4n1TIWan7BCM3ZHPe36RiSLuxch20FK8qkYl2rV2agxm-zJsq6WLAxj7LP2axFtR0ZJXUE2GK92ulO1G54deBWqx8Y6FSMO8dysnVNUN-kO7BE1YUf6uPrru_v7Sk; HSID=A79SL1G1f2qDL89Pk; SSID=Auz-wMgvmvFnXaP8w; APISID=krLHtF2ytvVoBuMp/AKEiBKg9Bybj6LlSB; SAPISID=2xGBXrVP-ONJ4eyX/A7AISzEoxcTgAs_h5")]

#get author name. NO spaces, words separated by '+'
name = "eric%20topol"  #sys.argv[1]

url = 'https://scholar.google.co.in/citations?view_op=search_authors&mauthors=' + name  #'http://scholar.google.gr/citations?hl=en&view_op=search_authors&mauthors='+name
response = download(url)
html = response.read()
soup = BeautifulSoup(html)

researcher = soup.findAll("h3", {"class": "gsc_1usr_name"})
researchersLinks = []
for person in researcher:
    researchersLinks.append(person.next.get("href"))

#print researchersLinks
reseaL = []
reseaL.append(researchersLinks[0])
number = 0

for link in reseaL:
    cstart = 0
    pagesize = 100
    while(True):
        url_second = 'https://scholar.google.co.in' + link + '&cstart=' + cstart.__str__() + '&pagesize=' + pagesize.__str__() #'http://scholar.google.gr/citations?hl=en&view_op=search_authors&mauthors='+name
        response_second = download(url_second)
        html_second = response_second.read()
        soup_second = BeautifulSoup(html_second)

        number += 1
        print "Page: " + number.__str__() + "..."

        researcher_info = soup_second.find("div", {"id": "gsc_prf_in"})
        researcher_name = researcher_info.string
        researcher_background = researcher_info.nextSibling.string

        research_paper = soup_second.findAll("a", {"class": "gsc_a_at"})
        topics = []
        research_paper_link = []
        research_paper_co_authors = []
        for paper in research_paper:
            number += 1
            initialTime = time.time()
            topics.append(paper.find(text=True))

            link_third = paper['href']
            research_paper_link.append(paper['href'])

            url_third = 'https://scholar.google.co.in' + link_third
            response_third = download(url_third)
            html_third = response_third.read()
            soup_third = BeautifulSoup(html_third)

            co_authors = soup_third.find("div", {"class": "gsc_value"}).contents
            research_paper_co_authors.append(co_authors)
            #print research_paper_co_authors
            print "Page: " + number.__str__() + "..."
            finalTime = time.time()
            delay = finalTime - initialTime
            if delay > 1:
                pass
            else:
                time.sleep(1-delay)

        print research_paper_link

        citations = soup_second.findAll("a", {"class": "gsc_a_ac"})
        cites = []
        for c in citations:
            cites.append(c.find(text=True))

        for n in range(len(cites)):
            f.write("\n\nName: " + researcher_name + ";Background: " + researcher_background + ";Topic: " + topics[n] +
                    ";Cited by: " + cites[n] + ";GoogleLink:" + research_paper_link[n] + ";Co-Authors:" + research_paper_co_authors[n][0] + ";")


        try:
            cont = soup_second.find("button", {"id": "gsc_bpf_more"})['disabled']
            print "Done"
            break
        except:
            cstart += 100
            continue

f.close()
