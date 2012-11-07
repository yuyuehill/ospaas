'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import commands

class  TestClinder(unittest.TestCase): 
    def _setUp(self):
        url = "http://hillopen:5000"
        user =  "admin"
        password = "admin_pass"
        params = '{"passwordCredentials":{"username":user,"password":password}}'
        headers= {"Content-Type":"application/json"}
        self.conn = httplib.HTTPConnection(url)
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
        response = self.conn.getresponse()
        data = response.read()
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        
        apitoken = dd['auth']['token']['id']
        print "You token is %s" % apitoken
    
    def test_keystone_validation(self):
        
        url = "http://hillopen:5000/v2.0/tokens"
        data = '{"passwordCredentials":{"username":"admin","password":"password"}}'
        
        command = "curl -d \'%s\' -H \"Content-Type: application/json\" %s "  % (data, url)
        print command        
        print commands.getoutput(command)
        
            
    def test_cinder_create_volume(self):
        abc = "hill"
        aa = '{"I am here" :abc}'  
        print   aa
        print " create volume"
        print "added from master"
        print "add a new line from master"