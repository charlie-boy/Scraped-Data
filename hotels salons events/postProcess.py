__author__ = 'bigDaDDy'

##############################################################################
# 1. Enter location of txt file you want to post process in f variable
# 2. Enter the attribute names in the search array
##############################################################################


import io

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


search = ["categories", "amenities", "features"]             # Enter the attribute names

###########################################################################
# Edit path of files here #

f = io.open('D:/hotelDetails.txt','r+',encoding='utf-16')  # Enter location of txt file
g = io.open('D:/postProcess.txt','a',encoding='utf-16')

###########################################################################

object = []
i = None
for i in f.readlines():
    object.append(str(i))

object = remove_values_from_list(object, '\n')
i = 0
for i in range(len(object)):
    object[i] = object[i].split(';')


for attr in range(len(search)):

    attribute = []
    attrSet = []
    for a in range(len(object)):
        for b in range(len(object[a])):
            #print x[a][b].lower()
            if object[a][b].lower().find(search[attr]) == 0:
                attribute.append(object[a][b])
                #print object[a][b]
    i = 0
    for i in range(len(attribute)):
        attribute[i] = attribute[i][len(search[attr])+1:].split(',')
        #print attribute[i]

    for a in range(len(attribute)):
        for b in range(len(attribute[a])):
            if " ".join(attribute[a][b].split()) not in attrSet and attribute[a][b] != '' and attribute[a][b] != '\n':
                attrSet.append(" ".join(attribute[a][b].split()))

    print (attrSet)
    g.write(str(search[attr])+": ".encode('ascii', 'ignore').decode('ascii'))
    for val in attrSet:
        g.write(val+",".encode('ascii', 'ignore').decode('ascii'))

    g.write('\n\n'.encode('ascii', 'ignore').decode('ascii'))

