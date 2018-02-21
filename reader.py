import urllib
from io import BytesIO
from scipy.misc import imread


class Reader():

    def __init__(self):
        super(Reader, self).__init__() 

    def read(self):
        raise NotImplementedError('Must implement read method.')


def FileReader(Reader):

    def __init__(self, image_path):
        self.image_path = image_path
        super(FileReader, self).__init__()

    def read(self):
        image = imread(self.image_path)
        return image


def HTTPReader(Reader):

    def __init__(self, address):
        self.address = address
        super(HTTPReader, self).__init__()

    def read(self):
        response = urllib.request(self.address)
        imageData = BytesIO(response.read())
        image = imread(imageData)
        return image
