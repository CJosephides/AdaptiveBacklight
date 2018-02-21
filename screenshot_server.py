import cherrypy
import subprocess


class ScreenGrabber():

    @cherrypy.expose
    def index(self, width=640, height=360):
        # Call subprocess.
        image = subprocess.run(['import', '-window', 'root', 
            '-resize', '{}x{}'.format(int(width), int(height)), 'bmp:-'],
                               stdout=subprocess.PIPE)
        # Return image.
        return image.stdout


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '192.168.1.177'})
    cherrypy.quickstart(ScreenGrabber())
