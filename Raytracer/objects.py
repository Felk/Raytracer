'''
Created on 04.05.2015

@author: Felk
'''
from math import sqrt


class Light(object):
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos


class Sphere(object):
    def __init__(self, mat, center, radius):
        self.mat = mat
        self.center = center
        self.radius = radius
        
    def intersectionParameter(self, straight):  
        co = self.center - straight.origin
        v = co.dot(straight.direction)
        discr = v*v - co.dot(co) + self.radius**2
        
        if discr >= 0:
            root = sqrt(discr)
            return [v - root, v + root]
        return None  
    
    def normalAt(self, p):
        return (p - self.center).normalized()
    

class Plane(object):
    def __init__(self, mat, p, n):
        self.mat = mat
        self.p = p
        self.n = n.normalized()
        
    def intersectionParameter(self, straight):
        op = straight.origin - self.p
        a = op.dot(self.n)
        b = straight.direction.dot(self.n)
        
        if b:
            return [-a/b]
        return None
        
    def normalAt(self, p):
        return self.n
        
        
class Triangle(object):
    def __init__(self, mat, a, b, c):
        self.mat = mat
        self.a = a
        self.b = b
        self.c = c
        
        self.u = self.b - self.a
        self.v = self.c - self.a
        self.n = (self.v.cross(self.u)).normalized()
        
    def intersectionParameter(self, straight):
        w = straight.origin - self.a
        dv = straight.direction.cross(self.v)
        dvu = dv.dot(self.u)
        
        if dvu == 0.0:
            return None
        
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(straight.direction) / dvu
        
        if 0<=r<=1 and 0<=s<=1 and r+s<=1:
            return [wu.dot(self.v) / dvu];
        return None
        
    def normalAt(self, p):
        return self.n
    
        