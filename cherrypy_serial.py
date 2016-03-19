import cherrypy
cherrypy.server.ssl_module = 'builtin'
cherrypy.server.ssl_certificate = "cert.pem"
cherrypy.server.ssl_private_key = "privkey.pem"

import serial
ser = serial.Serial('/dev/tty.usbmodem1411',9600)

def multi_headers():
    cherrypy.response.header_list.extend(
        cherrypy.response.headers.encode_header_items(
            cherrypy.response.multiheaders))

cherrypy.tools.multiheaders = cherrypy.Tool('on_end_resource', multi_headers)

class CherryArduino(object):
    @cherrypy.expose
    @cherrypy.tools.multiheaders()
    def index(self,value='Hello'):
        cherrypy.response.multiheaders = [('Access-Control-Allow-Origin', '*')]
        ser.write(str(value))
        return value

if __name__ == '__main__':
    cherrypy.quickstart(CherryArduino())
