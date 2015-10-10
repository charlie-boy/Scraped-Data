import requests
from bs4 import BeautifulSoup
import itertools
import io
import os
import re
import json
#import urllib.request, urllib2
import traceback

#url = 'http://www.zootout.com/delhi/attractions'

#amenities = ["Air Conditioned", "Boutiques", "Business Centre", "Coffee Shop", "Currency Exchange", "Dry Cleaning", "Executive Floor",
#             "Fitness Centre", "Parking", "Health Club", "Laundry Service", "Meeting Rooms", "Smoking Area", "Restaurant",
#             "Safe Deposit Box", "Swimming Pool", "Credit Cards Accepted", "Free Wifi"]

fileNum = 1
amenities = []
features = []
errorCountUrl = 0
count = 0
totalcount = 0


aTarrayCorrect = ['Address', 'Categories', 'Amenities', 'Features', 'Timings', 'Price Range', 'Photos']

errors = []

################################################################
# Edit path of files here #

f = io.open('D:/hotelDetails.txt','a',encoding='utf-16')
err = io.open('D:/errorList.txt','a',encoding='utf-16')
cityData = open('D:/data.txt')

################################################################

cities = json.load(cityData)

for city in cities:
    page = cities[city]["hotels"]
    print "\nCity: "+city.upper()
    print "Total pages: ",page,"\n"
    for idx in range(1, page+1):
        print('Processing ... ' + str(idx))
        url = 'http://www.zootout.com/hotel/searchlist/'+city+'/hotels/' + str(idx)

        if count == 0:
            pass
        else:
            err.write('\nHotel links that showed error: '+str(count).encode('ascii', 'ignore').decode('ascii'))
            totalcount = totalcount + count

        count = 0

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.content)

        except Exception as e:
            errors.append(url)
            err.write('\n\n'+url.encode('ascii', 'ignore').decode('ascii'))
            errorCountUrl = errorCountUrl + 1
            print('Error')
            continue


        MainPage_results = soup.findAll("div", {"class":"resultset"})
        #MainPage_phone = MainPage_results[0].findAll("div", {"class":"phone attr"})
        #MainPage_area = MainPage_results[0].findAll("span", {"class":"asset_icon tiny_address"})
        #MainPage_attr = MainPage_results[0].findAll("span", {"class":"attraction_icons tiny_good"})

        #print('yahpp')
        MainPage_phone = soup.findAll("p", {"class":"ctv_phone attr"})
        #MainPage_area = soup.findAll("span", {"class":"asset_icon tiny_address"})
        MainPage_area = soup.findAll("strong")
        MainPage_attr = soup.findAll("span", {"class":"attraction_icons tiny_good"})
        MainPage_cost = soup.findAll("span", {"class":"cost_value attr"})

        for h3, m, ar, gf, cost in itertools.izip_longest(soup.findAll("h3"), MainPage_phone, soup.findAll("strong"), MainPage_attr, MainPage_cost):

            #print('yahoo22')

            # Title
            name_attr = h3.findAll("a")
            name_at = 'null'
            try:
                name_at = name_attr[0].contents
                print(str(name_at[0]))
                f.write('\n\nhotel name:' + name_at[0])
            except:
                f.write('\n\nhotel name:PLEASE MANUALLY ADD HOTEL NAME'.encode('ascii', 'ignore').decode('ascii'))
                url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')
                if count == 0:
                    err.write('\n\nIn url:'+url+' following links of salons showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\t\t\'ascii\' codec can\'t encode characters'+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1


            # Link to Restraunt
            #print('https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
            url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')
            #print name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')
            f.write(';URL:' + url_rest)

            # Telephone
            tel_onclick = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
            tel_split = 'null'
            tel_split = tel_onclick.split("'")
            #print(str(tel_split[1]) + '\n')
            if len(tel_split)==0:
                f.write((";Tel:").encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Tel:' + tel_split[1])

            # Area
            #print(h3.parent)
            name_at = 'null'
            name_at = ar.contents
            #print(str(name_at))
            if len(name_at)==0:
                f.write((";Area:").encode('ascii', 'ignore').decode('ascii'))
                #f.write('Area: ' + name_at[0] + ';')
            else:
                f.write(';Area:' + name_at[0])

            # Cost
            #print(h3.parent)
            cost_at = 'null'
            cost_at = cost.contents
            #print(str(cost_at))
            if len(cost_at)==0:
                f.write((";Cost:").encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Cost:' + cost_at[0])



            url_rest = 'https://www.zootout.com/' + name_attr[0].get("href")

            try:
                r_rest_loc = requests.get(url_rest + '/overview', timeout=5)
                soup_rest_loc = BeautifulSoup(r_rest_loc.content)
            except:
                #errors.append(url_rest + '/overview')
                if count == 0:
                    err.write('\n\nIn url:'+url+' following links of hotels showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1
                continue



            #RestPage_maplat = soup_rest_loc.findAll("div", {"class":"info_section section_nearby"}).findAll("script",{"type":"text/javascript"})
            #RestPage_maplong = soup_rest_loc.findAll("div", {"class":"info_section section_nearby"}).findAll("script",{"type":"text/javascript"})
            #lat = RestPage_maplat[0].encode('ascii', 'ignore').decode('ascii')
            #print(lat)
            #f.write('Lat:'+ str(lat.get("content")))
            #f.write('Long:'+ RestPage_maplong[0].get("content"))

            RestPage_mapdata = soup_rest_loc.findAll("div", {"class":"info_section section_nearby"})

            #print(RestPage_mapdata)
            coordinate = 'null'
            for m in itertools.izip_longest(RestPage_mapdata):
                #print('yahoo')
                x = RestPage_mapdata[0].contents
                #print(x[1])
                x_sp = x[1].contents
                x_loc = x_sp[0].split("/")
                lo = "lon:" + x_loc[4]
                la = "lat:" + x_loc[5]
                coordinate =";" + lo + ";" + la
                #print(coordinate)
                f.write(coordinate.encode('ascii', 'ignore').decode('ascii') )

            try:
                r_rest = requests.get(url_rest, timeout=5)
                soup_rest = BeautifulSoup(r_rest.content)
            except:
                #errors.append(url_rest)
                if count == 0:
                    err.write('\n\nIn url: '+url+' following links of hotels showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1
                #print('Error')
                continue

    #        try:
    #            file_url = url_rest
    #            print(file_url)

    #            file = str(fileNum)
    #            os.makedirs(file)
    #            filename = str(file) + '/'+ str(file_url) + '.html'
    #            #urllib.request.urlretrieve(file_url, file)

    #            fileNum = fileNum+1
    #        except Exception as e:
    #            traceback.format_exc()
    #            print (e)

            RestPage_aText = soup_rest.findAll("span", {"class":"aText"})
            RestPage_aData = soup_rest.findAll("div", {"class":"aData"})
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
                fbdata = ';FB_URL: ' + x[0]
                f.write(fbdata.encode('ascii', 'ignore').decode('ascii'))

    #       aTarray = []
    #       for aText,aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
    #           aT = aText.contents
    #           aTarray.append(str(aT[0]))

    #       i = 0
    #       for i in range(len(aTarrayCorrect)):
    #            if aTarrayCorrect[i] != aTarray[i]:
    #                aTarray.insert(i,'!'+aTarrayCorrect[i])


            aDarray = {"Address":None, "Categories":None, "Amenities":None, "Features":None, "Timings":None, "Price Range":None}
            #aDarray["Address"] = sa[0]+ ''+ar[0]+ '' +aD[3]
            #print aDarray

            for aText,aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
                aT = aText.contents
                aD = aData.contents


                #print(str(aD))
                #print "\n"
                #f.write(' \n '+aT[0] +' : \n')

                try:

                    if 'Photos' in str(aT[0]):
                        continue

                    if 'Address' in str(aT[0]):
                        #f.write(str(aT[0]))
                        #print(aD)
                        #f.write((";Address:").encode('ascii', 'ignore').decode('ascii'))

                        #print(len(aD))
                        #print(str(aD[0].contents))
                        #print(str(aD[1].findAll("a")))
                        sa = aD[0].contents
                        #print(str(sa[0]))
                        ar = aD[2].contents
                        #print(str(sa[0])+ str(ar[0]) + str(aD[3]))
                        k=sa[0]+ ''+ar[0]+ '' +aD[3]

                        #f.write(sa[0]+ ''+ar[0]+ '' +aD[3])
                        aDarray["Address"] = str(k)
                        continue

                    if 'Categories' in str(aT[0]):
                        cus = aData.findAll("a")
                        #print('yahoo1')
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)))
                        #cus = cus[1]

                        #f.write((";Categories:").encode('ascii', 'ignore').decode('ascii'))

                        if len(cus)==0:
                            #f.write('null')
                            pass
                        cuarray = []
                        for cu_itr in range(0,len(cus)):
                            cu = cus[cu_itr].contents
                            cuarray.append(str(cu[0]))
                            #print(cu)
                            #print(str(cu[0]))
                            #f.write(cu[0]+ ' ,' )
                        aDarray["Categories"] = cuarray
                        continue

                    if 'Features' in str(aT[0]):
                        cus = aData.findAll("span")
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)/2))
                        #cus = cus[1]
                        #print('yahoo1')
                        #f.write((";Features:").encode('ascii', 'ignore').decode('ascii'))

                        if len(cus)==0:
                            #f.write('null')
                            pass

                        cuarray = []
                        for cu_itr in range(0,((len(cus)/2))):
                            cu = cus[2*cu_itr].contents
                            cuarray.append(str(cu[1]))
                            if str(cu[1]) not in features:
                                features.append(str(cu[1]))
                            #print(cu)
                            #print(str(cu[1]))
                            #f.write(cu[1]+ ' ,' )
                        aDarray["Features"] = cuarray
                        continue

                    if 'Amenities' in str(aT[0]):
                        cus = aData.findAll("span")
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)/2))
                        #cus = cus[1]
                        #print('yahoo1')
                        #f.write((";Amenities:").encode('ascii', 'ignore').decode('ascii'))
                        if len(cus)==0:
                            #f.write('null')
                            pass
                        cuarray = []
                        for cu_itr in range(0,((len(cus)/2))):
                            cu = cus[2*cu_itr].contents
                            cuarray.append(str(cu[1]))
                            if str(cu[1]) not in amenities:
                                amenities.append(str(cu[1]))
                            #f.write(cu[1]+ ' ,' )
                        #print(cuarray)
                        aDarray["Amenities"] = cuarray
                        #for val in amenities:
                        #    if val in cuarray:
                        #        k = val+","
                        #        aDarray["Amenities"] = str(k)
                                #f.write(k.encode('ascii', 'ignore').decode('ascii'))
                        #    else:
                        #        k=","
                                #f.write(k.encode('ascii', 'ignore').decode('ascii'))
                        continue

                    if 'Price Range' in str(aT[0]):
                        #cus_gud = aData.findAll("div")
                        #c_gud = cus_gud[0].contents
                        aTemp = aData.findAll("span")
                        #print(aTemp)
                        #print(str(aTemp[0].contents))
                        #f.write((";Price Range:").encode('ascii', 'ignore').decode('ascii'))
                        x_tp = 'null'
                        x_tp = aTemp[0].contents
                        #print(str(x_tp[0]))
                        k = x_tp[0].encode('ascii', 'ignore').decode('ascii')
                        aDarray["Price Range"] = str(k)
                        #f.write(x_tp[0].encode('ascii', 'ignore').decode('ascii') +' ,')

                    if 'Timings' in str(aT[0]):
                        cus = aData.findAll("div")
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)/2))
                        #cus = cus[1]
                        #print('yahoo1')
                        #f.write((";Amenities:").encode('ascii', 'ignore').decode('ascii'))
                        k = {"Check-in":None, "Check-out":None}
                        if len(cus)==0:
                            #f.write(';Check-in:null;Check-out:null')
                            pass
                        else:
                            cuin = cus[0].contents
                            #print(cu)
                            #print(str(cu[1]))
                            #print(cu)
                            #f.write(';Check-in:'+cu[1] )
                            cuout = cus[1].contents
                            #print(cu[1])
                            #print(str(cu[1]))
                            #f.write(';Check-out:'+cu[1] )
                            k["Check-in"] = str(cuin[1])
                            k["Check-out"] = str(cuout[1])
                        aDarray["Timings"] = k
                        continue



                    #print(";" + str(aT[0]) + " :" + str(aD[0]))
                    #f.write((';' + str(aT[0]) + ':' + str(aD[0])).encode('ascii', 'ignore').decode('ascii') )
                except:
                    continue

            #for key in aDarray:
            #    print key,";",aDarray[key]


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

            if aDarray["Amenities"] == None:
                f.write((';Amenities:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Amenities:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Amenities"])):
                    f.write((aDarray["Amenities"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Features"] == None:
                f.write((';Features:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Features:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Features"])):
                    f.write((aDarray["Features"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Timings"] == None:
                f.write((';Check-in:;Check-out:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Check-in:'+(aDarray['Timings']["Check-in"])+';Check-out:'+(aDarray['Timings']["Check-out"]).encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Price Range"] == None:
                f.write((';Price Range:;').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write(';Price Range:'+(aDarray["Price Range"])+";".encode('ascii', 'ignore').decode('ascii'))



err.write("\n\nTotal errors while retrieving main pages: "+str(len(errors))+'\n'.encode('ascii', 'ignore').decode('ascii'))
err.write('Total hotel links that showed error: '+str(totalcount).encode('ascii', 'ignore').decode('ascii'))


