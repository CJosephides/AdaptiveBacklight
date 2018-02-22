import numpy as np


class Analyzer(object):

    def __init__(self):
        super(Analyzer, self).__init__()

    def analyze(self, LED_RGB_collection):
        raise NotImplementedError()


class MedianAnalyzer(Analyzer):

    def __init__(self):
        super(MedianAnalyzer, self).__init__()

    def analyze(self, LED_RGB_collection):

        return { led: np.median(LED_RGB_collection[led], axis=0)  for led in LED_RGB_collection}


class MeanAnalyzer(Analyzer):

    def __init__(self):
        super(MeanAnalyzer, self).__init__()

    def analyze(self, LED_RGB_collection):

        return { led: np.mean(LED_RGB_collection[led], axis=0)  for led in LED_RGB_collection}
