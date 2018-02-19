import numpy as np

class Controller():
    pass


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

    def run(self, LED_RGB):

        return self.scatter_arrays(LED_RGB)





