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
_PICSPATH = None


def init():
    if _INITIALIZED:
        return
    


class Utilities:
    _single = None
    def __init__(self, picspath, carddatapath):
        if Utilities._single:
            raise Utilities._single
        self.picspath = picspath
        self.carddatapath = carddatapath
        
        self.IMAGEDATA = {}
        self.imagelist = glob.glob(picspath + '*.png')
        self._loadImages()
        Utilities._single = self

    def _loadImages(self):
        for img in self.imagelist:
            imgpath = os.path.join(self.picspath, img)
            self.IMAGEDATA[img] = ImageData(imgpath)

    def getImageData(self, cardname):
        return self.IMAGEDATA.get(cardname)

    def getImageList(self):
        return self.imagelist

class ImageData:
    def __init__(self, imagepath):
        self.image = pygame.image.load(imagepath)
        self.compiledimage = None
        self.compiled = False
    
    def isCompiled(self):
        return self.compiled

    def getCompiledImage(self):
        if self.compiled:
            return self.compiledimage
        raise Exception('Image Not Compiled')
    
    def compileImage(self, alpha):
        if self.compiled:
            return
        if alpha:
            self.compiledimage = self.image.convert_alpha()
        else:
            self.compiledimage = self.image.convert()
        self.compiled = True

def getGlobals():
    try:
        utils = Utilities(os.path.join(os.getcwd(), 'pics/'), None)
        return utils
    except Utilities, s:
        return s

def getImage(imagename, alpha=True):
    imagedata = getGlobals().getImageData(imagename)
    if not imagedata:
        raise Exception('Image: %s, not found.' % (imagename))
    if imagedata.isCompiled():
        return imagedata.getCompiledImage()
    imagedata.compileImage(alpha)
    return imagedata.getCompiledImage()
