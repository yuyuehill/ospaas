'''
Created on Oct 28, 2012

@author: hill
'''

import json
import re
import random
import test_os_base
import time

class  TestGlance(test_os_base.TestOpenStackBase): 
   
    def setUp(self):
        
        self.env = self.TIVX013
        test_os_base.TestOpenStackBase.setUp(self)
        
    
    def _index_images(self):
        
        dd=self._call_glance_api('GET','/v1/images?limit=999',None)
       
        return dd
    
    def _create_image(self, num = 30):
        
        for i in range(num):
            params = json.dumps({'name': 'hill_test_image_%s' % random.randint(1, 10000) , 'tags':['hill']})
            dd = self._call_glance_api('POST','/v2/images',params)
            print 'create image return %s' % dd
        
        return dd
    
    def test_images(self):
        
        #dd = self._create_image(10);
        print len(self._index_images()['images'])
        
        