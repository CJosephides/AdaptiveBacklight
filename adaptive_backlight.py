import time
import os
import argparse
from subprocess import call
import numpy as np

from reader import VoronoiReader
from analyzer import MedianAnalyzer, MeanAnalyzer
from controller import MatplotlibController
from viewer import MatplotlibViewer

def parse_arguments():
    pass

def test_main():

    SCREEN_HEIGHT = 290
    SCREEN_WIDTH = 505

    # Place LEDs
    xx = np.linspace(0, SCREEN_WIDTH, 25)
    yy = np.linspace(0, SCREEN_HEIGHT, 15)

    LEDs = []
    # LED_positions = [(yy[0], x) for x in xx] + [(yy[-1], x) for x in xx] + [(y, xx[0]) for y in yy[1:-1]] + [(y, xx[-1]) for y in yy[1:-1]]

    # With offset, to compensate for widescreen monitors.
    LED_positions = [(yy[0], x) for x in xx] + [(yy[-1], x) for x in xx] + [(y, xx[0]+50) for y in yy[1:-1]] + [(y, xx[-1]-50) for y in yy[1:-1]]

    for i in range(len(LED_positions)):
        LEDs.append(LED(i, LED_positions[i][0], LED_positions[i][1], screen_height=290, screen_width=505))
    
    image_path = '/home/christos/AdaptiveBacklight/screenshot.bmp'

    print("Initializing Voronoi segments.")
    reader = VoronoiReader(image_path, LEDs)
    analyzer = MeanAnalyzer()
    controller = MatplotlibController()
    viewer = MatplotlibViewer(ylim=[SCREEN_HEIGHT+10, 0-10], xlim=[0-10,SCREEN_WIDTH+10])

    print("Starting")
    while True:
        print("Screenshot")
        call(["import", "-window", "root", "-resize", "640x360", "screenshot.bmp"])
        print("Reading")
        LED_RGBs = reader.run()
        print("Analyzing")
        LED_RGB = analyzer.run(LED_RGBs)
        print("Controlling")
        X, Y, C = controller.run(LED_RGB) 
        print("Viewing")
        viewer.update(X, Y, C)


class LED():

    def __init__(self, number, y, x, screen_height, screen_width):
        """

        Arguments
        ---------

        number: int
                The number of the LED in the strip.
                The first LED in the strip is 0, the second is 1, etc...

        y, x:  float
                LED vertical and horizontal position in millimeters.
                Origin is at the top-left corner of the monitor.

        screen_height, screen_width:    float
                                        Screen height and width in millimeters.
        """
        self.number = number
        self.y = y
        self.x = x
        self.screen_height = screen_height
        self.screen_width = screen_width

    @property
    def coordinates(self):
        return((self.y, self.x))

    def pixel_position(self, y_pixels, x_pixels):
        """
        Return the pixel coordinates corresponding to the LED in a screen with pixel_height vertical pixels and pixel_width horizontal pixels.
        """

        pixel_y = int(y_pixels * (self.y / self.screen_height))
        pixel_x = int(x_pixels * (self.x / self.screen_width))

        return (pixel_y, pixel_x)

if __name__ == '__main__':

    test_main()
