import requests
from bs4 import BeautifulSoup
import itertools
import io
import re

url = 'http://www.zootout.com/delhi/attractions'
url = 'http://www.zootout.com/attraction/loadAttractionList/delhi/81'
r = requests.get(url)
soup = BeautifulSoup(r.content)
#MainPage_results = soup.findAll("div", {"class":"results"})
#MainPage_phone = MainPage_results[0].findAll("div", {"class":"phone attr"})
#MainPage_area = MainPage_results[0].findAll("span", {"class":"asset_icon tiny_address"})
#MainPage_attr = MainPage_results[0].findAll("span", {"class":"attraction_icons tiny_good"})

MainPage_phone = soup.findAll("div", {"class":"phone attr"})
MainPage_area = soup.findAll("span", {"class":"asset_icon tiny_address"})
MainPage_attr = soup.findAll("span", {"class":"attraction_icons tiny_good"})

for h3, m, ar, gf in itertools.izip_longest(soup.findAll("h3"), MainPage_phone, MainPage_area, MainPage_attr):

    f = io.open('C:/New folder (2)/3bandar/attractions/delhi/ZootoutAttractionsData-NCR-81-84.txt','a',encoding='utf-16')
    
    # Title
    #print(h3.parent)
    name_attr = h3.findAll("a")
    name_at = name_attr[0].contents
    print(name_at)        
    f.write('\n\n Attraction Name: ' + name_at[0]+ ';')

    # Link to Restraunt        
    #print('https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
    url_rest = 'https://www.zootout.com/' + name_attr[0].get("href").encode('ascii', 'ignore').decode('ascii')

    # Telephone
    tel_onclick = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
    tel_split = tel_onclick.split("'")
    #print(str(tel_split[1]) + '\n')
    f.write('Tel: ' + tel_split[1] + ';')  

    # Area    
    area = ar.parent
    name_at = area.contents
    #print(name_at)
    ar_tuple = name_at[1]
    #print(str(ar_tuple))        
    f.write('Area: ' + ar_tuple + ';')
    
    # Good For    
    good = gf.parent
    good_for = good.contents
    #print(good_for)
    gf_tuple = ''
    if len(good_for) > 1:
        gf_tuple = good_for[1]
    #print(str(gf_tuple))        
    f.write(('Good For: ' + str(gf_tuple) + ';').encode('ascii', 'ignore').decode('ascii'))

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
    coordinate = ''
    for m in itertools.izip_longest(RestPage_mapdata):
        #print('yahoo')
        x = RestPage_mapdata[0].contents
        #print(x[1])
        x_sp = x[1].contents
        x_loc = x_sp[0].split("/")
        lo = "lon:" + x_loc[4] 
        la = "lat:" + x_loc[5]
        coordinate = lo + ";" + la
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
            
            print(";" + str(aT[0]) + " :" + str(aD[0]))
            f.write((';' + str(aT[0]) + ':' + str(aD[0])).encode('ascii', 'ignore').decode('ascii') )
        except:
            continue

##    for aText,aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
##        aT = aText.contents
##        aD = aData.contents
##        f.write(' \n '+aT[0] +' : \n')
##
##        if 'Photos' in str(aT[0]):
##            continue            
##
##        if 'Address' in str(aT[0]):
##            #f.write(str(aT[0]))
##            print(str(aT[0]))
##            f.write('; Address:' + aT[0] +';')            
##
##        if 'Address' in str(aT[0]):
##            #f.write(str(aT[0]))
##            print(str(aT[0]))
##            f.write('; Address:' + aT[0] +';')
##
##        if 'Attraction ' in str(aT[0]):
##            cus = aData.findAll("span")
##            #print(cus)
##            #cus = cus[0].contents
##            #print(str(len(cus)/2))
##            #cus = cus[1]
##            #print('yahoo1')                
##            for cu_itr in range(0,((len(cus)/2))):
##                cu = cus[2*cu_itr].contents
##                #print(cu)
##                print(str(cu[1]))
##                f.write(cu[1]+ ' ,' )
##            
##        if 'What\'s Good' in str(aT[0]):
##            cus_gud = aData.findAll("div")
##            c_gud = cus_gud[0].contents
##            print(str(c_gud[0]))
##            f.write(c_gud[0] +' ,')
##
##        if 'Services' in str(aT[0]):
##            cus = aData.findAll("span")
##            #print(cus)
##            #cus = cus[0].contents
##            #print(str(len(cus)/2))
##            #cus = cus[1]
##            #print('yahoo1')                
##            for cu_itr in range(0,((len(cus)/2))):
##                cu = cus[2*cu_itr].contents
##                #print(cu)
##                print(str(cu[1]))
##                f.write(cu[1]+ ' ,' )    
##
##        if 'Buffet' in str(aT[0]):
##            #cus_gud = aData.findAll("div")
##            #c_gud = cus_gud[0].contents
##            aTemp = aData
##            #print(aTemp)
##            print(str(aTemp).replace('<br/>',' , '))
##            x_tp = str(aTemp).replace('<br/>',' , ')
##            f.write(x_tp.encode('ascii', 'ignore').decode('ascii') +' ,')
##
##        if 'Price Range' in str(aT[0]):
##            #cus_gud = aData.findAll("div")
##            #c_gud = cus_gud[0].contents
##            aTemp = aData
##            #print(aTemp)
##            print(str(aTemp))
##            x_tp = str(aTemp)
##            f.write(x_tp.encode('ascii', 'ignore').decode('ascii') +' ,')
##
##            #if 'Timings' in str(aT[0]):
##
##        
##   
##    # Good For    
##    MainPage_textdata = soup.findAll("div", {"class":"restaurant"})
##    MainPage_add = soup.findAll("span", {"class":"address attr"})
##    MainPage_area = soup.findAll("strong")
##    MainPage_cuisine = soup.findAll("div", {"class":"res-snippet-small-cuisine"})
##    MainPage_tel = soup.findAll("p", {"class":"ctv_phone attr"})
##    MainPage_cost_cat = soup.findAll("span", {"class":"cost_value attr"})
##    #print(MainPage_textdata)
##        #MainPage_text = MainPage_textdata[0].text
##    
##        #MainPage_link = 'en.wikipedia.org' + MainPage_textdata[0].find_all("a")[-1].get("href")
##    
##        # if __name__ == "__main__":
##    
##    for i,j,k,m,n in itertools.izip_longest(MainPage_textdata, MainPage_add, MainPage_area, MainPage_tel, MainPage_cost_cat):
##
##        # Title
##        title = i.find_all("a")
##        title_str = title[0].contents
##        print(title_str)
##        f.write('\n\n Restraunt Name: ' + title_str[0]+ '\n')
##        
##        #print(str(i) + '\n')
##
##        # Link to Restraunt        
##        print('https://www.zootout.com/' + title[0].get("href").encode('ascii', 'ignore').decode('ascii')+ '\n')
##        url_rest = 'https://www.zootout.com/' + title[0].get("href").encode('ascii', 'ignore').decode('ascii')
##
##        # Address
##        add = j.contents
##        print(add[0] + '\n')
##        f.write(add[0]+ '\n')
##
##        # Area
##        area = k.contents
##        print(str(area[0]) + '\n')
##        f.write('Area: ' + area[0]+ '\n')
##
##        # Telephone
##        tel = m.get("onclick").encode('ascii', 'ignore').decode('ascii')
##        print(str(tel) + '\n')
##        f.write('Tel: ' + tel+ '\n')
##        
##        # Economic Category        
##        econ = n.contents
##        print(str(econ[0]) + '\n')
##        f.write('Econ Category: ' + econ[0] + '\n')                
##        
##        r_rest = requests.get(url_rest)
##        soup_rest = BeautifulSoup(r_rest.content)
##        RestPage_maplat = soup_rest.findAll("meta", {"property":"zootoutcom:location:latitude"})
##        RestPage_maplong = soup_rest.findAll("meta", {"property":"zootoutcom:location:longitude"})
##        #lat = RestPage_maplat[0].encode('ascii', 'ignore').decode('ascii')
##        #print(lat)
##        #f.write('Lat:'+ str(lat.get("content")))
##        #f.write('Long:'+ RestPage_maplong[0].get("content"))
##
##        RestPage_aText = soup_rest.findAll("span", {"class":"aText"})
##        RestPage_aData = soup_rest.findAll("div", {"class":"aData"})
##
##        for lat, lon in itertools.izip_longest(RestPage_maplat, RestPage_maplong):
##            f.write('lat: '+ lat.get("content").encode('ascii', 'ignore').decode('ascii') + '\n')
##            f.write('lon: '+ lon.get("content").encode('ascii', 'ignore').decode('ascii') + '\n')                        
##
##        for aText,aData in itertools.izip_longest(RestPage_aText, RestPage_aData):
##            aT = aText.contents
##            aD = aData.contents
##            f.write(' \n '+aT[0] +' : \n')
##
##            if 'Categories' in str(aT[0]):
##                #f.write(str(aT[0]))
##                cat = aData.findAll("a");
##                for ca in cat:
##                    cc = ca.contents
##                    print(str(cc[0]))
##                    f.write(cc[0] +' ,')
##
##            if 'Cuisines' in str(aT[0]):
##                cus = aData.findAll("span")
##                #print(cus)
##                #cus = cus[0].contents
##                #print(str(len(cus)/2))
##                #cus = cus[1]
##                #print('yahoo1')                
##                for cu_itr in range(0,((len(cus)/2))):
##                    cu = cus[2*cu_itr].contents
##                    #print(cu)
##                    print(str(cu[1]))
##                    f.write(cu[1]+ ' ,' )
##                
##            if 'What\'s Good' in str(aT[0]):
##                cus_gud = aData.findAll("div")
##                c_gud = cus_gud[0].contents
##                print(str(c_gud[0]))
##                f.write(c_gud[0] +' ,')
##
##            if 'Services' in str(aT[0]):
##                cus = aData.findAll("span")
##                #print(cus)
##                #cus = cus[0].contents
##                #print(str(len(cus)/2))
##                #cus = cus[1]
##                #print('yahoo1')                
##                for cu_itr in range(0,((len(cus)/2))):
##                    cu = cus[2*cu_itr].contents
##                    #print(cu)
##                    print(str(cu[1]))
##                    f.write(cu[1]+ ' ,' )    
##
##            if 'Buffet' in str(aT[0]):
##                #cus_gud = aData.findAll("div")
##                #c_gud = cus_gud[0].contents
##                aTemp = aData
##                #print(aTemp)
##                print(str(aTemp).replace('<br/>',' , '))
##                x_tp = str(aTemp).replace('<br/>',' , ')
##                f.write(x_tp.encode('ascii', 'ignore').decode('ascii') +' ,')
##
##            if 'Price Range' in str(aT[0]):
##                #cus_gud = aData.findAll("div")
##                #c_gud = cus_gud[0].contents
##                aTemp = aData
##                #print(aTemp)
##                print(str(aTemp))
##                x_tp = str(aTemp)
##                f.write(x_tp.encode('ascii', 'ignore').decode('ascii') +' ,')
##
##            #if 'Timings' in str(aT[0]):
##
##        RestPage_dowt = soup_rest.findAll("span", {"class":"dow"})
##        RestPage_time = soup_rest.findAll("span", {"class":"timing"})
##
##        #f.write('\n Timing: \n' )
##        for dow, time in itertools.izip_longest(RestPage_dowt, RestPage_time):
##            d_c = dow.contents
##            t_c = time.contents
##            print(d_c[0] + ' , ' + t_c[0])
##            f.write(d_c[0] + ' , ' + t_c[0])
##            
##                
        
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

        

            
