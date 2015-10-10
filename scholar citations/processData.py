__author__ = 'bigDaDDy'

import io

f = io.open('D:/publ.txt','r+',encoding='utf-16')
g = io.open('D:/paperTitles.txt','r+',encoding='utf-16')

a = ""
for line in f:
    if line[:2] == "#*":
        a = line[2:]
    if line[:2] == "#@":
        a = a + line[2:] + "\n\n"
        g.write(a)

f.close()
g.close()