'''
Created on 05.05.2015

@author: Felk
'''

class Hit(object):
    def __init__(self, obj, pos):
        self.obj = obj
        self.pos = pos


class World(object):
    def __init__(self):
        self.objects = []
    
    def add(self, o):
        self.objects.append(o)
        
    def getIntersection(self, ray, exclude=None):
        maxdist = float('inf')
        intersect = None
        for o in self.objects:
            #if o == exclude: continue
            param = o.intersectionParameter(ray)
            if param and param > 0.0001 and param < maxdist:
                maxdist = param
                intersect = Hit(o, ray.pointAt(param))
        return intersect

        
