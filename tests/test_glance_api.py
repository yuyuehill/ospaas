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
        
        self.env = self.LOCAL
        test_os_base.TestOpenStackBase.setUp(self)
        
    
    def _index_images(self):
            
        dd=self._call_glance_api('GET','/images',None)
       
        return dd
    
    def test_images(self):
        
        
        print self._index_images()
        
        