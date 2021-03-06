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

    # TODO we should be able to define a smooth transition time and calculate these
    SMOOTH_UPDATE_PAUSE = 0  # milliseconds
    SMOOTH_UPDATE_ITERATIONS = 20

    def __init__(self, LEDs, WS281x_config, update_mode='step'):

        # Strip setup.
        self.LEDs = LEDs
        self.num_LEDs = len(self.LEDs)
        self.strip = Adafruit_NeoPixel(**WS281x_config)
        self.strip.begin()
        self.update = self.set_mode(update_mode)

        # Signal setup.
        signal.signal(signal.SIGINT, self.signal_handler)

        super(WS281xController, self).__init__()

    def set_mode(self, mode):
        if mode == 'step':
            return self.step
        elif mode == 'smooth':
            return self.smooth

    def control(self, LED_RGB):
        self.update(LED_RGB)

    def step(self, LED_RGB):
        for led in LED_RGB:
            self.strip.setPixelColor(led.number,
                                     self.make_color(LED_RGB[led][0], LED_RGB[led][1], LED_RGB[led][2]))
        self.strip.show()

    def smooth(self, LED_RGB):

        # Get increments for each LED's channels.
        LED_increments = { led: [0, 0, 0] for led in LED_RGB }
        for led in LED_RGB:
            LED_increments[led][0] = float(( LED_RGB[led][0] - led.red   )) / self.SMOOTH_UPDATE_ITERATIONS
            LED_increments[led][1] = float(( LED_RGB[led][1] - led.green )) / self.SMOOTH_UPDATE_ITERATIONS
            LED_increments[led][2] = float(( LED_RGB[led][2] - led.blue  )) / self.SMOOTH_UPDATE_ITERATIONS

        # Do the smooth transition.
        for i in range(self.SMOOTH_UPDATE_ITERATIONS):
            for led in LED_RGB:
                # TODO could turn the color updates into a method
                led.red += LED_increments[led][0]
                led.green += LED_increments[led][1]
                led.blue += LED_increments[led][2]
                color = self.make_color(led.red, led.green, led.blue)

                self.strip.setPixelColor(led.number, color)

            self.strip.show()
            time.sleep(self.SMOOTH_UPDATE_PAUSE / 1000.)

    def get_color_int(self, color):
        if np.isnan(color):
            return 0
        else:
            return int(max(0, color))

    def make_color(self, red, green, blue):
        return Color(self.get_color_int(red), self.get_color_int(green), self.get_color_int(blue))

    def signal_handler(self, signal, frame):
        for led in self.LEDs:
            self.strip.setPixelColor(led.number, Color(0, 0, 0))
        self.strip.show()
        sys.exit(0)

