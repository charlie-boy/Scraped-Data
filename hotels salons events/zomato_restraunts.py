import requests
from bs4 import BeautifulSoup
import itertools
import io
import re
import urllib3
from threading import Thread
import json
import urllib2
import time

#"Canada": {"https://www.zomato.com/toronto/restaurants": "276"}

#cities = ['Varanasi', 'Agra', 'Ahmedabad', 'Allahabad', 'Amritsar', 'Aurangabad', 'Bhopal', 'Bhubaneswar', 'Chandigarh',
#          'Chennai', 'Coimbatore', 'Dehradun', 'ncr', 'Guwahati', 'Hyderabad', 'Indore', 'Kanpur', 'Kochi', 'Kolkata',
#          'Lucknow', 'Ludhiana', 'Mangalore', 'Mysore', 'Nagpur', 'Nashik', 'Patna', 'Puducherry', 'Pune', 'Ranchi', 'Surat',
#          'Vadodara', 'Visakhapatnam']

#page_count = [4, 11, 62, 12, 11, 9, 9, 8, 37, 104, 7, 11, 305, 20, 109, 25, 16, 27, 82, 28, 19, 5, 6, 22, 4, 9, 4, 116,
#              6, 8, 9, 23]

headers = {'User-Agent' : 'Mozilla/5.0'}

cityData = open('D:/zomatoCityPages.txt')
citiesPages = json.load(cityData)


err = io.open('D:/errorList.txt','a',encoding='utf-16')
errorCountUrl = 0
count = 0
totalcount = 0


def internet_on():
    try:
        url = 'https://www.zomato.com/'
        http = urllib3.PoolManager()
        r1 = http.request('GET', url,headers=headers, timeout=5)
        print "CONNECTION MADE"
        return True
    except urllib2.URLError as err: pass
    return False


def th(i,j,k,cost):
    L = i.contents
    n = L[0]

    if cost is None or cost.parent is None:
        costfor2 = ""
    else:
        C = cost.parent.contents
        #print type(C[2])
        #Co = C[2].encode('utf-8').strip()
        costfor2 = C[2].strip()

    #add = str(j.get("title"))
    add = j.get("title").encode('ascii', 'ignore').decode('ascii')

    #cui = str(k.get("title"))
    try:
        cui = k.contents[1][3:]
    except:
        cui = k.contents[0]
        a = cui.index(":")
        cui = cui[a+1:]
        pass
    url_rest = i.get("href")
    #print ("This is URL_rest" + url_rest)

    try:
        r_rest = requests.get(url_rest, headers=headers, timeout=5)
        soup_rest = BeautifulSoup(r_rest.content)
    except:
        connection = False
        while connection == False:
            connection = internet_on()

        r_rest = requests.get(url_rest, headers=headers)
        soup_rest = BeautifulSoup(r_rest.content)

    RestPage_mapdata = soup_rest.findAll(text=re.compile('mapData'))
    print i.get("title")

    fblink = ""
    try:
        fb = soup_rest.findAll("div", {"class": "fb-likebox-wrapper"})

        fblink = re.findall(r'href=(.*?)&amp;',str(fb[0]))
        fblink = fblink[0].replace('%3A', ':')
        fblink = fblink.replace('%2F', '/')
    except:
        pass


    coordinate = ''
    try:
        for m in itertools.izip_longest(RestPage_mapdata):
            x = m[0].encode('ascii', 'ignore').decode('ascii')
            x = x.strip().split()
        lo = "lon:" + x[4]
        la = "la:" + x[6]
    except:
        lo = "lon:"
        la = "la:"
    coordinate =";" + lo.replace(",", "") + ";" + la.replace("};", "") + ";"

    RestPage_mapdata = soup_rest.findAll("span", {"class": "tel"})


   # for s in range(len(RestPage_mapdata[0].contents)):
    #    if str(RestPage_mapdata[0].contents[s]) not in ['\n',"<br/>", ' ']:
      #      z.append(str(RestPage_mapdata[0].contents[s].string))

    #z = re.findall(r'"tel">(.*?)</span',str(RestPage_mapdata[0]))
    #print (z)
    tel = ''
    try:
        for t in itertools.izip_longest(RestPage_mapdata):
            #tt = t[0].encode('ascii', 'ignore').decode('ascii')
            L_tel = t[0].contents;
            if 'Not' in str(L_tel[0]):
                break
            #print(str(L_tel[0]) + '\n')
            if '\n' == L_tel[0]:
                continue
            #yjprint L_tel[0]
            tel = tel + L_tel[0] + ','
    except:
        pass

    tel = tel.strip() + ';'

    #tel = tel.strip() + ';'

    pl = ''
    try:
        place = soup_rest.findAll("a", {"class": "nhu"})
        pl = place[0].contents[0].contents[0]
    except:
        pass

    Rest_known_for = soup_rest.findAll("div", {"class": "res-info-known-for-text mr5"})
    #print(Rest_known_for)
    known_for = ''
    for t in itertools.izip_longest(Rest_known_for):
        #tt = t[0].encode('ascii', 'ignore').decode('ascii')
        L_kf = t[0].contents;
        #if 'Not'in str(L_kf[0]):
        #    break
        #print('yahoo')
        #print(str(L_kf[0]) + '\n')
        known_for = known_for + L_kf[0].strip() + ','
    #print (known_for)

    Rest_wsuo = soup_rest.findAll("div", {"class": "res-info-dishes-text"})
    #print(Rest_wsuo)
    wsuo = ''
    for t in itertools.izip_longest(Rest_wsuo):
        #tt = t[0].encode('ascii', 'ignore').decode('ascii')
        L_wsuo = t[0].contents;
        #if 'Not'in str(L_kf[0]):
        #    break
        #print('yahoo')
        #print(str(L_wsuo[0]) + '\n')
        #print(wsuo)
        wsuo = wsuo + L_wsuo[0].strip() + ','
    #print (wsuo)

    Rest_infoftr = soup_rest.findAll("div", {"class": "res-info-feature-text"})
    #print(Rest_infoftr)
    infoftr = ''
    for t in itertools.izip_longest(Rest_infoftr):
        #tt = t[0].encode('ascii', 'ignore').decode('ascii')
        L_infoftr = t[0].contents;
        #if 'Not'in str(L_kf[0]):
        #    break
        #print('yahoo')
        #print(str(L_infoftr[0]) + '\n')

        try:
            infoftr = infoftr + L_infoftr[0].strip() + ','
        except:
            continue
    #print (infoftr)

    ##            Rest_costfor2 = soup_rest.findAll("span", {"class":"res-buffet-price rbp3"})
    ##            print(Rest_costfor2)
    ##            #print(Rest_infoftr)
    ##            costfor2 = 'null'
    ##            for t in itertools.izip_longest(Rest_costfor2):
    ##                #tt = t[0].encode('ascii', 'ignore').decode('ascii')
    ##                L_costfor2 = t.contents;
    ##
    ##                print(L_costfor2)
    ##                #if 'Not'in str(L_kf[0]):
    ##                #    break
    ##                #print('yahoo')
    ##                #print(str(L_infoftr[0]) + '\n')
    ##                costfor2 = costfor2 + L_costfor2[0] +  ','
    ##            costfor2 = costfor2.strip() + ';'

    Rest_day = soup_rest.findAll("div", {"style": "min-width:50px;float:left;"})
    Rest_time = soup_rest.findAll("span", {"style": "margin-right: 10px;"})
    #print(Rest_infoftr)
    timings = ''
    count_day = 0
    for d, t in itertools.izip_longest(Rest_day, Rest_time):
        if count_day == 0:
            count_day = count_day + 1
            continue

        #print(d)
        #tt = t[0].encode('ascii', 'ignore').decode('ascii')
        L_day = d.contents;
        L_time = t.contents;

        #if 'Not'in str(L_kf[0]):
        #    break
        #print('yahoo')
        #print(str(L_infoftr[0]) + '\n')
        try:
            timings = timings + L_day[0] + ',' + L_time[0] + ','
        except:
            pass
    timings = timings.strip() + ';'
    #f.write('Tel: '+ L_tel[0] +  ' \n')
    f.write(
        'Name:' + n + ';Place:'+ pl + ';Address:' + add + ';Zomato url:'+ url_rest + ';FB url:' + fblink + ';Cuisines:' + cui + coordinate + 'Tel:' + tel + 'Known For:' + known_for + ';Info Feature:' + infoftr + ';Cost:' + costfor2 + ';What should you order:' + wsuo + ';Timings:' + timings + '\n')

try:
    url = 'https://www.zomato.com/'
    http = urllib3.PoolManager()
    r1 = http.request('GET', url,headers=headers, timeout=5)
    print "CONNECTION MADE"
except:
    err.write('\n\nCONNECTION ABORTED\n\n'.encode('ascii', 'ignore').decode('ascii'))

for country in citiesPages:
    #country = "India"
    for urlKey in citiesPages[country]:
        for x in range(1, int(citiesPages[country][urlKey])+1):
            print str(x)
            url = urlKey+'/?page=' + str(x) #"https://www.zomato.com/hyderabad/restaurants?category=6"
            #url = "https://www.zomato.com/ncr/restaurants"
            print url
            if count == 0:
                pass
            else:
                err.write('\nHotel links that showed error: '+str(count).encode('ascii', 'ignore').decode('ascii'))
                totalcount = totalcount + count

            count = 0

            try:
                r = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(r.content)
            except:
                err.write('\n\n'+url.encode('ascii', 'ignore').decode('ascii'))
                errorCountUrl = errorCountUrl + 1
                continue

            MainPage_textdata = soup.findAll("a", {"class": "result-title"})
            MainPage_add = soup.findAll("span", {"class": "search-result-address"})
            MainPage_cuisine = soup.findAll("div", {"class": "res-snippet-small-cuisine"})
            MainPage_cost = soup.findAll("span", {"class": "upc grey-text sml"})

            Mainpage_morelocations = soup.findAll("a", {"class":"search-collapse"})

            MainPage_cuisine = [MainPage_cuisine[n] for n in range(len(MainPage_cuisine)) if n%2]

            for val in Mainpage_morelocations:
                url_loc = 'https://www.zomato.com' + val.get("href")
                print val
                try:
                    r_loc = requests.get(url_loc, headers=headers, timeout=5)
                    soup = BeautifulSoup(r_loc.content)
                except:
                    if count == 0:
                        err.write('\n\nIn url:'+url+' following links of hotels showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                    err.write('\t'+url_loc+'\n'.encode('ascii', 'ignore').decode('ascii'))
                    count = count + 1
                    continue

                for index in range(len(soup.findAll("a", {"class": "result-title"}))):

                    if soup.findAll("a", {"class": "result-title"})[index] not  in MainPage_textdata:
                        MainPage_textdata.append(soup.findAll("a", {"class": "result-title"})[index])
                        MainPage_add.append(soup.findAll("span", {"class": "search-result-address"})[index])
                        MainPage_cuisine.append(soup.findAll("div", {"class": "res-snippet-small-cuisine"})[2*index-1])
                        MainPage_cost.append(soup.findAll("span", {"class": "upc grey-text sml"})[index])

            #print len(MainPage_textdata), " ", len(MainPage_add), " ", len(MainPage_cuisine), " ", len(MainPage_cost)
            x = re.findall(r'com/(.*?)/res',str(urlKey))
            print x[0]
            f = io.open('D:/'+country+ x[0] + 'Zomato.txt', 'a', encoding='utf-16')
            start = time.clock()
            threadList = []

            print len(MainPage_cuisine), len(MainPage_textdata), len(MainPage_add), len(MainPage_cost)
            for i, j, k, cost in itertools.izip_longest(MainPage_textdata, MainPage_add, MainPage_cuisine, MainPage_cost):
                try:
                    i.get("title")
                except:
                    continue
                try:
                    thr = Thread(target=th, args=(i,j,k,cost,))
                    thr.start()
                    threadList.append(thr)
                except:
                    url_rest = i.get("href").encode('ascii', 'ignore').decode('ascii')
                    if count == 0:
                        err.write('\n\nIn url:'+url+' following links of hotels showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                    err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                    count = count + 1

            for b in threadList:
                b.join()

            f.close()
            print(time.clock() - start)
