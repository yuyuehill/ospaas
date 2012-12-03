'''
Created on Dec 2, 2012

@author: hill
'''

import unittest

from keystoneclient import client

class ClientSSLTest(unittest.TestCase):

    TIVX043_SSL =  {"endpoint":"https://tivx043:5000", "user":"admin", "password":"admin", "tenant":"admin" ,
                    "cacert":"~/git/ospaas/examples/pki/certs/cacert.pem",
                    "key":"~/git/ospaas/examples/pki/private/ssl_key.pem",
                    "cert":"~/git/ospaas/examples/pki/certs/ssl_cert.pem"
                    }
    
    
    def _test_connect(self):
        
        localenv = self.TIVX043_SSL
        cl = client.HTTPClient(username=localenv["user"], password=localenv["password"],
                           tenant_id=localenv["tenant"], auth_url=localenv["endpoint"],
                           cacert=localenv["cacert"], key=localenv["key"], cert=localenv["cert"])
        
        cl.request(localenv["endpoint"]+"/tokens","GET")
    
    
    def test_ssl(self):
        import socket, ssl, pprint

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # require a certificate from the server
        ssl_sock = ssl.wrap_socket(s,
                           ca_certs="~/myca/test/cacert.pem",
                           cert_reqs=ssl.CERT_OPTIONAL)

        ssl_sock.connect(('tivx043', 5000))

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