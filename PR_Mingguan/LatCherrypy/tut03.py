import random
import string
import cherrypy
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.config.update({'server.socket_port': 15161})

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, \
                       int(length)))

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())

