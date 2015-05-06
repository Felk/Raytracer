'''
Created on 04.05.2015

@author: Felk
'''

class Material(object):
    def __init__(self, color, ka=0.3, kd=0.7, ks=0.3, n=80, reflect=0.5, transparency=0, refract=1):
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.n = n
        self.reflect = reflect
        self.transparency = transparency
        self.refract = refract
        
    def colorAt(self, p):
        return self.color

class MaterialCheckerboard(Material):
    def __init__(self, color1, color2, checksize=2, ka=0.3, kd=0.7, ks=0.3, n=80, reflect=0, transparency=0, refract=1):
        self.color1 = color1
        self.color2 = color2
        self.checksize = checksize
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.n = n
        self.reflect = reflect
        self.transparency = transparency
        self.refract = refract
        
    def colorAt(self, p):
        p = p / self.checksize
        x = int(abs(p.x) + 0.5)
        z = int(abs(p.z) + 0.5)
        if (x + z) % 2:
            return self.color1
        return self.color2