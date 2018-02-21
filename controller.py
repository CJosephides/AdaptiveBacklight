import time
import sys
import signal
import numpy as np
from neopixel import Color, Adafruit_NeoPixel

class Controller():

    def __init__(self):
        super(Controller, self).__init__()

    def control(self, LED_RGB):
        raise NotImplementedError("Must implement control method.")


class MatplotlibController(Controller):

    def __init__(self):
        super(MatplotlibController, self).__init__()

    def scatter_arrays(self, LED_RGB):

        r_x = []
        r_y = []
        r_c = []
        for led in LED_RGB:
            r_x.append(led.x)
            r_y.append(led.y)
            r_c.append(LED_RGB[led]/256.)

        return np.array(r_x), np.array(r_y), np.array(r_c)

    def control(self, LED_RGB):

        return self.scatter_arrays(LED_RGB)


class WS281xController(Controller):

    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 100
    LED_INVERT = False
    LED_CHANNEL = 0
    LED_STRIP = ws.WS2811_STRIP_GRB

    def __init__(self, LEDs, WS2812_params):

        # Strip setup.
        self.LEDs = LEDs
        self.num_LEDs = len(self.LEDs)
        self.strip = Adafruit_NeoPixel(self.num_LEDs, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        strip.begin()

        # Signal setup.
        signal.signal(signal.SIGINT, self.signal_handler)

        super(WS281xController, self).__init__()

    def control(self, LED_RGB):
        for led in LED_RGB:
            strip.setPixelColor(led.number, Color(tuple(LED_RGB[led]))) 
            strip.show()

    def signal_handler(self, signal, frame):
        for led in LED_RGB:
            strip.setPixelColor(led.number, Color(0, 0, 0))
        sys.exit(0)



