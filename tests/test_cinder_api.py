'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import urlparse
import random

class  TestClinder(unittest.TestCase): 
    def setUp(self):
        url = "localhost:5000"
        user="admin"
        password = "passw0rd"
        params = '{"auth":{"passwordCredentials":{"username":\"%s\","password":\"%s\"},"tenantName":"admin"}}' %(user,password)
                
        
        headers= {"Content-Type":"application/json"}
        self.conn = httplib.HTTPConnection(url)
     
        self.conn.request("POST","/v2.0/tokens",params,headers)
       
        response = self.conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        
        self.apitoken = dd['access']['token']['id']
        
    
        self.tenant_id = dd['access']['token']['tenant']['id']
        
        for service in dd['access']['serviceCatalog']:
            if service['type'] == 'volume':
                print "cinder endpoints " , service['endpoints']
                self.cinder_endpoints= service['endpoints']
    
    def _call_cinder_api(self,method,path,params):
    
        for endpoint in self.cinder_endpoints:
            cinder_url = endpoint["publicURL"]
            scheme, netloc, rootpath, query, frag = urlparse.urlsplit(cinder_url)
        
        print netloc,path   
        
        cinder_conn =  httplib.HTTPConnection(netloc)
        headers = {"Content-Type":"application/json","x-auth-token":self.apitoken}
        
        cinder_conn.request(method,rootpath + path, headers)
        response = self.conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        dd = json.loads(data)
        self.conn.close()
        
        return dd
    
    def test_cinder_list_volumes(self):
        params=json.dumps({})        
        dd=self._call_cinder_api("GET","/volumes",params)
        
        print dd
                 
    def test_cinder_create_volume(self):
        
        
        params = json.dumps({"volume": {"display_name": "hill_{0}".format(random.randint(1,10000)),"display_description": "hill test volume","size": 1}})
                   
        
        
        
        