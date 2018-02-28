import numpy as np
from scipy.spatial import KDTree


class Collector(object):

    # TODO Collector should accept LEDs argument, since we need it everywhere.
    def __init__(self, screen_y_pixels, screen_x_pixels):
        self.screen_y_pixels = screen_y_pixels
        self.screen_x_pixels = screen_x_pixels

    def collect(self, image):
        raise NotImplementedError()


class StaticCollector(Collector):

    def __init__(self, LEDs):
        self.LEDs = LEDs

    def collect(self, image):
        return { led: np.array(image).reshape(1,3) for led in self.LEDs }


class VoronoiCollector(Collector):

    def __init__(self, LEDs, screen_y_pixels, screen_x_pixels, num_neighbors=1):

        super(VoronoiCollector, self).__init__(screen_y_pixels, screen_x_pixels)

        self.LEDs = LEDs
        self.num_LEDs = len(self.LEDs)
        self.LED_map = self.make_LED_map()
        self.num_neighbors = num_neighbors
        self.nearest_LED_mask = self.make_LED_mask()

    def make_LED_map(self):

        return { i: LED for i, LED in enumerate(self.LEDs) }

    def make_LED_mask(self):
        """
        Returns a (screen_y_pixels, screen_x_pixels, num_neighbrs) numpy array.
        The number at each index is the nearest LED neighbor of the pixel at that index.

        Note that the LED number follows the order of the LEDs in the self.LEDs list (*not* the actual numbers of the LED objects).
        """

        # Construct a K-d tree with LED pixel positions adjusted to our image size.
        LED_pixel_positions = []
        for led in self.LEDs:
            y, x = led.pixel_position(self.screen_y_pixels, self.screen_x_pixels)
            LED_pixel_positions.append((y, x))
        tree = KDTree(LED_pixel_positions)

        # Get nearest neighbor for each pixel. The indices follow the sequence in the self.LEDs list.
        # NOTE this is slow!
        _, nearest_led = tree.query([[y,x] for y in range(self.screen_y_pixels)
                                           for x in range(self.screen_x_pixels)],
                                           k=self.num_neighbors)

        nearest_led = nearest_led.reshape((self.screen_y_pixels, self.screen_x_pixels, self.num_neighbors))

        return nearest_led

    def collect_LED_RGBs(self, image):

        return { self.LED_map[led_number]: np.vstack([image[self.nearest_LED_mask[:,:,n] == led_number] for n in range(self.num_neighbors)]) for led_number in range(self.num_LEDs) }

    def collect(self, image):

        return self.collect_LED_RGBs(image)
