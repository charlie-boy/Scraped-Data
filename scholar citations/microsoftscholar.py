#-------------------------------------------------------------------------------
# Name:        NGD extractor
# Author:      Kartik
#
# Created:     11-06-2014
#-------------------------------------------------------------------------------
import time
import math
import glob
import sys
import urllib, urllib2
from bs4 import BeautifulSoup, Comment

def Distance(x,y,xy):
    fx=math.log(float(x))
    fy=math.log(float(y))
    fxy=math.log(float(xy))
    M=math.log(3539277)
    NGD=(max(fx,fy)-fxy)/(M-min(fx,fy))
    return NGD

# This is the function which sends queries on Microsoft Search Engine and retrieve results. You can send paper names as String a. Remove String b in your case.
def bs(a,b,val1,val2,fand):
    Stringa=a.replace(" ","%20")
    Stringb=b.replace(" ","%20")
    fand.write(a+' '+b);
    url='http://academic.research.microsoft.com/Search?query="'+Stringa+'"%20"'+Stringb+'"';
    content = urllib2.urlopen(url).read()
# The Soup object stores the html source code of the URL page and initiates a parser on that.
    soup = BeautifulSoup(content, "html.parser")
    if soup.find_all('span',attrs={"class" : "item-count"}):
# You need to know the exact tags in which your relevant information is stored. Change those tags below.
        for row in soup.find_all('span',attrs={"class" : "item-count"}):
            n1=int(row.text.replace("(","").replace(")",""));
            fand.write(' '+str(n1));
            fand.write('\n');
            fand.flush();
    else:
        return 100000;
    print "------------"+str(n1)
    ngd=Distance(val1,val2,n1)
    return ngd;

i=0;
j=0;
keywordlist=[];
keywordvaluelist=[];
nodelist=[];
nodevaluelist=[];
print 'Program initialized'
fcounter=open('Counter.txt','w');
fand=open('join13_455.txt','w');
fwrite=open('LabelValueskey13_4.txt','w');
with open('Values2.txt') as fkeywords:
    for String1 in fkeywords:
        value=String1.rsplit(' ',1)[1];
        value=value.rstrip('\n');
        String1=String1.rsplit(' ',1)[0];
        keywordlist.append(String1);
        keywordvaluelist.append(value);
        i=i+1;
with open('Values1.txt') as fp:
    for String2 in fp:
        value=String2.rsplit(' ',1)[1];
        value=value.rstrip('\n');
        String2=String2.rsplit(' ',1)[0];
        String2=String2.replace('*','');
        nodelist.append(String2);
        nodevaluelist.append(value);
        j=j+1;
print keywordlist;
k=12;
l=455;
error=0;
while k<len(keywordlist):
        String1=keywordlist[k];
        value1=keywordvaluelist[k];
        if k==13:
            break;
        k=k+1;
        if k>=14:
            l=0;
        fwrite.write('\n');
        while l<len(nodelist):
            String2=nodelist[l];
            value2=nodevaluelist[l];
            l=l+1;
            try:
                if (value1=='-1') or (value2=='-1'):
                    n=10000;
                else:
                    n=bs(String1,String2,value1,value2,fand)
                fwrite.write(str(n)+',');
                fwrite.flush();
# Timer for the scheduled querying
                if l%500==0:
                    fwrite.flush();
                    time.sleep(300);
                print str(l)
            except Exception, e:
                print str(e);
                print String1, String2;
                l=l-1;
                error=error+1;
                fwrite.flush();
                fcounter.write(str(k)+','+str(l)+','+str(error));
                fcounter.write(str(e));
                fcounter.write('\n');
                fcounter.flush();
fwrite.close()
fcounter.close()
