'''
Created on 04.05.2015

@author: Felk
'''

class Material(object):
    def __init__(self, color, ka=0.3, kd=0.7, ks=0.3, n=80, reflect=0.5):
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.n = n
        self.reflect = reflect
