'''
Created on 04.05.2015

@author: Felk
'''

from __future__ import division

from math import pi

from display import Resolution, View, Camera
from material import Material, MaterialCheckerboard
from objects import Sphere, Plane, Triangle, Light
from util import Vec3, Ray
from world import World
import time
from OpenGL.extensions import alternate

AA = 1
FILE = 'out.png'

BG_COLOR = Vec3(0.6, 0.6, 1)
MAX_DEPTH = 5  #  for raytracing

LIGHT_AMBIENT = Vec3(1, 1, 1)
lights = [Light(Vec3(0.9, 0.9, 0.9), Vec3(16, 30, 10)),
          #Light(Vec3(0.3, 0.3, 0.9), Vec3(-20, 30, 10)),
          # Und das? Wozu ist das?
          # Das ist blaues Licht.
          # Und was macht es?
          # Es leuchtet blau.
          # Verstehe...
          ]


fov = 45
eye = Vec3(0, 3.3, 10)
center = Vec3(0, 3, 0)
up = Vec3(0, 1, 0)
camera = Camera(fov / 360 * pi, eye, center, up)

res = Resolution(480, 270)
view = View(res, camera)

world = World()
world.add(Sphere(Material(Vec3(1, 0, 0)), Vec3(1.41, 3, -14), 1))
world.add(Sphere(Material(Vec3(0, 1, 0)), Vec3(-1.41, 3, -14), 1))
world.add(Sphere(Material(Vec3(0, 0, 1)), Vec3(0, 5, -14), 1))
world.add(Plane(MaterialCheckerboard(Vec3(0.9, 0.9, 0.9), Vec3(0.1, 0.1, 0.1)), Vec3(0, 0, 0), Vec3(0, 1, 0)))
world.add(Triangle(Material(Vec3(1, 1, 0), reflect=0), Vec3(0, 5, -16), Vec3(2, 3, -16), Vec3(-2, 3, -16)))

# TODO fixen! Brechung funktioniert nicht und macht bei einer Glasscheibe auch wenig Sinn
# world.add(Triangle(Material(Vec3(0.6, 1, 0.6), reflect=0, transparency=0.7, refract=0), Vec3(-6, 0, -11), Vec3(-1, 0, -18), Vec3(-6, 8, -11)))
world.add(Triangle(Material(Vec3(0.6, 1, 0.6), reflect=0.7), Vec3(1, 0, -18), Vec3(6, 0, -11), Vec3(6, 8, -11)))

def trace(ray, level=0):
    if level <= MAX_DEPTH:
        hit = world.getIntersection(ray)
        if hit:
            return shade(hit, level)
    return BG_COLOR

def shade(hit, level):
    this = hit.obj
    n = this.normalAt(hit.pos)
    
    vecToHit = (hit.pos - camera.eye).normalized()
    light = LIGHT_AMBIENT * this.mat.ka # ambient
    
    for L in lights:
        vecToLight = (L.pos - hit.pos).normalized()
        vecToLightR = vecToLight.reflect(n)
        rayToLight = Ray(hit.pos, vecToLight)
    
        # Lichtabgewandte Seite oder im Schatten?
        inShadow = vecToLight.dot(n) < 0 or world.getIntersection(rayToLight, this)
        
        if not inShadow:
            light += L.color * this.mat.kd * n.dot(vecToLight)  # diffus
            light += L.color * this.mat.ks * vecToLightR.dot(-vecToHit) ** this.mat.n  # spekular
    
    color = this.mat.colorAt(hit.pos) * light
    if this.mat.reflect > 0:
        rayReflected = vecToHit.reflect(n)
        color += trace(Ray(hit.pos, rayReflected), level + 1) * this.mat.reflect
    if this.mat.transparency > 0 and len(hit.posN) > 1:
        alternate = False
        rayRefracted = vecToHit
        curPos = hit.pos
        curN = n
        # TODO WIP
        for intersect in hit.posN:
            if not rayReflected: break;
            if alternate:
                rayRefracted = rayRefracted.refract(this.normalAt(intersect), this.mat.refract)
            else:
                rayRefracted = rayRefracted.refract(this.normalAt(intersect), 1/this.mat.refract)
            alternate = not alternate
        if rayRefracted:
            color += trace(Ray(hit.pos, rayRefracted), level + 1) * this.mat.transparency
    return color

def main():
    for x in range(res.width):
        for y in range(res.height):
            rays = view.raysAt(x, y, AA)
            color = Vec3(0, 0, 0)
            for ray in rays:
                color += trace(ray) * (1 / (AA*AA))
            color.clamp(0, 1)
            view.putpixel((x, y), color)
        print '%4.1f%%' % (100 * x / res.width)
    view.show()
    view.save(FILE)
    
if __name__ == '__main__':
    t1 = time.time()
    main()
    print 'baked image with %d*%d Antialiasing in %.2fs! saved as "%s"' % (AA, AA, time.time() - t1, FILE)

