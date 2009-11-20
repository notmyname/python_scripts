#!/usr/bin/env python

import OpenSSL
import socket
import time

file_path = 'simple/client.cert'
cert_data = open(file_path,'rb').read()
x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
print x.get_issuer().CN # is "Certificate Authority"
print x.get_subject().CN # is "Simple Client"
print x.subject_name_hash()

print

file_path = 'simple/CA.cert'
CA_data = open(file_path,'rb').read()
y = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, CA_data)
print y.get_issuer().CN # is "Certificate Authority"
print y.get_subject().CN # is "Certificate Authority

print

file_path = 'simple/server.cert'
cert_data = open(file_path,'rb').read()
z = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
print z.get_issuer().CN # is "Certificate Authority"
print z.get_subject().CN # is "Simple Server"

print

file_path = 'simple/CA.pkey'
CA_pkey_data = open(file_path,'rb').read()
CA_pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, CA_pkey_data)
print CA_pkey
print CA_pkey.bits()

print

def verify(connection, x509, errnum, errdepth, ok):
    print '_verify (ok=%d):' % ok
    print '  subject:', x509.get_subject()
    print '  issuer:', x509.get_issuer()
    print '  errnum %s, errdepth %d' % (errnum, errdepth)
    return ok

# create the context
ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
ctx.use_certificate_file('simple/client.cert')
ctx.use_privatekey_file('simple/client.pkey')
ctx.load_verify_locations('simple/CA.cert')
ctx.set_verify(OpenSSL.SSL.VERIFY_PEER|OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT,verify) # just means we want to verify the server too (requires that we have the certificate chain root available--CA.cert)
# create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',5000))
# tie the socket and context together in a connection
conn = OpenSSL.SSL.Connection(ctx, sock)
conn.set_connect_state()
conn.do_handshake()
#conn.setblocking(False)
print 'pending data length:',conn.pending()
print 'state:',conn.state_string()
print 'peer certificate:',conn.get_peer_certificate() # who are we talking to?
print "Sever response:"
conn.send("HEAD / HTTP/1.0\n\n")
#conn.setblocking(False)
while True:#conn.want_read():
    try:
        buff = conn.recv(4096) # why does this error out? why don't we have any data to read?
    except OpenSSL.SSL.ZeroReturnError:
        # we're done
        break
    except OpenSSL.SSL.WantReadError:
        pass
