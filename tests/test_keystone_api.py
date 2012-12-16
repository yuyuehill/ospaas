'''
Created on Oct 28, 2012

@author: hill
'''

import json
import re
import random
import test_os_base
import time
import httplib
import datetime
from Crypto.Cipher import AES
import base64



class  TestKeyStone(test_os_base.TestOpenStackBase): 
   

   
    def setUp(self):
        
        self.env = self.TIVX013
        test_os_base.TestOpenStackBase.setUp(self)
    
    def __create_service(self):
        params = json.dumps({'OS-KSADM:service':{'name':'mytest_ec2_%d' %random.randint(1000, 2000), 'type':'ec2'}})
        dd = self.__call_keystone_admin_api('POST','/OS-KSADM/services',params)
        print 'create service return  %s' % dd
        return dd 
    
    def __delete_service(self, id):
        
        params = None
        dd = self.__call_keystone_admin_api('DELETE','/OS-KSADM/services/%s' % id, params)
        print 'delete  service return  %s' % dd
    
    
    def __list_service(self):
        params = None
        dd = self.__call_keystone_admin_api('GET','/OS-KSADM/services',params)
        print 'get service return  %s' % dd
        return dd
    
    def __list_endpoints(self):
        params = None
        dd = self.__call_keystone_admin_api('GET','/endpoints',params)
        print 'get endpoints return  %s' % dd
        
        return dd
       
    def __encrpty_token(self,json_str):    
        secret = "EzzNhXb17ZsOu9j18Ek7jg=="
        _iv = '\0' * 16
        secret_key = base64.b64decode(secret)
        
              
        print 'secret_key', secret_key , "json_str" , json_str
        BLOCK_SIZE=16
        decryptor=AES.new(secret_key,AES.MODE_CBC,_iv)
        
        PADDING=u'\x0000'
        pad= lambda s: s +(BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
  
              
        padding_json=pad(json_str)
        print 'padding_json', padding_json
        
        encrpt_json= decryptor.encrypt(padding_json)
        print 'encrpty_json', encrpt_json
        
        simple_token=base64.b64encode(encrpt_json)
        
        return simple_token
    
    def __testSimpleToken(self):
      
        params = '{"auth":{"passwordCredentials":{"username":\"%s\"},"tenantName":\"%s\"}}' %(self.env['username'],self.env['tenant'])
       
        simpletoken_json = json.dumps({'username':'test','expiration': (time.time() + 10000)* 1000})
        print 'simpletoken_json',simpletoken_json        
        
        simpletoken = self.__encrpty_token(simpletoken_json)
        
        print 'simpletoken', simpletoken
        headers= {"Content-Type":"application/json" ,"SimpleToken": simpletoken}

        self.conn = httplib.HTTPConnection(self.env['url'])
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
       
        response = self.conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        
        
    def test_list_service_after_delete(self):
        
        
        dd = self.__list_service()
        print dd
        
        dd = self.__create_service()      
        
    
        service_id = dd['OS-KSADM:service']['id']
        
        dd = self.__delete_service(service_id)
        
        print dd
        
        dd = self.__list_service()
        print dd
        
        