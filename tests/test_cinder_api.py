'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import commands

class  TestClinder(unittest.TestCase): 
    def setUp(self):
        url = "hillopen:5000"
        user="admin"
        password = "admin_pass"
        params = '{"auth":{"passwordCredentials":{"username":\"%s\","password":\"%s\"}}}' %(user,password)
        
        
        
        headers= {"Content-Type":"application/json"}
        self.conn = httplib.HTTPConnection(url)
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
        response = self.conn.getresponse()
        data = response.read()
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        
        apitoken = dd['access']['token']['id']
        print "You token is %s" % apitoken
   
            
    def test_cinder_create_volume(self):
        abc = "hill"
        aa = '{"I am here" :abc}'  
        print   aa
        print " create volume"
        