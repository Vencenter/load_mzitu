import urllib 
import urllib2 
import requests
import random 
import uuid,os


#img_url = "https://p.ssl.qhimg.com/dm/48_48_100/t017aee03b28107657b.jpg"

img_url="http://i.meizitu.net/2018/10/13c02.jpg"
img="http://i.meizitu.net/2018/11/06c35.jpg"

my_headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36",
   'Referer':'http://m.mzitu.com/15309'}

def read_txt(path):
    mt=[]
    f=open(path,'r')
    for t in f.readlines():
        mt.append(t)
    f.close()
    return mt
 
def down_load(img,my_headers):
    request =  urllib2.Request(url=img, headers=my_headers)
    response = urllib2.urlopen(request)
    pic=response.read()
    path_name=img.split('/')[-1]
    path_name=path_name.replace('\n','')
    new_name="pic/" + path_name
    
    if not os.path.exists(new_name):
        with open("%s" % new_name, "wb") as f:
            f.write(pic)
        
    print "downloading with urllib"
    
def main():
    path="data.txt"
    mt=read_txt(path)
    print len(mt)
    print len(set(mt))
    for f in mt:
        print f
        down_load(f,my_headers)
    print 'fininsh'.center(40,'-')
    
main()


