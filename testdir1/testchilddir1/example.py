from pyshorteners import Shortener
import http

g = Shortener()

l = 'examplessss' 
i = 0
k = ''
while i < len(l):
    if i % 2 != 0:
        k += l[i].upper()
    else:
        k += l[i]
print(k)