import time
import numpy as np
from led import LED
from reader import HTTPReader
from collector import VoronoiCollector
from analyzer import MedianAnalyzer, MeanAnalyzer
from controller import WS281xController
#from controller import MatplotlibController
#from viewer import MatplotlibViewer
from neopixel import Color, Adafruit_NeoPixel, ws


# LED and monitor configuration
# -----------------------------

# Physical screen dimensions in millimeters.
SCREEN_WIDTH = 505
SCREEN_HEIGHT = 290

# (Effective) screen resolution in pixels.
SCREEN_X_PIXELS = 64
SCREEN_Y_PIXELS = 36

# LED numbering and positioning.
LEDs = []

# Test: place LEDs
xx = np.linspace(0, SCREEN_WIDTH, 29)
yy = np.linspace(0, SCREEN_HEIGHT, 16)

# LED_positions = [(yy[0], x) for x in xx] + [(y, xx[-1]) for y in yy[1:-1]] + [(yy[-1], x) for x in xx] + [(y, xx[0]) for y in yy[1:-1]] +

LED_positions = [(yy[-1], x) for x in xx] + [(y, xx[-1]) for y in reversed(yy[1:-1])] + [(yy[0], x) for x in reversed(xx)] + [(y, xx[0]) for y in yy[1:-1]]


for i in range(len(LED_positions)):
        LEDs.append(LED(i, LED_positions[i][0], LED_positions[i][1], screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH))

# Configuration
# -------------

READER = HTTPReader
READER_PARAMS = {'address': 'http://192.168.1.177:8080',
                 'request_params': {'width': SCREEN_X_PIXELS, 'height': SCREEN_Y_PIXELS}}
COLLECTOR = VoronoiCollector
COLLECTOR_PARAMS = {'LEDs': LEDs, 'num_neighbors': 2,
                    'screen_x_pixels': SCREEN_X_PIXELS, 'screen_y_pixels': SCREEN_Y_PIXELS}
ANALYZER = MeanAnalyzer
ANALYZER_PARAMS = {}
CONTROLLER = WS281xController
CONTROLLER_PARAMS = {'LEDs': LEDs, 'WS281x_config': {
    'num': len(LEDs),
    'pin': 18,
    'freq_hz': 800000,
    'dma': 10,
    'brightness': 250,
    'invert': False,
    'channel': 0,
    'strip_type': ws.WS2811_STRIP_GRB
    }, 'update_mode': 'smooth'}

UPDATE_PAUSE = 0  # seconds

# Main loop
# ---------

def main():

    # Initialization.
    print("Initializing")
    reader = READER(**READER_PARAMS)
    collector = COLLECTOR(**COLLECTOR_PARAMS)
    analyzer = ANALYZER(**ANALYZER_PARAMS)
    controller = CONTROLLER(**CONTROLLER_PARAMS)
    print("Running. Ctrl+C to terminate.")
    while True:
        image = reader.read()
        LED_RGB_collection = collector.collect(image)
        LED_RGB = analyzer.analyze(LED_RGB_collection)
        controller.control(LED_RGB)
        time.sleep(UPDATE_PAUSE)

#def test_main():
#
#    SCREEN_HEIGHT = 290
#    SCREEN_WIDTH = 505
#
#    # Place LEDs
#    xx = np.linspace(0, SCREEN_WIDTH, 25)
#    yy = np.linspace(0, SCREEN_HEIGHT, 15)
#
#    LEDs = []
#    LED_positions = [(yy[0], x) for x in xx] + [(yy[-1], x) for x in xx] + [(y, xx[0]) for y in yy[1:-1]] + [(y, xx[-1]) for y in yy[1:-1]]
#
#    for i in range(len(LED_positions)):
#        LEDs.append(LED(i, LED_positions[i][0], LED_positions[i][1], screen_height=290, screen_width=505))
#
#    image_path = '/home/christos/AdaptiveBacklight/screenshot.bmp'
#
#    print("Initializing Voronoi segments.")
#    reader = VoronoiReader(image_path, LEDs, num_neighbors=2)
#    analyzer = MeanAnalyzer()
#    controller = MatplotlibController()
#    viewer = MatplotlibViewer(ylim=[SCREEN_HEIGHT+10, 0-10], xlim=[0-10,SCREEN_WIDTH+10])
#
#    print("Starting")
#    while True:
#        print("Screenshot")
#        call(["import", "-window", "root", "-resize", "640x360", "screenshot.bmp"])
#        print("Reading")
#        LED_RGBs = reader.run()
#        print("Analyzing")
#        LED_RGB = analyzer.run(LED_RGBs)
#        print("Controlling")
#        X, Y, C = controller.run(LED_RGB)
#        print("Viewing")
#        viewer.update(X, Y, C)


if __name__ == '__main__':

    main()
