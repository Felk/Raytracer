'''
Created on 05.05.2015

@author: Felk
'''

class Hit(object):
    def __init__(self, obj, positions):
        self.obj = obj
        self.pos = positions[0]
        self.posN = positions


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
            params = o.intersectionParameter(ray)
            if params and params[0] > 0.0001 and params[0] < maxdist:
                maxdist = params[0]
                intersect = Hit(o, [ray.pointAt(P) for P in params])
        return intersect

        
