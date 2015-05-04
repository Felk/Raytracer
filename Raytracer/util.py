'''
Created on 04.05.2015

@author: Felk
'''
from __future__ import division

from math import sqrt


class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        if type(other) is Vector3:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise Exception("invalid operand for Vector3 addition: " + repr(type(other)))
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return Vector3(self.x * other, self.y * other, self.z * other)
        elif type(other) is Vector3:
            # cross multiplication by default. use dot() for dot product
            return Vector3(self.y * other.z - self.z * other.y,
                          self.z * other.x - self.x * other.z,
                          self.x * other.y - self.y * other.x)
        else:
            raise Exception("invalid operand for Vector3 multiplication: " + repr(type(other)))
            
    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)
       
    def __neg__(self):
        return self * -1
         
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalized(self):
        return self / self.length()
    
    def clamp(self, mi, ma):
        self.x = min(ma, max(mi, self.x))
        self.y = min(ma, max(mi, self.y))
        self.z = min(ma, max(mi, self.z))
    
    def __repr__(self):
        return 'Vector3(%f, %f, %f)' % (self.x, self.y, self.z)
             
        
class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
        
    def pointAt(self, t):
        return self.origin + self.direction * t
