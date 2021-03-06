'''
Created on Dec 2, 2012

@author: hill
'''

import unittest

import httplib
import os
import ssl




from keystoneclient.v2_0 import client


ROOTDIR = os.path.dirname(os.path.abspath(os.curdir))

CERTDIR = os.path.join(ROOTDIR,"examples/pki/certs")
KEYDIR = os.path.join(ROOTDIR,"examples/pki/private")
CERT = os.path.join(CERTDIR, 'ssl_cert.pem')
KEY = os.path.join(KEYDIR, 'ssl_key.pem')
CA = os.path.join(CERTDIR, 'cacert.pem')
CLIENT = os.path.join(CERTDIR, 'middleware.pem')

CACLIENT= os.path.join(ROOTDIR,"examples/pki/certs/middleware.pem")


class ClientSSLTest(unittest.TestCase):

    TIVX043_SSL =  {"endpoint":"https://tivx043:5000", "user":"admin", "password":"admin", "tenant":"admin" ,
                    "cacert":"~/git/ospaas/examples/pki/certs/cacert.pem",
                    "key":"~/git/ospaas/examples/pki/certs/middleware.pem",
                    "cert":"~/git/ospaas/examples/pki/certs/middleware.pem"
                    }
    
    LOCAL_SSL =  {"endpoint":"https://localhost:5000/v2.0", "user":"admin", "password":"passw0rd", "tenant":"admin" ,
                    "cacert":CA,
                    "key":CACLIENT,
                    "cert":CACLIENT
                    }
   
    def __test_connect(self):
        
        localenv = self.TIVX043_SSL
        
        keystone = client.Client(username=localenv["user"], password=localenv["password"],
                           tenant_name=localenv["tenant"], auth_url=localenv["endpoint"],
                           cacert=localenv["cacert"], key=localenv["key"], cert=localenv["cert"],debug=True)
        
        
        print keystone.tenants.list()
        
    
    def test_https(self):
      
        host="tivx013"
         # Verify Admin
        conn = httplib.HTTPSConnection(host, '35357')
        conn.request('GET', '/')
        resp = conn.getresponse()
        self.assertEqual(resp.status, 300)
        print "verify %s admin port ssl single way successful" % host 
        # Verify Public
        conn = httplib.HTTPSConnection(host, '5000')
        conn.request('GET', '/')
        resp = conn.getresponse()
        self.assertEqual(resp.status, 300)
        print "verify %s public port ssl single way successful" % host 
        
        print 'hill',CACLIENT
        
         # Verify Admin
        conn = httplib.HTTPSConnection(
            host, '35357', CACLIENT, CACLIENT)
        conn.request('GET', '/')
        resp = conn.getresponse()
        self.assertEqual(resp.status, 300)
        
        print "verify %s admin port ssl dual way successful" % host 
        # Verify Public
        conn = httplib.HTTPSConnection(
            host, '5000', CACLIENT, CACLIENT)
        conn.request('GET', '/')
        resp = conn.getresponse()
        self.assertEqual(resp.status, 300)
        print "verify %s public port ssl dual way successful" % host 
        
    
    def __test_ssl(self):
        import socket, ssl, pprint

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # require a certificate from the server
        ssl_sock = ssl.wrap_socket(s,
                           ca_certs=CA,
                           cert_reqs=ssl.CERT_OPTIONAL)

        ssl_sock.connect(('localhost', 5000))

        print repr(ssl_sock.getpeername())
        print ssl_sock.cipher()
        print pprint.pformat(ssl_sock.getpeercert())

        # Set a simple HTTP request -- use httplib in actual code.
        ssl_sock.write("""GET / HTTP/1.0\r
                                Host: tivx043\r\n\r\n""")

        # Read a chunk of data.  Will not necessarily
        # read all the data returned by the server.
        data = ssl_sock.read()

        # note that closing the SSLSocket will also close the underlying socket
        ssl_sock.close()