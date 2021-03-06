class LED():

    def __init__(self, number, y, x, screen_height, screen_width, red=0, green=0, blue=0):
        """

        Arguments
        ---------

        number: int
                The number of the LED in the strip.
                The first LED in the strip is 0, the second is 1, etc...

        y, x:  float
                LED vertical and horizontal position in millimeters.
                Origin is at the top-left corner of the monitor.

        red, green, blue:   int
                            An optional attribute to store the color state of the LED.

        screen_height, screen_width:    float
                                        Screen height and width in millimeters.
        """
        self.number = number
        self.y = y
        self.x = x
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.red = red
        self.green = green
        self.blue = blue

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

    @property
    def color(self):
        return (self.red, self.green, self.blue)
