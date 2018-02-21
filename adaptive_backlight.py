import time
from led import LED
from collector import VoronoiCollector
from analyzer import MedianAnalyzer, MeanAnalyzer
from controller import MatplotlibController
from viewer import MatplotlibViewer
from neopixel import Color, Adafruit_NeoPixel


# LED and monitor configuration
# -----------------------------

# Physical screen dimensions in millimeters.
SCREEN_WIDTH = 505
SCREEN_HEIGHT = 290

# LED numbering and positioning.
LEDs = []

# test
LED_positions = [(yy[0], x) for x in xx] + [(yy[-1], x) for x in xx] + [(y, xx[0]) for y in yy[1:-1]] + [(y, xx[-1]) for y in yy[1:-1]]

for i in range(len(LED_positions)):
        LEDs.append(LED(i, LED_positions[i][0], LED_positions[i][1], screen_height=290, screen_width=505))

# Configuration
# -------------

READER = HTTPReader
READER_PARAMS = {'address': 'http://192.168.1.177:8080?width=640&height=360'}
COLLECTOR = VoronoiCollector
COLLECTOR_PARAMS = {'LEDs': LEDs, 'num_neighbors': 2}
ANALYZER = MeanAnalyzer
ANALYZER_PARAMS = {}
CONTROLLER = WS281xController
CONTROLLER_PARAMS = {'LEDs': LEDs, 'WS281_config': {
    'LED_COUNT': len(LEDs),
    'LED_PIN' : 18,
    'LED_FREQ_HZ' : 800000,
    'LED_DMA' : 10,
    'LED_BRIGHTNESS' : 100,
    'LED_INVERT' : False,
    'LED_CHANNEL' : 0,
    'LED_STRIP' : ws.WS2811_STRIP_GRB
    }}

UPDATE_PAUSE = 1  # seconds

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
