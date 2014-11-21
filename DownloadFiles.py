import json
import os
import urllib2
import glob

CURDIR = os.getcwd()
JSONPATH = os.path.join(CURDIR, 'all-cards.json')
PICSPATH = os.path.join(CURDIR,'pics' + os.sep)

def loadJson():
    json_data = open(JSONPATH).read()
    pjson = json.loads(json_data)
    return pjson

def downloadCard(card):
    cname = filter(lambda c: c not in ' :\'', card["name"])
    cname += '.png'
    curl  = card["image_url"]

    os.chdir(PICSPATH)
    if cname in glob.glob('*.png'):
        return
    os.chdir("..")
    
    urldata = urllib2.urlopen(curl)
    cardpath = os.path.join(PICSPATH, cname)
    cardfile = open(cardpath, 'wb')

    print "Downloading: %s" % (cname)

    cardfile.write(urldata.read())
    cardfile.close()

        

if __name__ == '__main__':
    try:
        os.mkdir(PICSPATH)
    except OSError:
        print 'Space Created'
        pass
    
    json = loadJson()

    cards = json["cards"]
    for card in cards:
        downloadCard(card)
