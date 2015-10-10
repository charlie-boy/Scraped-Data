import requests
from bs4 import BeautifulSoup
import itertools
import io
import re
import json

aDarray = {"Address": None, "Categories": None, "Cuisines": None, "What\'s Good": None, "Services": None,
           "Buffet": None, "Price Range": None, "Timings":None}

errors = []
errorCountUrl = 0
count = 0
totalcount = 0

###########################################################################
# Edit path of files here #

f = io.open('D:/Restaurant.txt', 'a', encoding='utf-16')
err = io.open('D:/errorListRestaurants.txt','a',encoding='utf-16')
cityData = open('D:/trimmedData.txt')

############################################################################

cities = json.load(cityData)

for city in cities:
    page = cities[city]["restaurant"]
    print "\nCity: "+city.upper()
    print "Total pages: ",page,"\n"

    for x in range(1, page+1):
        print('Processing ... ' + str(x))
        url = 'https://www.zootout.com/restaurant/searchlist/delhi/restaurants/' + str(x)
        # print(x)
        if count == 0:
            pass
        else:
            err.write('\nRestaurant links that showed error: '+str(count).encode('ascii', 'ignore').decode('ascii'))
            totalcount = totalcount + count

        count = 0

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.content)
        except Exception as e:
            errors.append(url)
            err.write('\n\n'+url.encode('ascii', 'ignore').decode('ascii'))
            errorCountUrl = errorCountUrl + 1
            #print('Error')
            continue

        MainPage_textdata = soup.findAll("div", {"class": "restaurant"})
        MainPage_add = soup.findAll("span", {"class": "address attr"})
        MainPage_area = soup.findAll("strong")
        MainPage_cuisine = soup.findAll("div", {"class": "res-snippet-small-cuisine"})
        MainPage_tel = soup.findAll("p", {"class": "ctv_phone attr"})
        MainPage_cost_cat = soup.findAll("span", {"class": "cost_value attr"})
        #print(MainPage_textdata)
        #MainPage_text = MainPage_textdata[0].text

        #MainPage_link = 'en.wikipedia.org' + MainPage_textdata[0].find_all("a")[-1].get("href")

        # if __name__ == "__main__":

        for i, j, k, m, n in itertools.izip_longest(MainPage_textdata, MainPage_add, MainPage_area, MainPage_tel,
                                                    MainPage_cost_cat):

            # Title
            title = i.find_all("a")
            title_str = title[0].contents
            print(title_str[0])
            f.write('\n\nRestraunt Name:' + title_str[0])

            #print(str(i) + '\n')

            # Link to Restraunt
            #print('https://www.zootout.com/' + title[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
            url_rest = 'https://www.zootout.com/' + title[0].get("href").encode('ascii', 'ignore').decode('ascii')
            f.write(';URL:' + url_rest)

            # Address
            add = j.contents
            #print(add[0] + '\n')
            #f.write(add[0]+ '\n')

            # Area
            area = k.contents
            #print(str(area[0]) + '\n')
            #f.write('Area: ' + area[0]+ '\n')

            # Telephone
            tel = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
            #print(str(tel))
            a = re.findall(r'\d+', str(tel))
            telNumbers = []
            f.write(';Tel:'.encode('ascii', 'ignore').decode('ascii'))
            for num in a:
                if len(num) == 10:
                    f.write(num + ','.encode('ascii', 'ignore').decode('ascii'))
                    telNumbers.append(num)
            #print telNumbers


            # Economic Category
            econ = n.contents
            #print(str(econ[0]) + '\n')
            f.write(';Econ Category:' + econ[0])

            try:
                r_rest = requests.get(url_rest, timeout=5)
                soup_rest = BeautifulSoup(r_rest.content)

            except:
                #errors.append(url_rest + '/overview')
                if count == 0:
                    err.write('\n\nIn url:'+url+' following links of restaurants showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1
                continue

            RestPage_maplat = soup_rest.findAll("meta", {"property": "zootoutcom:location:latitude"})
            RestPage_maplong = soup_rest.findAll("meta", {"property": "zootoutcom:location:longitude"})
            #lat = RestPage_maplat[0].encode('ascii', 'ignore').decode('ascii')
            #print(lat)
            #f.write('Lat:'+ str(lat.get("content")))
            #f.write('Long:'+ RestPage_maplong[0].get("content"))

            RestPage_aText = soup_rest.findAll("span", {"class": "aText"})
            RestPage_aData = soup_rest.findAll("div", {"class": "aData"})

            x = []
            try:
                division = soup_rest.find_all('iframe',src=True)
                #print division
                x = re.findall(r'href=(.*?)&amp;width',str(division))
            except:
                pass

            if len(x)== 0:
                fbdata = ';FB_URL:'
                f.write(fbdata.encode('ascii', 'ignore').decode('ascii'))
            else:
                fbdata = ';FB_URL:' + x[0]
                f.write(fbdata.encode('ascii', 'ignore').decode('ascii'))


            for lat, lon in itertools.izip_longest(RestPage_maplat, RestPage_maplong):
                la = lat.get("content")
                lo = lon.get("content")
                if la == '0' and lo == '0':
                    la = ""
                    lo = ""
                else:
                    pass
                f.write(';lat:' + la.encode('ascii', 'ignore').decode('ascii'))
                f.write(';lon:' + lo.encode('ascii', 'ignore').decode('ascii'))

            for aText, aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
                aT = aText.contents
                aD = aData.contents
                #f.write(";" + aT[0] + ": ")

                #print aT[0]

                if 'Address' in str(aT[0]):
                    add = aData.contents

                    ad1 = add[0].contents
                    ad2 = add[2].contents
                    ad3 = add[3]
                    address = str(ad1[0] + ad2[0] + ad3)
                    aDarray["Address"] = address
                    #f.write(address.encode('ascii', 'ignore').decode('ascii'))

                if 'Categories' in str(aT[0]):
                    #f.write(str(aT[0]))
                    cat = aData.findAll("a")
                    calist = []
                    for ca in cat:
                        cc = ca.contents
                        calist.append(str(cc[0]))
                        #print(str(cc[0]))
                        #f.write(cc[0] + ' ,')
                    aDarray["Categories"] = calist

                if 'Cuisines' in str(aT[0]):
                    cus = aData.findAll("span")
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)/2))
                    #cus = cus[1]
                    #print('yahoo1')
                    culist = []
                    for cu_itr in range(0, ((len(cus) / 2))):
                        cu = cus[2 * cu_itr].contents
                        culist.append(str(cu[1]))
                        #print(cu)
                        #print(str(cu[1]))
                        #f.write(cu[1] + ' ,')
                    aDarray["Cuisines"] = culist

                if 'What\'s Good' in str(aT[0]):
                    cus_gud = aData.findAll("div")
                    whlist = []
                    for cus in cus_gud:
                        c_gud = cus.contents
                        c = str(c_gud[0])
                        whlist.append(c.strip())

                    #print(str(c_gud[0]))
                        #f.write(c.strip().encode('ascii', 'ignore').decode('ascii') + ' ,')
                    aDarray["What\'s Good"] = whlist

                if 'Services' in str(aT[0]):
                    cus = aData.findAll("span")
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)/2))
                    #cus = cus[1]
                    #print('yahoo1')
                    selist = []
                    for cu_itr in range(0, ((len(cus) / 2))):
                        cu = cus[2 * cu_itr].contents
                        selist.append(str(cu[1]))
                        #print(cu)
                        #print(str(cu[1]))
                        #f.write(cu[1] + ' ,')
                    aDarray["Services"] = selist

                if 'Buffet' in str(aT[0]):
                    #cus_gud = aData.findAll("div")
                    #c_gud = cus_gud[0].contents
                    aTemp = aData
                    #print(aTemp)
                    #print(str(aTemp).replace('<br/>',' , '))
                    x_tp = str(aTemp).replace('<br/>', ' , ')
                    #f.write(x_tp.encode('ascii', 'ignore').decode('ascii') + ' ,')
                    aDarray["Buffet"] = x_tp

                if 'Price Range' in str(aT[0]):
                    #cus_gud = aData.findAll("div")
                    #c_gud = cus_gud[0].contents
                    aTemp = aData
                    #print(aTemp)
                    #print(str(aTemp))
                    x_tp = aTemp.contents
                    #f.write(str(x_tp[0]).encode('ascii', 'ignore').decode('ascii') + ' ,')
                    aDarray["Price Range"] = str(x_tp[0])


            #if 'Timings' in str(aT[0]):

            RestPage_dowt = soup_rest.findAll("span", {"class": "dow"})
            RestPage_time = soup_rest.findAll("span", {"class": "timing"})

            #f.write('\n Timing: \n' )
            timearray = {}
            for dow, time in itertools.izip_longest(RestPage_dowt, RestPage_time):
                d_c = dow.contents
                t_c = time.contents
                #print(d_c[0] + ' , ' + t_c[0])
                a = str(d_c[0]).strip()
                b = str(t_c[0]).strip()
                timearray[a] = b
                #f.write(d_c[0] + ' , ' + t_c[0])
            aDarray["Timings"] = timearray

            #print aDarray


            if aDarray["Address"] == None:
                f.write((';Address:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Address:'+(aDarray["Address"]).encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Categories"] == None:
                f.write((';Categories:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Categories:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Categories"])):
                    f.write((aDarray["Categories"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Cuisines"] == None:
                f.write((';Cuisines:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Cuisines:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Cuisines"])):
                    f.write((aDarray["Cuisines"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["What\'s Good"] == None:
                f.write((';What\'s Good:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';What\'s Good:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["What\'s Good"])):
                    f.write((aDarray["What\'s Good"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Buffet"] == None:
                f.write((';Buffet:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Buffet:'+(aDarray["Buffet"]).encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Services"] == None:
                f.write((';Services:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Services:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Services"])):
                    f.write((aDarray["Services"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Price Range"] == None:
                f.write((';Price Range:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Price Range:'+(aDarray["Price Range"]).encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Timings"] == None:
                f.write((';Timings:;').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Timings:').encode('ascii', 'ignore').decode('ascii'))
                for key in aDarray["Timings"]:
                    f.write(key+" : "+(aDarray["Timings"][key]+",").encode('ascii', 'ignore').decode('ascii'))
                f.write(';'.encode('ascii', 'ignore').decode('ascii'))




##        for m in itertools.izip_longest(RestPage_mapdata):
##            x = m[0].encode('ascii', 'ignore').decode('ascii')
##            x = x.strip().split()
##            lo = "lon:" + x[4]
##            la = "la:" + x[6]
##            coordinate = lo + la.replace("}","")       
##        
##        f.write(n +  '\n' + add + '\n'+ cui+ '\n' + coordinate)
##        RestPage_mapdata = soup_rest.findAll("span", {"class":"tel"})
##        for t in itertools.izip_longest(RestPage_mapdata):
##            #tt = t[0].encode('ascii', 'ignore').decode('ascii')
##            L_tel = t[0].contents;
##            if 'Not'in str(L_tel[0]):
##                break
##            print(str(L_tel[0]) + '\n')
##            f.write('Tel: '+ L_tel[0] +  ' \n')

err.write("\n\nTotal errors while retrieving main pages: "+str(len(errors))+'\n'.encode('ascii', 'ignore').decode('ascii'))
err.write('Total restaurant links that showed error: '+str(totalcount).encode('ascii', 'ignore').decode('ascii'))
            
