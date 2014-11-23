"""
" AUTHOR: Michael Gorlin
" DATE:   2014-11-22
" 
" This module contains the tools to load the resources required for the ui. 
" Curently the only operation is to retrieve card image data and convert
" them to pygame surfaces when needed.
"
" TODO: Fix model of retrieving resources.
"""

import os
import glob

import pygame
from pygame.locals import * 

_INITIALIZED = False
_UTIL = None

def _init(picspath, carddatapath):
    global _INITIALIZED
    global _UTIL
    if _INITIALIZED:
        return
    _UTIL = Utilities(picspath, carddatapath)
    _INITIALIZED = True

class Utilities(object):
    def __init__(self, picspath, carddatapath):
        self.picspath = picspath
        self.carddatapath = carddatapath
        
        self.IMAGEDATA = {}
        self.imagelist = glob.glob(picspath + '*.png')
        self._loadImages()

    def _loadImages(self):
        for img in self.imagelist:
            imgpath = os.path.join(self.picspath, img)
            self.IMAGEDATA[img] = ImageData(imgpath)

    def getImageData(self, cardname):
        return self.IMAGEDATA.get(cardname)

    def getImageList(self):
        return self.imagelist

class ImageData(object):
    def __init__(self, imagepath):
        self.image = pygame.image.load(imagepath)
        self.convertedimage = None
        self.converted = False
    
    def isConverted(self):
        return self.converted

    def getConvertedImage(self):
        if self.converted:
            return self.convertedimage
        raise Exception('Image Not Converted')
    
    def convertImage(self, alpha):
        if self.converted:
            return
        if alpha:
            self.convertedimage = self.image.convert_alpha()
        else:
            self.convertedimage = self.image.convert()
        self.converted = True

def getGlobals():
    if not _INITIALIZED:
        _init(os.path.join(os.getcwd(), 'pics/'), None)
    return _UTIL
    

def getImage(imagename, alpha=True):
    """
    " This method will load pygame surface representation using the images name.
    " If the image has been converted already then that image will be returned,
    " otherwise it will be converted using either convert() or convert_alpha().
    " When the image name does not exist then an exception is raised.
    " Names are in the form [name].[imagetype].
    """
    imagedata = getGlobals().getImageData(imagename)
    if not imagedata:
        raise Exception('Image: %s, not found.' % (imagename))
    if imagedata.isConverted():
        return imagedata.getConvertedImage()
    imagedata.convertImage(alpha)
    return imagedata.getConvertedImage()
