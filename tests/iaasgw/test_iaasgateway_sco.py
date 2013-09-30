'''
This will simulate the IWD calls

Created on 2013

@author: yuyue
'''
import unittest
import random
import json
import test_gw_base


class TestGWSCOKeystoneFunctions(test_gw_base.TestIaasGatewayBase):



    def setUp(self):
        self.env =  self.TIVX013
        test_gw_base.TestIaasGatewayBase.setUp(self)


    def list_users(self):
        path="/users"
        result = self.call_keystone_api("GET",path,None) 
        return result
    
    def list_domains(self):
        path="/domains"
        result = self.call_keystone_api("GET",path,None)
        return result
        
    def tearDown(self):
        pass


    def testKeystone(self):
        ret=self.list_users()
        print "users %s " % ret
        ret=self.list_domains()
        print "domains %s " % ret
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGlancePost']
    unittest.main()