import socket
import random
import time
import binascii
import sys
import math
import struct

class PixelFlut:
    def __init__(self, remote):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(remote)

    def set(self, x, y, value):
        self.s.send(
            bytes('PX {:g} {:g} {:s}\n'.format(x, y, value), 'ascii')
        )

    def get(self, x, y):
        self.s.send(bytes('PX {} {}\n'.format(x, y), 'ascii'))
        res = self.s.recv(1024)
        hexc = res[:-1].decode('ascii').split(' ')[-1]
        return tuple(bytes.fromhex(hexc))
    
    def dims(self):
        self.s.send(b'SIZE\n')
        res = self.s.recv(1024).decode('ascii')
        return list(map(int, res[:-1].split(' ')[1:]))


def clamp(x): 
  return max(0, min(x, 255))

def rgba(r,g,b,a):
    return binascii.hexlify(
        struct.pack('BBBB', clamp(r), clamp(g), clamp(b),
                    clamp(a))).decode('ascii')

def random_color(alpha):
    return rgba(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        alpha
    )

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
                    pf.set(x, y, rgba(0, 0, 0, 32))

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

if __name__ == '__main__':
    pf = PixelFlut(('localhost', 1338))
    print(pf.get(0,0))
    if len(sys.argv) < 2:
        exit()
    if sys.argv[1] == "random":
        Examples.random_walk(pf)
    elif sys.argv[1] == "grid":
        Examples.grid(pf)
    elif sys.argv[1] == "spiral":
        Examples.spiral(pf)
    else:
        Examples.clear(pf)
