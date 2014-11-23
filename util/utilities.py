import os
import pygame
from pygame.locals import * 
import glob

class Utilities:
    __single = None
    def __init__(self, picspath, carddatapath):
        if Utilities.__single:
            raise Utilities.__single
        self.picspath = picspath
        self.carddatapath = carddatapath
        
        self.IMAGEDATA = {}
        self.imagelist = glob.glob(picspath + '*.png')
        self.__loadImages()
        Utilities.__single = self

    def __loadImages(self):
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
