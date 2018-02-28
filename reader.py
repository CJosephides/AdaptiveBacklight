import requests
from io import BytesIO
from scipy.misc import imread


class Reader(object):

    def __init__(self):
        super(Reader, self).__init__()

    def read(self):
        raise NotImplementedError('Must implement read method.')


class FileReader(Reader):

    def __init__(self, image_path):
        self.image_path = image_path
        super(FileReader, self).__init__()

    def read(self):
        image = imread(self.image_path)
        return image


class HTTPReader(Reader):

    def __init__(self, address, request_params):
        self.address = address
        self.request_params = request_params
        self.session = requests.Session()
        super(HTTPReader, self).__init__()

    def read(self):
        response = self.session.get(self.address, params=self.request_params)
        imageData = BytesIO(response.content)
        image = imread(imageData)
        return image


class StaticColorReader(Reader):

    def __init__(self, rgbColor):
        self.rgbColor = rgbColor
        super(StaticColorReader, self).__init__()

    def read(self):
        return list(self.rgbColor)

