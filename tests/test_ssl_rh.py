'''
Created on Dec 2, 2012

@author: hill
'''

import unittest

import httplib
import os
import ssl
import tests

from keystoneclient.v2_0 import client


ROOTDIR = os.path.dirname(os.path.abspath(os.curdir))

CERTDIR = os.path.join(ROOTDIR,"examples/ssl/certs")
KEYDIR = os.path.join(ROOTDIR,"examples/ssl/private")
CERT = os.path.join(CERTDIR, 'keystone.pem')
KEY = os.path.join(KEYDIR, 'keystonekey.pem')
CA = os.path.join(CERTDIR, 'ca.pem')
CLIENT = os.path.join(CERTDIR, 'middleware.pem')

CACLIENT= os.path.join(ROOTDIR,"examples/ssl/certs/middleware.pem")


class ClientSSLTest(unittest.TestCase):

    TIVX043_SSL =  {"host":"tivx043","endpoint":"https://tivx043:5000", "user":"admin", "password":"admin", "tenant":"admin" ,
                    "cacert":CA,
                    "key":KEY,
                    "cert":CERT
                    }
    
    TIVX013_SSL =  {"host":"tivx013","endpoint":"https://tivx013:5000", "user":"admin", "password":"admin", "tenant":"admin" ,
                    "cacert":CA,
                    "key":KEY,
                    "cert":CERT
                    }
    def setUp(self):
        self.localenv=self.TIVX013_SSL
    
    def test_connect(self):
        
        keystone = client.Client(username=self.localenv["user"], password=self.localenv["password"],
                           tenant_name=self.localenv["tenant"], auth_url=self.localenv["endpoint"],
                           cacert=self.localenv["cacert"], key=self.localenv["key"], cert=self.localenv["cert"],debug=True)
        
        
        print keystone.tenants.list()
        
    def __test_https_one_way(self):
        
        host=self.localenv["host"]
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
    
    def __test_https_two_way(self):
        
        host=self.localenv["host"]
        
         # Verify Admin
        conn = httplib.HTTPSConnection(
            host, '35357', CACLIENT,CACLIENT)
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