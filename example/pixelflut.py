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
