'''
Created on 04.05.2015

@author: Felk
'''

class Material(object):
    def __init__(self, color, ka=0.2, kd=0.9, ks=0.1):
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
