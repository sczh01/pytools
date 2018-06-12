#!python2 
from collections import Counter
from pprint import pprint
fh=open("result.txt")
places=[]
for line in fh.readlines()[1:]:
    places.append(line.strip().split()[1])

# pprint(places)
place_d=Counter(places)

fh.close()

fh=open("pro_list.txt")
for pro in fh:
    print place_d[pro.strip()]