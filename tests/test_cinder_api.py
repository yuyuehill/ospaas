'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest

class  TestClinder(unittest.TestCase): 
    def setUp(self):
        url = "hillopen:5000"
        user =  "admin"
        password = "passwo0rd"
        params = '{"passwordCredentials":{"username":user,"password":password}}'
        headers= {"Content-Type":"application/json"}
        self.conn = httplib.HTTPConnection(url)
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
        response = self.conn.getresponse()
        data = response.read()
        dd = json.loads(data)
        self.conn.close()
        apitoken = dd['auth']['token']['id']
        print "You token is %s" % apitoken
        
    def test_cinder_create_volume(self):
        
        print "I am here"    
        print "test again"
    