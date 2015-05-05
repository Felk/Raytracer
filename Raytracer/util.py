'''
Created on 04.05.2015

@author: Felk
'''
from __future__ import division

from math import sqrt

class Vec3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        if type(other) is Vec3:
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise Exception("invalid operand for Vec3 addition: " + repr(type(other)))
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif type(other) is Vec3:
            # component multiplication by default. use dot() or cross() for others
            return Vec3(self.x * other.x,
                           self.y * other.y,
                           self.z * other.z)
        else:
            raise Exception("invalid operand for Vec3 multiplication: " + repr(type(other)))
            
    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)
       
    def __neg__(self):
        return self * -1
         
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)
    
    def reflect(self, n):
        return self - n * self.dot(n) * 2
    
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalized(self):
        return self / self.length()
    
    def clamp(self, mi, ma):
        self.x = min(ma, max(mi, self.x))
        self.y = min(ma, max(mi, self.y))
        self.z = min(ma, max(mi, self.z))
    
    def __repr__(self):
        return 'Vec3(%f, %f, %f)' % (self.x, self.y, self.z)
             
        
class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
        
    def pointAt(self, t):
        return self.origin + self.direction * t
