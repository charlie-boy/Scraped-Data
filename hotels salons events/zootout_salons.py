import requests
from bs4 import BeautifulSoup
import itertools
import io
import re
import json

aDarray = {"Address":None, "Categories":None, "Services":None, "Service Types":None}

errors = []
errorCountUrl = 0
count = 0
totalcount = 0

#url = 'http://www.zootout.com/delhi/attractions'

###############################################################
# Edit path of files here #

f = io.open('C:/New folder (2)/3bandar/internship/himanshu_communication/himanshu_communication/SalonsData_India.txt','a',encoding='utf-16')
err = io.open('C:/New folder (2)/3bandar/internship/himanshu_communication/himanshu_communication/errorListSalons.txt','a',encoding='utf-16')
cityData = open('C:/New folder (2)/3bandar/internship/himanshu_communication/himanshu_communication/india_data.txt')

###############################################################

cities = json.load(cityData)

for city in cities:
    page = cities[city]["salons"]
    print "\nCity: "+city.upper()
    print "Total pages: ",page,"\n"

    for idx in range(1, page+1):
        print('Processing ... ' + str(idx) )
        url = 'http://www.zootout.com/salon/searchlist/'+city+'/salons/'+str(idx)

        if count == 0:
            pass
        else:
            err.write('\nSalons links that showed error: '+str(count).encode('ascii', 'ignore').decode('ascii'))
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


        MainPage_results = soup.findAll("div", {"class":"resultset"})
        #MainPage_phone = MainPage_results[0].findAll("div", {"class":"phone attr"})
        #MainPage_area = MainPage_results[0].findAll("span", {"class":"asset_icon tiny_address"})
        #MainPage_attr = MainPage_results[0].findAll("span", {"class":"attraction_icons tiny_good"})

        #print('yahpp')
        MainPage_phone = soup.findAll("p", {"class":"ctv_phone attr"})
        #MainPage_area = soup.findAll("span", {"class":"asset_icon tiny_address"})
        MainPage_area = soup.findAll("strong")
        MainPage_attr = soup.findAll("span", {"class":"attraction_icons tiny_good"})

        for h3, m, ar, gf in itertools.izip_longest(soup.findAll("h3"), MainPage_phone, soup.findAll("strong"), MainPage_attr):
            #print('yahoo22')

            # Title
            #print(h3)
            name_attr = h3.findAll("a")
            name_at = 'null'
            try:
                name_at = name_attr[0].contents
                print(str(name_at[0]))
                f.write('\n\nSalon Name:' + name_at[0])
            except:
                f.write('\n\nSalon Name:PLEASE MANUALLY ADD SALON NAME'.encode('ascii', 'ignore').decode('ascii'))
                url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')
                if count == 0:
                    err.write('\n\nIn url:'+url+' following links of salons showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\t\t\'ascii\' codec can\'t encode characters'+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1

            # Link to Restraunt
            #print('https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
            url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')
            f.write(';URL:' + url_rest)

            # Telephone
            tel_onclick = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
            tel_split = 'null'
            tel_split = tel_onclick.split("'")
            #print(str(tel_split[1]) + '\n')
            f.write(';Tel:' + tel_split[1])

            # Area
            #print(h3.parent)
            name_at = 'null'
            name_at = ar.contents
            f.write(';Area:'.encode('ascii', 'ignore').decode('ascii'))
            if len(name_at) != 0:
                 f.write(name_at[0])

            try:
                r_rest_loc = requests.get(url_rest + '/overview', timeout=5)
                soup_rest_loc = BeautifulSoup(r_rest_loc.content)
            except:
                #errors.append(url_rest + '/overview')
                if count == 0:
                    err.write('\n\nIn url:'+url+' following links of salons showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1
                continue

            #RestPage_maplat = soup_rest_loc.findAll("div", {"class":"info_section section_nearby"}).findAll("script",{"type":"text/javascript"})
            #RestPage_maplong = soup_rest_loc.findAll("div", {"class":"info_section section_nearby"}).findAll("script",{"type":"text/javascript"})
            #lat = RestPage_maplat[0].encode('ascii', 'ignore').decode('ascii')
            #print(lat)
            #f.write('Lat:'+ str(lat.get("content")))
            #f.write('Long:'+ RestPage_maplong[0].get("content"))

            soup_rest_loc = BeautifulSoup(r_rest_loc.content)
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
                f.write(coordinate.encode('ascii', 'ignore').decode('ascii') )

            try:
                r_rest = requests.get(url_rest, timeout=5)
                soup_rest = BeautifulSoup(r_rest.content)
            except:
                #errors.append(url_rest)
                if count == 0:
                    err.write('\n\nIn url: '+url+' following links of salons showed error-\n\n'.encode('ascii', 'ignore').decode('ascii'))
                err.write('\t'+url_rest+'\n'.encode('ascii', 'ignore').decode('ascii'))
                count = count + 1
                #print('Error')
                continue

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
                fbdata = ';FB_URL:' + x[0]
                f.write(fbdata.encode('ascii', 'ignore').decode('ascii'))

            for aText,aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
                aT = aText.contents
                aD = aData.contents
                #print(str(aT[0]))
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
                        #f.write(sa[0]+ ''+ar[0]+ '' +aD[3])
                        k = sa[0]+ ''+ar[0]+ '' +aD[3]
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

                    if 'Services' in str(aT[0]):
                        cus = aData.findAll("span")
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)/2))
                        #cus = cus[1]
                        #print('yahoo1')
                        #f.write((";Services:").encode('ascii', 'ignore').decode('ascii'))

                        if len(cus)==0:
                            #f.write('null')
                            pass

                        cuarray = []
                        for cu_itr in range(0,((len(cus)/2))):
                            cu = cus[2*cu_itr].contents
                            #print(cu)
                            #print(str(cu[1]))
                            cuarray.append(str(cu[1]))
                            #f.write(cu[1]+ ' ,' )
                        aDarray["Services"] = cuarray
                        continue

                    if 'Service Types' in str(aT[0]):
                        cus = aData.findAll("span")
                        #print(cus)
                        #cus = cus[0].contents
                        #print(str(len(cus)/2))
                        #cus = cus[1]
                        #print('yahoo1')
                        #f.write((";Service Types:").encode('ascii', 'ignore').decode('ascii'))
                        if len(cus)==0:
                            pass
                            #f.write('null')
                        cuarray = []
                        for cu_itr in range(0,((len(cus)/2))):
                            cu = cus[2*cu_itr].contents
                            cuarray.append(str(cu[1]))
                            #print(cu)
                            #print(str(cu[1]))
                            #f.write(cu[1]+ ' ,' )
                        aDarray["Service Types"] = cuarray
                        continue


                    #print(";" + str(aT[0]) + " :" + str(aD[0]))
                    #f.write((';' + str(aT[0]) + ':' + str(aD[0])).encode('ascii', 'ignore').decode('ascii') )
                except:
                    continue

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

            if aDarray["Services"] == None:
                f.write((';Services:').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Services:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Services"])):
                    f.write((aDarray["Services"][i]+",").encode('ascii', 'ignore').decode('ascii'))

            if aDarray["Service Types"] == None:
                f.write((';Service Types:;').encode('ascii', 'ignore').decode('ascii'))
            else:
                f.write((';Service Types:').encode('ascii', 'ignore').decode('ascii'))
                for i in range(len(aDarray["Service Types"])):
                    f.write((aDarray["Service Types"][i]+",").encode('ascii', 'ignore').decode('ascii'))
                f.write(';'.encode('ascii', 'ignore').decode('ascii'))


err.write("\n\nTotal errors while retrieving main pages: "+str(len(errors))+'\n'.encode('ascii', 'ignore').decode('ascii'))
err.write('Total salon links that showed error: '+str(totalcount).encode('ascii', 'ignore').decode('ascii'))
