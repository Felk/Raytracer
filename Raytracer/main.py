'''
Created on 04.05.2015

@author: Felk
'''

from __future__ import division

from math import pi

from display import Resolution, View, Camera
from material import Material
from objects import Sphere, Plane, Triangle, Light
from util import Vec3, Ray
from world import World


BG_COLOR = Vec3(0, 0, 0)
MAX_DEPTH = 5  #  for raytracing

LIGHT_AMBIENT = Vec3(1, 1, 1)
LIGHT_POINT = Light(Vec3(1, 1, 1), Vec3(20, 30, 10))

fov = 45
eye = Vec3(0, 3.3, 10)
center = Vec3(0, 3, 0)
up = Vec3(0, 1, 0)
camera = Camera(fov / 360 * pi, eye, center, up)

res = Resolution(800, 800)
view = View(res, camera)

world = World()
world.add(Sphere(Material(Vec3(1, 0, 0)), Vec3(1.41, 3, -14), 1))
world.add(Sphere(Material(Vec3(0, 1, 0)), Vec3(-1.41, 3, -14), 1))
world.add(Sphere(Material(Vec3(0, 0, 1)), Vec3(0, 5, -14), 1))
world.add(Plane(Material(Vec3(0.6, 0.6, 0.6)), Vec3(0, 0, 0), Vec3(0, 1, 0)))
world.add(Triangle(Material(Vec3(1, 1, 0)), Vec3(0, 5, -16), Vec3(2, 3, -16), Vec3(-2, 3, -16)))

def trace(ray, level=0):
    if level <= MAX_DEPTH:
        hit = world.getIntersection(ray)
        if hit:
            return shade(hit, level)
    return BG_COLOR

def shade(hit, level):
    this = hit.obj
    n = this.normalAt(hit.pos)
    vecToLight = (LIGHT_POINT.pos - hit.pos).normalized()
    vecToLightR = vecToLight.reflect(n)
    rayToLight = Ray(hit.pos, vecToLight)
    vecToHit = (hit.pos - camera.eye).normalized()
    
    # Ambientes Licht
    light = LIGHT_AMBIENT * this.mat.ka  # ambient light
    
    # Lichtabgewandte Seite oder im Schatten?
    inShadow = vecToLight.dot(n) < 0 or world.getIntersection(rayToLight, this)
    
    if not inShadow:  # Diffuses und spekulares Licht
        light += LIGHT_POINT.color * this.mat.kd * max(0, n.dot(vecToLight))  # diffus
        light += LIGHT_POINT.color * this.mat.ks * max(0, vecToLightR.dot(-vecToHit) ** this.mat.n)  # spekular
    
    return this.mat.color * light + trace(Ray(hit.pos, vecToHit.reflect(n)), level + 1) * this.mat.reflect

for x in range(res.width):
    for y in range(res.height):
        color = trace(view.rayAt(x, y))
        color.clamp(0, 1)
        view.putpixel((x, y), color)
    print x, '/', res.width

# view.show()
view.save('a.png')

