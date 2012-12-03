'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import random
import test_os_base
import time



class  TestQuantum(test_os_base.TestOpenStackBase): 
 
    def setUp(self):
        
        self.env = self.LOCAL
        test_os_base.TestOpenStackBase.setUp(self)
        
 
    def _list_networks(self):
        params=json.dumps({})        
        dd=self._call_quantum_api('GET','/networks',params)
        self.assertTrue(dd.has_key("networks"),"failed to list networks")
       
        return dd['networks']
    
    def test_network_subnet(self):
        print self._list_networks()