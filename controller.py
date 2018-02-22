import time
import sys
import signal
import numpy as np
from neopixel import Color, Adafruit_NeoPixel, ws

class Controller(object):

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

    def __init__(self, LEDs, WS281x_config):

        # Strip setup.
        self.LEDs = LEDs
        self.num_LEDs = len(self.LEDs)
        self.strip = Adafruit_NeoPixel(**WS281x_config)
        self.strip.begin()

        # Signal setup.
        signal.signal(signal.SIGINT, self.signal_handler)

        super(WS281xController, self).__init__()

    def control(self, LED_RGB):
        for led in LED_RGB:
            red = self.get_color_int(LED_RGB[led][0])
            green = self.get_color_int(LED_RGB[led][1])
            blue = self.get_color_int(LED_RGB[led][2])
            self.strip.setPixelColor(led.number, Color(red, green, blue))
        self.strip.show()

    @staticmethod
    def get_color_int(color):
        if np.isnan(color):
            return 0
        else:
            return int(color)

    def signal_handler(self, signal, frame):
        for led in self.LEDs:
            self.strip.setPixelColor(led.number, Color(0, 0, 0))
        self.strip.show()
        sys.exit(0)



