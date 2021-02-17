import random
import time
import sys
import math
import struct
from PIL import Image

from pixelflut import random_color, rgba, PixelFlut

class Examples:
    @staticmethod
    def random_walk(pf):
        (width, height) = pf.dims()
        x = width/2
        y = height/2
        color = random_color(32)
        while True:
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            if (x > width) or (x < 0) or (y > height) or (y < 0):
                x = width/2
                y = height/2
                color = random_color(32)
            pf.set(x, y, color)

    @staticmethod
    def grid(pf):
        (width, height) = pf.dims()
        for k in range(0, width, 100):
            for v in range(0, width):
                pf.set(v, k, rgba(255, 255, 255, 64))
                pf.set(k, v, rgba(255, 255, 255, 64))

    @staticmethod
    def clear(pf):
        (width, height) = pf.dims()
        while True:
            for x in range(width):
                for y in range(height):
                    pf.set(x, y, rgba(0, 0, 0, 64))

    @staticmethod
    def spiral(pf):
        (width, height) = pf.dims()
        center_x = width/2
        center_y = height/2
        t = math.pi
        maxr = 50
        while True:
            t += 0.001
            t %= maxr
            x = abs(center_x + 2*math.floor(10*t*math.sin(t)))
            y = abs(center_y + 2*math.floor(10*t*math.cos(t)))
            pf.set(x, y,
                   rgba(255-math.floor(128*(t/maxr))
                        , math.floor(255*(t/maxr))
                        , 100-math.floor(64*(t/maxr)), 10))

    @staticmethod
    def image(pf):
        (width, height) = pf.dims()
        
        img = Image.open('covhack.png')
        rsz_x = 128
        rsz_y = 128
        rsz = img.resize((rsz_x, rsz_y))
        out = rsz.convert('1')
        offset_x = random.randint(0, width)
        offset_y = random.randint(0, height)
        t = 0
        while True:
            t += 0.1
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            offset_x += 50 #random.randint(0,width)
            offset_y += 50 #random.randint(0,height)
            for x in range(rsz_x):
                for y in range(rsz_y):
                    a = out.getpixel((x,y))
                    if a == 0:
                        continue
                    color = rgba(r, g, b, int(a))
                    pf.set(
                        int(offset_x+1*x) % width, 
                        int(offset_y+1*y) % height, 
                        color
                    )

samples = {
    'image': Examples.image,
    'grid': Examples.grid,
    'spiral': Examples.spiral,
    'clear': Examples.clear,
    'random': Examples.random_walk
}

if __name__ == '__main__':
    pf = PixelFlut(('entry.athon.uk', 1337))

    if len(sys.argv) < 2:
        exit()
    
    samples.get(
        sys.argv[1],
        lambda _: print('unknown function')
    )(pf)
