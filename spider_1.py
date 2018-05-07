import urllib
import re

def getHtml(url):
    page=urllib.urlopen(url)
    html=page.read()
    return html
def getImg(html):
    reg=r'src="(.+?\.jpg)" width'
    imgreg=re.compile(reg)
    imglist=re.findall(imgreg,html)
    with open(r"./list.txt","a") as f:
        for imgurl in imglist:
            f.write(imgurl+'\n')
        return "OK"

for page in range(1,47):
    k="list_1_"+str(page)+".html"
    html=getHtml("http://www.55156.com/a/rosi/"+k)
    print k+getImg(html)

x=1
with open("./list.txt") as f:
    for line in f.readlines():
        urllib.urlretrieve(line,"./a/%s.jpg"%x)
        x+=1
        print x
