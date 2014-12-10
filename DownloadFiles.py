# AUTHOR: Michael Gorlin
# DATE:   2014-11-21
# 
# Downloads hearthstone picture art from the all-cards.json file. 
# This file was found at: 
#   https://github.com/pdyck/hearthstone-db
#

import json
import os
from urllib.request import *
import glob

CURDIR = os.getcwd()
JSONPATH = os.path.join(CURDIR, 'all-cards.json')
PICSPATH = os.path.join(CURDIR,'pics' + os.sep)

def loadJson():
    """ Loads the JSON file and reads it into a map. """
    json_data = open(JSONPATH).read()
    pjson = json.loads(json_data)
    return pjson

def downloadCard(card):
    # remove bad space, colon, and apostrophy from card name. 
    cname = "".join(filter(lambda c: c not in ' .:\'', card["name"]))
    cname += '.png'

    curl  = card["image_url"]

    # Ignore cards that have already been downloaded 
    os.chdir(PICSPATH)
    if cname in glob.glob('*.png'):
        return
    os.chdir("..")
    

    urldata = urlopen(curl)
    cardpath = os.path.join(PICSPATH, cname)

    cardfile = open(cardpath, 'wb')

    print('Downloading: %s' % (cname))

    cardfile.write(urldata.read())
    cardfile.close()

        

if __name__ == '__main__':
    try:
        # Create pics directory if one does not exist
        os.mkdir(PICSPATH)
    except OSError:
        print('Space Created')
        pass
    

    # Download the cards
    json = loadJson()
    cards = json["cards"]
    for card in cards:
        downloadCard(card)
