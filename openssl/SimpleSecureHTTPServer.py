'''
SimpleSecureHTTPServer.py - simple HTTP server supporting SSL.

- replace fpem with the location of your .pem server file.
- the default port is 443.

usage: python SimpleSecureHTTPServer.py
'''
import socket
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL


class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.TLSv1_METHOD)
        ctx.use_privatekey_file ('simple/server.pkey')
        ctx.use_certificate_file('simple/server.cert')
        ctx.load_verify_locations('simple/CA.cert')
        ctx.set_options(SSL.OP_SINGLE_DH_USE | SSL.OP_NO_SSLv2)
        ctx.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT,self._verify)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,self.socket_type))
        self.server_bind()
        self.server_activate()
    
    def _verify(self, connection, x509, errnum, errdepth, ok):
        print '_verify (ok=%d):' % ok
        print '  subject:', x509.get_subject()
        print '  issuer:', x509.get_issuer()
        print '  errnum %s, errdepth %d' % (errnum, errdepth)
        return ok


class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
    
    def do_HEAD(self):
        print 'HEAD request received...'
        print self.requestline
        print '\twe are talking to',self.connection.get_peer_certificate().get_subject().CN # who is talking to us
        #self.send_header('foo','bar')
        self.end_headers()
        print '\theaders sent'
        self.send_response(200, 'hello world')
        #return SimpleHTTPRequestHandler.do_HEAD(self)


def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    server_address = ('localhost', 5000) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print "Serving HTTPS on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()


if __name__ == '__main__':
    test()
