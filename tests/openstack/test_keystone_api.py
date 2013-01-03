'''
Created on Oct 28, 2012

@author: hill
'''

import json
import re
import random
from tests.openstack import test_os_base
import time
import httplib
import datetime
from Crypto.Cipher import AES
import base64



class  TestKeyStone(test_os_base.TestOpenStackBase): 
   

   
    def setUp(self):
        
        self.env = self.LOCAL
        test_os_base.TestOpenStackBase.setUp(self)
    
    def create_service(self):
        params = json.dumps({'OS-KSADM:service':{'name':'mytest_ec2_%d' %random.randint(1000, 2000), 'type':'ec2'}})
        dd = self.call_keystone_admin_api('POST','/OS-KSADM/services',params)
        print 'create service return  %s' % dd
        return dd 
    
    def delete_service(self, id):
        
        params = None
        dd = self.call_keystone_admin_api('DELETE','/OS-KSADM/services/%s' % id, params)
        print 'delete  service return  %s' % dd
    
    
    def list_service(self):
        params = None
        dd = self.call_keystone_admin_api('GET','/OS-KSADM/services',params)
        print 'get service return  %s' % dd
        return dd
    
    def list_endpoints(self):
        params = None
        dd = self.call_keystone_admin_api('GET','/endpoints',params)
        print 'get endpoints return  %s' % dd
        
        return dd
       
    def encrpty_token(self,json_str):    
        secret = "EzzNhXb17ZsOu9j18Ek7jg=="
        iv = '\0' * 16
        secret_key = base64.b64decode(secret)
        bs=16
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs) 
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        simple_token=base64.b64encode(cipher.encrypt(pad(json_str)))
        print 'u+L/C6VjWSLqv4UmpggxsERzU85d/L9GPXzhHkBKMzSzFKUNfh3zn4HrPRyPobdgFv6qJiKH8xQ57wztZq/8TA=='
        return simple_token
    
    def testSimpleToken(self):
      
        params = '{"auth":{"passwordCredentials":{"username":\"%s\"},"tenantName":\"%s\"}}' %(self.env['username'],self.env['tenant'])
       
        simpletoken_json = '{"username":"admin","expiration":  %d }' % ((time.time() + 10000)* 1000)
        #simpletoken_json = '{"username":"test", "expiration":"1355854311344.885"}'
        
        print 'simpletoken_json',simpletoken_json        
        
        simpletoken = self.encrpty_token(simpletoken_json)
        
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
        
        
        dd = self.list_service()
        print dd
        
        dd = self.create_service()      
        
    
        service_id = dd['OS-KSADM:service']['id']
        
        dd = self.delete_service(service_id)
        
        print dd
        
        dd = self.list_service()
        print dd
        
        