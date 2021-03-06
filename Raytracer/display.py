'''
Created on 04.05.2015

@author: Felk
'''
from __future__ import division

from collections import namedtuple
from math import tan

import Image

from util import Ray


Resolution = namedtuple('Resolution', 'width height')

class Camera(object):
    def __init__(self, fov, eye, center, up):
        self.fov = fov
        self.eye = eye
        self.center = center
        self.up = up
        
        self.f = (self.center - self.eye).normalized()
        self.s = (self.f.cross(self.up)).normalized()
        self.u = self.s.cross(self.f)

class View(object):
    def __init__(self, res, camera):
        self.res = res
        self.camera = camera
        
        self.height = 2 * tan(camera.fov / 2)
        self.width = self.height * (res.width / res.height)
        
        self.image = Image.new('RGB', res)
        self.pixelWidth = self.width / (res.width - 1)
        self.pixelHeight = self.height / (res.height - 1)
        
    def raysAt(self, posX, posY, aa=1):
        rays = []
        stepX = self.pixelWidth / aa
        stepY = self.pixelHeight / aa
        for ix in range(aa):
            for iy in range(aa):
                x = self.camera.s * (posX * self.pixelWidth + ix * stepX - self.width / 2)
                y = self.camera.u * (posY * self.pixelHeight + iy * stepY - self.height / 2)
                rays.append(Ray(self.camera.eye, self.camera.f + x + y))
        return rays
    
    def putpixel(self, (x, y), color):
        c = int(255 * color.x) | (int(255 * color.y) << 8) | (int(255 * color.z) << 16)
        self.image.putpixel((x, self.res.height - 1 - y), c)
        
    def save(self, f):
        self.image.save(f)
    
    def show(self):
        self.image.show()
        
