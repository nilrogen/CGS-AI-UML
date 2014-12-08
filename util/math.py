"""
" AUTHOR: Michael Gorlin
" DATE: 2014-12-05
"
" This module contains various mathematical functions. Many of these
" functions are related changing pygame.Rect objects, a functionality
" that is desired in some situations.
"""

from pygame import Rect
from pygame.locals import *

def addPoint(point, dv):
    return (point[0] + dv[0], point[1] + dv[1])

def addRect(rect, dp, ds=(0, 0)):
    dx, dy = dp
    dw, dh = ds
    return Rect(rect.x+dx, rect.y+dy, rect.w+dw, rect.h+dh)

def scaleRect(rect, dp, ds=(1, 1)):
    dx, dy = dp
    dw, dh = ds
    return Rect(rect.x*dx, rect.y*dy, rect.w*dw, rect.h*dh)

def centerToRect(dest, source):
    retv = dest.copy()    
    retv.center = source.center
    return retv
    
