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
        params = json.dumps({'name': 'hill_test_image_%s' % random.randint(1, 10000) , 'tags':['hill'] , 'disk_format':'qcow2', 'container_format':'bare'})
        dd = self.call_glance_api('POST','/v2/images',params)
        image_id=dd["id"]
        print 'create image return %s' % dd
        #upload binary
        #image_file="/Users/yuyue/work/ova_images/cirros-0.3.0-x86_64-disk.img"
        #image_file="/home/hill/work/ova_images/cirros-0.3.0-x86_64-disk.img"
        image_file="/data/scp_images/2.2/rhel61basic-sda.qcow2"
       
        self.call_glance_api_put_file('/v2/images/%s/file' % image_id, image_file)
        
        return image_id
    
    def delete_image(self,image_id):
        
        dd = self.call_glance_api('DELETE','/v2/images/%s' % image_id,None)
        print 'delete image return %s' % dd
     
        
    def tearDown(self):
        pass


    def testGlace(self):
        self.list_images()
        
        id=self.create_image()
        self.delete_image(id)
        
        pass

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGlancePost']
    unittest.main()