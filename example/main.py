import random
import time
import sys
import math
from PIL import Image

from pixelflut import random_color, rgba, PixelFlut

class Examples:
    """
    Our example codes.
    """
    @staticmethod
    def random_walk(pf):
        """
        Random walk, basically ends up looking like a cool fractal.
        """
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
        """
        This draws a general grid.
        """
        (width, height) = pf.dims()
        for k in range(0, width, 100):
            for v in range(0, width):
                pf.set(v, k, rgba(255, 255, 255, 64))
                pf.set(k, v, rgba(255, 255, 255, 64))

    @staticmethod
    def clear(pf):
        """
        Sets the screen to a single color.
        """
        (width, height) = pf.dims()
        while True:
            for x in range(width):
                for y in range(height):
                    pf.set(x, y, rgba(0, 0, 0, 64))

    @staticmethod
    def spiral(pf):
        """
        Draws a spiral
        """
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
            color = rgba(
                255-math.floor(128*(t/maxr)),
                math.floor(255*(t/maxr)),
                100-math.floor(64*(t/maxr)),
                10
            )
            pf.set(x, y, color)

    @staticmethod
    def image(pf):
        """
        Draws an image and makes it loop around the screen.
        """
        # Some generic default settings.
        t = 0
        rsz_x = 128
        rsz_y = 128
        direction_x = 1
        direction_y = 1
        speed = 128

        (width, height) = pf.dims()

        # Pick a random location to draw
        offset_x = random.randint(0, width % rsz_x) * rsz_x
        offset_y = random.randint(0, height % rsz_y) * rsz_y
        
        # Load, resize and make it a binary image.
        img = Image.open('covhack.png')
        rsz = img.resize((rsz_x, rsz_y))
        out = rsz.convert('1')
        
        while True:
            t += 0.01
            # Chose a random colour
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            offset_x += direction_x*speed
            offset_y += direction_y*speed
            
            # Loop through every pixel and print it.
            for x in range(rsz_x):
                for y in range(rsz_y):
                    # Skip any pixel with an grayscale value of 0.
                    a = out.getpixel((x,y))
                    
                    if a == 0:
                        continue
           
                    color = rgba(r, g, b, int(a))
           
                    pf.set(
                        int(offset_x+x) % width, 
                        int(offset_y+y) % height, 
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
    #pf = PixelFlut(('localhost', 1337))
    pf = PixelFlut(('entry.athon.uk', 1337))

    if len(sys.argv) < 2:
        exit()
    
    # Call a function in `samples` by the name we provide.
    samples.get(
        sys.argv[1],
        lambda _: print('unknown function')
    )(pf)
