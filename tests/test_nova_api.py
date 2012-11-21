'''
Created on Oct 28, 2012

@author: hill
'''

import json

import test_os_base

class  TestNova(test_os_base.TestOpenStackBase): 
   
    def _list_extends(self):
        params=json.dumps({})        
        dd=self._call_nova_api('GET','/extensions',params)
       
        print dd
        
    def test_extneds(self):
        dd = self._list_extends()    
        for extension in dd['extendsions']:
            print "name",extension["name"]