'''
Created on Dec 10, 2012

This is for those failed cases for regression or due to different deployment and configuration 
for general openstack

@author: hill
'''
import unittest
import json
import test_os_base
import test_nova_api


class  TestRegression(test_nova_api.TestNova): 


    def setUp(self):
        
        self.env = self.TIVX013
        test_os_base.TestOpenStackBase.setUp(self)
    
          
    def test_network_list(self):
        dd = self._list_networks()
        print dd
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
