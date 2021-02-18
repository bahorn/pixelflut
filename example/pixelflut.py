import socket
import random
import time
import binascii
import sys
import math
import struct

class PixelFlut:
    """
    A quick and easy pixel flut client.
    """
    def __init__(self, remote):
        """
        Connects to the server.
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(remote)

    def set(self, x, y, value):
        """
        Change a pixel on the display.
        """
        self.s.send(
            bytes('PX {:g} {:g} {:s}\n'.format(x, y, value), 'ascii')
        )

    def get(self, x, y):
        """
        Gets the value of a pixel on the display.
        """
        self.s.send(bytes('PX {} {}\n'.format(x, y), 'ascii'))
        res = self.s.recv(1024)
        hexc = res[:-1].decode('ascii').split(' ')[-1]
        return tuple(bytes.fromhex(hexc))
    
    def dims(self):
        """
        Returns the dimensions of the screen.
        """
        self.s.send(b'SIZE\n')
        res = self.s.recv(1024).decode('ascii')
        return list(map(int, res[:-1].split(' ')[1:]))

    def clear(self):
        """
        A custom command, you probably don't need this.
        """
        self.s.send(b'CLEAR\n')


def clamp(x):
    """
    Limits the values into the range 0-255
    """
    return max(0, min(x, 255))

def rgba(r,g,b,a):
    """
    Packs an RGBA value in a form thats suitable for pixelflut.
    """
    color = struct.pack(
        'BBBB',
        clamp(r), clamp(g), clamp(b), clamp(a)
    )
    return binascii.hexlify(color).decode('ascii')

def random_color(alpha):
    """
    Returns a random color.
    """
    return rgba(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        alpha
    )
