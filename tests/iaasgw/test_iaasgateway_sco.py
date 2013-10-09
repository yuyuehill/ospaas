'''
This will simulate the IWD calls

Created on 2013

@author: yuyue
'''
import unittest
import random
import json
import test_gw_base


class TestGWSCOFunctions(test_gw_base.TestIaasGatewayBase):



    def setUp(self):
        self.env =  self.RTP
        test_gw_base.TestIaasGatewayBase.setUp(self)


    def list_users(self):
        path="/users"
        result = self.call_keystone_api("GET",path,None) 
        return result
    
    def list_domains(self):
        path="/domains"
        result = self.call_keystone_api("GET",path,None)
        return result
        
    def list_flavors(self):
        path="/flavors/detail"
        result = self.call_nova_api("GET",path,None)
        return result;
    
    def show_hypervisor(self):
        path = "/os-hypervisors/1"
        result = self.call_nova_api("GET",path,None)
        return result;

    def tearDown(self):
        pass


    def testKeystone(self):
        ret=self.list_users()
        print "users %s " % ret
        ret=self.list_domains()
        print "domains %s " % ret
        
    def testnova(self):
        #r
        ret = self.list_flavors()
        print "flavor %s" % ret
        
        ret = self.show_hypervisor()
        print "hyperviosr %s " % ret
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGlancePost']
    unittest.main()