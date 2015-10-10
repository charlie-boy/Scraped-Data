import requests
from bs4 import BeautifulSoup
import itertools
import io
import re

#url = 'http://www.zootout.com/delhi/attractions'
f = io.open('C:/New folder (2)/3bandar/attractions/delhi/ZootoutMovieTheatreData-NCR.txt','a',encoding='utf-16')

for idx in range(1,11):
    print('Processing ... ' + str(idx) )
    url = 'http://www.zootout.com/ajaxmovies/cinemaList/delhi/'+str(idx)

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
    except:
        print('Error')
        continue
        
    MainPage_results = soup.findAll("div", {"class":"resultset"})
    #MainPage_phone = MainPage_results[0].findAll("div", {"class":"phone attr"})
    #MainPage_area = MainPage_results[0].findAll("span", {"class":"asset_icon tiny_address"})
    #MainPage_attr = MainPage_results[0].findAll("span", {"class":"attraction_icons tiny_good"})

    #print('yahpp')
    MainPage_phone = soup.findAll("div", {"class":"phone"})
    #MainPage_area = soup.findAll("span", {"class":"asset_icon tiny_address"})
    MainPage_area = soup.findAll("span",{"class": "t2"})
    MainPage_attr = soup.findAll("span", {"class":"attraction_icons tiny_good"})
    MainPage_cost = soup.findAll("span", {"class":"cost_value attr"})

    for h3, m, ar, gf, cost in itertools.izip_longest(soup.findAll("h3"), MainPage_phone, MainPage_area, MainPage_attr, MainPage_cost):

        #print('yahoo22')
        
        # Title
        #print(h3)
        name_attr = h3.findAll("a")
        name_at = 'null'
        name_at = name_attr[0].contents
        #print(str(name_at[0]))        
        f.write('\n\n Cinema Name: ' + name_at[0]+ ';')

        # Link to Restraunt        
        #print('https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
        url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')

        # Telephone
        tel_onclick = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
        tel_split = 'null'
        tel_split = tel_onclick.split("'")
        #print(str(tel_split[1]) + '\n')
        if len(tel_split)==0:
            f.write((";Tel: null").encode('ascii', 'ignore').decode('ascii'))            
        else:
            f.write('Tel: ' + tel_split[1] + ';')  

        # Area
        #print(h3.parent)
        #print(ar)
        name_at = 'null'
        name_at = ar.contents    
        #print(str(name_at))
        if len(name_at)==0:
            f.write((";Area: null").encode('ascii', 'ignore').decode('ascii'))            
            #f.write('Area: ' + name_at[0] + ';')
        else:
            f.write('Area: ' + name_at[0] + ';')

        # Cost
##        #print(h3.parent)
##        cost_at = 'null'
##        cost_at = cost.contents    
##        #print(str(cost_at))
##        if len(cost_at)==0:
##            f.write((";Cost: null").encode('ascii', 'ignore').decode('ascii'))            
##        else:
##            f.write('Cost: ' + cost_at[0])        

        r_rest_loc = requests.get(url_rest + '/overview')
        soup_rest_loc = BeautifulSoup(r_rest_loc.content)
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
            coordinate = lo + ";" + la
            #print(coordinate)
            f.write(coordinate.encode('ascii', 'ignore').decode('ascii') )                           

        try:
            r_rest = requests.get(url_rest)
            soup_rest = BeautifulSoup(r_rest.content)
        except:
            print('Error')
            continue
        
        RestPage_aText = soup_rest.findAll("span", {"class":"aText"})
        RestPage_aData = soup_rest.findAll("div", {"class":"aData"})

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
                    f.write((";Address:").encode('ascii', 'ignore').decode('ascii'))

                    #print(len(aD))
                    #print(str(aD[0].contents))
                    #print(str(aD[1].findAll("a")))
                    sa = aD[0].contents
                    #print(str(sa[0]))
                    ar = aD[2].contents            
                    #print(str(sa[0])+ str(ar[0]) + str(aD[3]))
                    f.write(sa[0]+ ''+ar[0]+ '' +aD[3])
                    continue

                if 'Website' in str(aT[0]):                
                    cus = aData.findAll("span")
                    #print('yahoo1')
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)))
                    #cus = cus[1]
                    
                    f.write((";Website:").encode('ascii', 'ignore').decode('ascii'))
                    
                    if len(cus)==0:
                        f.write('null')
                    
                    for cu_itr in range(0,len(cus)):
                        cu = cus[cu_itr].contents
                        #print(cu)
                        #print(str(cu[0]))
                        f.write(cu[0]+ ' ,' )
                    continue

                if 'Services' in str(aT[0]):                
                    cus = aData.findAll("span")
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)/2))
                    #cus = cus[1]
                    #print('yahoo1')
                    f.write((";Services:").encode('ascii', 'ignore').decode('ascii'))

                    if len(cus)==0:
                        f.write('null')
                    
                    for cu_itr in range(0,((len(cus)/2))):
                        cu = cus[2*cu_itr].contents
                        #print(cu)
                        #print(str(cu[1]))
                        f.write(cu[1]+ ' ,' )
                    continue

                if 'Amenities' in str(aT[0]):                
                    cus = aData.findAll("span")
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)/2))
                    #cus = cus[1]
                    #print('yahoo1')
                    f.write((";Amenities:").encode('ascii', 'ignore').decode('ascii'))
                    if len(cus)==0:
                        f.write('null')
                    for cu_itr in range(0,((len(cus)/2))):
                        cu = cus[2*cu_itr].contents
                        #print(cu)
                        #print(str(cu[1]))
                        f.write(cu[1]+ ' ,' )
                    continue

                if 'Price Range' in str(aT[0]):
                    #cus_gud = aData.findAll("div")
                    #c_gud = cus_gud[0].contents
                    aTemp = aData.findAll("span")
                    #print(aTemp)
                    #print(str(aTemp[0].contents))
                    f.write((";Price Range:").encode('ascii', 'ignore').decode('ascii'))
                    x_tp = 'null'
                    x_tp = aTemp[0].contents
                    #print(str(x_tp[0]))
                    f.write(x_tp[0].encode('ascii', 'ignore').decode('ascii') +' ,')

                if 'Timings' in str(aT[0]):                
                    cus = aData.findAll("div")
                    #print(cus)
                    #cus = cus[0].contents
                    #print(str(len(cus)/2))
                    #cus = cus[1]
                    #print('yahoo1')
                    #f.write((";Amenities:").encode('ascii', 'ignore').decode('ascii'))
                    if len(cus)==0:
                        f.write(';Check-in:null;Check-out:null')
                    else:
                        cu = cus[0].contents
                        #print(cu)
                        #print(str(cu[1]))
                        #print(cu)
                        f.write(';Check-in:'+cu[1] )
                        cu = cus[1].contents
                        #print(cu[1])
                        #print(str(cu[1]))
                        f.write(';Check-out:'+cu[1] )                        
                    
                    continue


                
                #print(";" + str(aT[0]) + " :" + str(aD[0]))
                #f.write((';' + str(aT[0]) + ':' + str(aD[0])).encode('ascii', 'ignore').decode('ascii') )
            except:
                continue
