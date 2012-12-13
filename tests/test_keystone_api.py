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
   
    TIVX043 = {'url':'tivx043:5000', 'username':'t1' , 'password':'t1', 'tenant':'admin','token':'80dc9ef6caef43809c48b14a1bc60c40'}

    LOCAL = {'url':'localhost:5000', 'username':'test' , 'password':'test', 'tenant':'admin','token':'80dc9ef6caef43809c48b14a1bc60c40'}
   
    def setUp(self):
        
        self.env = self.TIVX043
        
    def _encrpty_token(self,json_str):    
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
    
    def testSimpleToken(self):
      
        params = '{"auth":{"passwordCredentials":{"username":\"%s\"},"tenantName":\"%s\"}}' %(self.env['username'],self.env['tenant'])
       
        simpletoken_json = json.dumps({'username':'test','expiration': (time.time() + 10000)* 1000})
        print 'simpletoken_json',simpletoken_json        
        
        simpletoken = self._encrpty_token(simpletoken_json)
        
        print 'simpletoken', simpletoken
        headers= {"Content-Type":"application/json" ,"SimpleToken": simpletoken}

        self.conn = httplib.HTTPConnection(self.env['url'])
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
       
        response = self.conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        