import numpy as np


class Analyzer():

    def __init__(self):
        super(Analyzer, self).__init__()

    def run(self, LED_RGBs):
        raise NotImplementedError()


class MedianAnalyzer():

    def run(self, LED_RGBs):

        return { led: np.median(LED_RGBs[led], axis=0)  for led in LED_RGBs}


class MeanAnalyzer():

    def run(self, LED_RGBs):

        return { led: np.mean(LED_RGBs[led], axis=0)  for led in LED_RGBs}
