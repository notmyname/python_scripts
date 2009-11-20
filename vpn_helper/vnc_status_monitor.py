#!/usr/bin/env python

import SocketServer
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

class VNCWatcher(SocketServer.ForkingTCPServer):
    allow_reuse_address = True

class VNCWatcherHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        ctx.use_certificate_file('/home/john/python_scripts/openssl/simple/server.cert')
        ctx.use_privatekey_file('/home/john/python_scripts/openssl/simple/server.pkey')
        ctx.load_verify_locations('/home/john/python_scripts/openssl/simple/CA.cert')
        ctx.set_verify(OpenSSL.SSL.VERIFY_PEER|OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT,verify) # just means we want to verify the server too (requires that we have the certificate chain root available--CA.cert)
        
        # tie the socket and context together in a connection
        conn = OpenSSL.SSL.Connection(ctx, self.request)
        conn.set_connect_state()
        
        version = conn.recv(RECV_BUFFER) # get version
        
        # only support version 1.0 for now
        if version == '1.0':
            client_cert = conn.get_peer_certificate() # who are we talking to?
            client_name = client_cert.get_subject().CN
            print 'connection from version %s client: %s' % (version, client_name)
            
            # now find the running vncserver on parker
            #look for Xvnc running on parker
            ps_results = res = subprocess.Popen('ps -ef | grep Xrealvnc | grep "%s" | grep -v grep' % client_name, stdout=subprocess.PIPE, shell=True).stdout.readlines()
            if ps_results:
                server = ps_results[0].split('Xrealvnc')[-1].strip().split(' ')[0]
                print server
            else:
                # if no server is running, create one
                p = subprocess.Popen('vncserver -geometry 1024x768', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # start it
                out = p.stderr.read()
                # can we create a password from the SSL certificate?
                print 'creating new vncserver instance'
                hostname = SocketServer.socket.gethostname()
                display = out.split('desktop is ')[1].split()[0].strip().split(':')[1]
                server = '%s:%s' % (hostname,display)
            
            # send back the running vncserver info (for example: parker:8)
        
            conn.sendall(server) # send results back

if __name__ == '__main__':
    where = ('127.0.0.1',5000)
    s = VNCWatcher(where, VNCWatcherHandler)
    s.serve_forever()
