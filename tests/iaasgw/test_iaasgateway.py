'''
Created on 2013

@author: yuyue
'''
import unittest
import random
import json
import test_gw_base


class TestGWFunctions(test_gw_base.TestIaasGatewayBase):



    def setUp(self):
        self.env =  self.TIVX013
        test_gw_base.TestIaasGatewayBase.setUp(self)


    def list_images(self):
        path = "v2/images"
        result = self.call_glance_api("GET",path,None)

        print "list images %s " % result
        
    def create_image(self):
        params = json.dumps({'name': 'hill_test_image_%s' % random.randint(1, 10000) , 'tags':['hill']})
        dd = self.call_glance_api('POST','/v2/images',params)
        image_id=dd["id"]
        print 'create image return %s' % dd
        #upload binary
        image_file="/Users/yuyue/work/ova_images/cirros-0.3.0-x86_64-disk.img"
       
        self.call_glance_api_put_file('/v2/images/%s/file' % image_id, image_file)
        
    def tearDown(self):
        pass


    def testGlace(self):
        self.list_images()
        
        self.create_image()
        pass

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGlancePost']
    unittest.main()