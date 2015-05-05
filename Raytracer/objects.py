'''
Created on 04.05.2015

@author: Felk
'''
from math import sqrt

class Sphere(object):
    def __init__(self, mat, center, radius):
        self.mat = mat
        self.center = center
        self.radius = radius
        
    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discr = v**2 - co.dot(co) + self.radius**2
        
        if discr >= 0:
            param = v - sqrt(discr)
            if param > 0: return param
        return None

    def normalAt(self, p):
        return (p - self.center).normalized()
    

class Plane(object):
    def __init__(self, mat, p, n):
        self.mat = mat
        self.p = p
        self.n = n.normalized()
        
    def intersectionParameter(self, ray):
        op = ray.origin - self.p
        a = op.dot(self.n)
        b = ray.direction.dot(self.n)
        
        if b and -a/b > 0:
            return -a/b
        else:
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
        
    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction * self.v
        dvu = dv.dot(self.u)
        
        if dvu == 0.0:
            return None
        
        wu = w * self.u
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s<=1:
            param = wu.dot(self.v) / dvu
            if param > 0: return param;
        return None
        
    def normalAt(self, p):
        return (self.v * self.u).normalized()
    
        