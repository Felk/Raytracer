'''
Created on 04.05.2015

@author: Felk
'''

from __future__ import division

from math import pi

from display import Resolution, View, Camera
from objects import Sphere, Plane, Triangle
from util import Vector3, Ray
from material import Material


res = Resolution(400, 400)
BG_COLOR = Vector3(0, 0, 0)
AMBIENT_COLOR = Vector3(0.4, 0.4, 0.4)
LIGHT = Vector3(30, 30, 10)

fov    = 45
eye    = Vector3(0, 1.8, 10)
center = Vector3(0, 3, 0)
up     = Vector3(0, 1, 0)

camera = Camera(fov / 360 * pi, eye, center, up)
view = View(res, camera)

objects = [
           Sphere(Material(Vector3(1, 0, 0)), Vector3(0, 5, -14), 1),
           Sphere(Material(Vector3(0, 1, 0)), Vector3(1.41, 3, -14), 1),
           Sphere(Material(Vector3(0, 0, 1)), Vector3(-1.41, 3, -14), 1),
           Plane(Material(Vector3(0.6, 0.6, 0.6)), Vector3(0,0,0), Vector3(0,1,0)),
           Triangle(Material(Vector3(1, 1, 0)), Vector3(0, 5, -16), Vector3(2, 3, -16), Vector3(-2, 3, -16)),
          ]

for x in range(res.width):
    for y in range(res.height):
        
        ray = view.rayAt(x, y)
        maxdist = float('inf')
        color = BG_COLOR
        
        for o in objects:
            param = o.intersectionParameter(ray)
            if param:
                if param < maxdist:
                    maxdist = param
                    
                    intersect = ray.pointAt(param)
                    l = (LIGHT - intersect).normalized()
                    lightRay = Ray(intersect, l)
                    color = AMBIENT_COLOR * o.mat.ka # ambient light
                    shadow = False
                    for o2 in objects:
                        if o2 == o: continue
                        param2 = o2.intersectionParameter(lightRay)
                        if param2:
                            shadow = True
                            break
                    if not shadow:
                        d = (intersect - camera.eye).normalized()
                        n = o.normalAt(intersect)
                        lr = d - n * d.dot(n) * 2
                        # calc color with Phong
                        color += o.mat.color * o.mat.kd * n.dot(l) # diffuse light
                        color += o.mat.color * o.mat.ks * lr.dot(-d) #specular light 
                    
                    color.clamp(0, 1) # TODO is this really necessary or is there a bug?
                 
        view.putpixel((x, y), color)
        
    print x, '/', res.width
                                
view.save('a.png')

