'''
Created on Dec 2, 2012

@author: hill
'''

import unittest

import httplib2
import os
import ssl

ROOTDIR = os.path.dirname(os.path.abspath(os.curdir))

KEY =  os.path.join(ROOTDIR,"../examples/ssl/private/keystonekey.pem")
CAERT = os.path.join(ROOTDIR,"../examples/ssl/certs/keystone.pem")
CA = os.path.join(ROOTDIR,"../examples/ssl/certs/ca.pem")
print KEY

class TestHttpLib2(unittest.TestCase):

   
    
    def test_https_oneway(self):
      
        uri = "https://tivx013:5000/"
        h = httplib2.Http()
        h.disable_ssl_certificate_validation = True
        resp, content = h.request(uri=uri)
        print resp,content
    
    #this is also be used by keystone client
        
    def test_https_twoway(self):
        uri = "https://tivx013:5000/"
        h = httplib2.Http(ca_certs=CA)
        h.add_certificate(key=KEY, cert=CAERT, domain='')
        resp, content = h.request(uri=uri)
        
        self.assertEqual(resp.status, 300)
        print resp,content
        print 'two way ssl successfully'
 
if __name__ == 'main':
    unittest.main()              