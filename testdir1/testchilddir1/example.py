import pyshorteners
import http

g = pyshorteners 

l = 'examplessss' # this line should not show up even though it has 'pyshorteners' in it
i = 0
k = ''
while i < len(l):
    if i % 2 != 0:
        k += l[i].upper()
    else:
        k += l[i]
print(k)