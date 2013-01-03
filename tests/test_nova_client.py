'''
Created on Jan 2, 2013

@author: hill
'''


import unittest
from novaclient.v1_1 import client



''' this class is to test the nova client

'''
class TestNovaClient(unittest.TestCase):
    
    TIVX013 = {'url':'https://tivx013:5000', 'username':'admin', 'password':'passw0rd', 'tenant':'admin'}

    def setUp(self):
        self.env = self.TIVX013
        pass
    
    def test_nova_ssl(self):
        
        
        nt = client.Client(self.env['username'], self.env['password'],self.env['tenant'],self.env['url'],service_type='compute')
        
        nt.flavors.list()
        
                           
                                    
                                   