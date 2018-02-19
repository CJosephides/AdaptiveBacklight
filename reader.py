import numpy as np
from scipy.misc import imread


class Reader():

    def __init__(self, image_path):
        self.image_path = image_path
        self.y_pixels, self.x_pixels = self.get_screen_pixels()

    def read(self):
        return imread(self.image_path)

    def get_screen_pixels(self):
        return self.read().shape[0:2]

    def run(self):
        raise NotImplementedError()


class VoronoiReader(Reader):

    def __init__(self, image_path, LEDs):
        super(VoronoiReader, self).__init__(image_path)
        
        self.LEDs = LEDs
        self.num_LEDs = len(self.LEDs)
        self.LED_map = self.make_LED_map()
        self.nearest_LED_mask = self.make_LED_mask()

    def make_LED_map(self):

        return { i: LED for i, LED in enumerate(self.LEDs) }

    def make_LED_mask(self):
        """
        Returns an self.y_pixels X self.x_pixels numpy array. The number at each index is the nearest LED neighbor of the pixel at that index. 

        Note that the LED number follows the order of the LEDs in the self.LEDs list (*not* the actual numbers of the LED objects).
        """

        from scipy.spatial import KDTree

        # Construct a K-d tree with LED pixel positions adjusted to our image size.
        # NOTE KDTree takes pairs of (x,y) coordinates. We are storing pairs of (y,x) LED coordinates.
        # NOTE I don't think it matters, as long as we are consistent. I should refactor this.
        LED_pixel_positions = []
        for led in self.LEDs:
            y, x = led.pixel_position(self.y_pixels, self.x_pixels)            
            LED_pixel_positions.append((x, y))
        tree = KDTree(LED_pixel_positions)

        # Get nearest neighbor for each pixel. The indices follow the sequence in the self.LEDs list.
        # NOTE this is slow!
        _, nearest_led = tree.query([[x,y] for y in range(self.y_pixels) 
                                           for x in range(self.x_pixels)]) 

        nearest_led = nearest_led.reshape((self.y_pixels, self.x_pixels))

        return nearest_led

    def collect_LED_RGBs(self, image):

        return { self.LED_map[led_number]: image[self.nearest_LED_mask == led_number] for led_number in range(self.num_LEDs) }

    def run(self):

        image = self.read()
        return self.collect_LED_RGBs(image)
        

# def example():
# 
#    import numpy as np
#    from reader import VoronoiReader
#    from adaptive_backlight import LED
#
#    # In mm
#    SCREEN_HEIGHT = 290
#    SCREEN_WIDTH = 505
#
#    # Place LEDs
#    xx = np.linspace(0, SCREEN_WIDTH, 25)
#    yy = np.linspace(0, SCREEN_HEIGHT, 15)
#
#    LEDs = []
#    LED_positions = [(yy[0], x) for x in xx] + [(yy[-1], x) for x in xx] + [(y, xx[0]) for y in yy] + [(y, xx[-1]) for y in yy]
#
#    for i in range(len(LED_positions)):
#        LEDs.append(LED(i, LED_positions[i][0], LED_positions[i][1], screen_height=290, screen_width=505))
#
#    image_path = 'spectrum.bmp'
#
#    vr = VoronoiReader(image_path, LEDs)
#
#    LED_RGBs = vr.run()
#
#    # Plot
#    result = []
#    for led in LED_RGBs:
#        result.append([led.x, led.y, *np.median(LED_RGBs[led], axis=0)])
#    
#    result = np.array(result)
#    r_x = result[:,0]
#    r_y = result[:,1]
#    r_c = result[:,2:]/356.
# 
#     import matplotlib.pyplot as plt
# 
#     fig, axes = plt.subplots(2,2)
#     axes[0,0].imshow(vr.read())
#     axes[0,1].scatter(r_x, r_y, c=r_c)
#     axes[0,1].set_ylim(axes[0,1].get_ylim()[::-1])
#     axes[1,1].imshow(vr.nearest_LED_mask)
#     plt.show()
# 
#     
# 
# 
