


'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import urlparse


class  TestOpenStackBase(unittest.TestCase): 
    
    #get the service from keystone
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
                self.cinder_endpoints = service['endpoints']
            elif service['type'] == 'compute':
                print "compute endpoints", service['endpoints'] 
                self.nova_endpoints = service['endpoints']
            elif service['type'] == 'image':
                print "image endpoints",service['endpoints']
                self.glance_endpoints = service['endpoints'] 
            elif service['type'] == 'network':
                print 'network endpoints', service['endpoints']
                self.quantum_endpoints = service['endpoints']
    
    
    def _call_api(self,endpoints,method,path,params):
        
        for endpoint in endpoints:
            public_url = endpoint["publicURL"]
            scheme, netloc, rootpath, query, frag = urlparse.urlsplit(public_url)
        
        print scheme,netloc,rootpath,query,frag   
        
        api_conn =  httplib.HTTPConnection(netloc)
        headers = {"Content-Type":"application/json","x-auth-token":self.apitoken}
        print "headers",headers,"method",method,"path", rootpath + path, "params", params
        api_conn.request(method,rootpath + path, params, headers)
        
        response = api_conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        
        if data is None or data == "":
            dd = {}
        else:
            dd = json.loads(data)
            
        self.conn.close()
        
        return dd
    def _call_cinder_api(self,method,path,params):
        return self._call_api(self.cinder_endpoints,method,path,params)
        
    
    def _call_nova_api(self,method,path,params):
        return self._call_api(self.nova_endpoints,method,path,params)
        
        