import pyshorteners
import idna

# this line should not show up even though it has 'pyshorteners' in it
pyshorteners
# another comment line
pyshorteners # pyshorteners is also BEFORE the comment so this line should show up

idna
k = 0
for i in range(0,5):
    k += i*i