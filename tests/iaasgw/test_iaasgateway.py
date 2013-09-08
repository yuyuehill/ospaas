'''
Created on 2013

@author: yuyue
'''
import unittest
import test_gw_base


class TestGWFunctions(test_gw_base.TestIaasGatewayBase):



    def setUp(self):
        self.env =  self.TIVX013
        test_gw_base.TestIaasGatewayBase.setUp(self)


    def tearDown(self):
        pass

    def token_get(self):
        pass

    def testGlacePost(self):
        pass

    def testServiceCatology(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGlancePost']
    unittest.main()