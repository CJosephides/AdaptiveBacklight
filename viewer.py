import numpy as np
import matplotlib.pyplot as plt

class Viewer(object):

    def __init__(self):
        pass


class MatplotlibViewer(Viewer):

    def __init__(self, ylim, xlim):

        plt.ion()

        self.xlim = xlim
        self.ylim = ylim

        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter([], [])
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        plt.draw()

        super(MatplotlibViewer, self).__init__()

    def update(self, X, Y, C):
        self.scatter.set_offsets(np.c_[X,Y])
        self.scatter.set_color(C)
        self.fig.canvas.draw_idle()
        plt.pause(0.1)





