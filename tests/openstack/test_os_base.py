


'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import urlparse



class  TestOpenStackBase(unittest.TestCase): 
    
    LOCAL = {'url':'localhost:5000', 'username':'admin', 'password':'passw0rd', 'tenant':'admin'}

    HILLOPEN = {'url':'hillopen:5000', 'username':'admin' , 'password':'admin_pass' , 'tenant':'admin'}
    
    HILLOS = {'url':'hillos:5000', 'username':'admin' , 'password':'passw0rd' , 'tenant':'admin'}

    TIVX043 = {'url':'tivx043:5000', 'username':'admin' , 'password':'admin' , 'tenant':'admin'}

    TIVX013 = {'url':'tivx013:5000', 'username':'admin' , 'password':'admin' , 'tenant':'admin'}
    
    GEMINI =  {'url':'9.115.78.63:5000'  , 'username' :'admin', 'password':'admin', 'tenant':'admin'}

    CLOUDOE =  {'url':'9.111.221.21:5000'  , 'username' :'admin', 'password':'admin', 'tenant':'admin'}
    
    #get the service from keystone
    def setUp(self):
        
          
        params = '{"auth":{"passwordCredentials":{"username":\"%s\","password":\"%s\"},"tenantName":\"%s\"}}' %(self.env['username'],self.env['password'],self.env['tenant'])
        print params
        
        headers= {"Content-Type":"application/json"}

        self.conn = httplib.HTTPConnection(self.env['url'])
     
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
            elif service['type'] == 'identity':
                print 'identify endpoints', service['endpoints']
                self.keystone_endpoints = service['endpoints']
    
    def __call_api(self,endpoints,method,path,params, urltype='publicURL' ):
        
        for endpoint in endpoints:
            public_url = endpoint[urltype]
            scheme, netloc, rootpath, query, frag = urlparse.urlsplit(public_url)
        
        print scheme,netloc,rootpath,query,frag  
        
        if netloc.split(':')[0] == 'localhost':
            netloc = self.env['url'].split(':')[0] + ":" + netloc.split(':')[1]
        
        api_conn =  httplib.HTTPConnection(netloc)
        headers = {"Content-Type":"application/json","x-auth-token":self.apitoken }
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
    
    
    def call_cinder_api(self,method,path,params):
        return self.__call_api(self.cinder_endpoints,method,path,params)
        
    
    def call_nova_api(self,method,path,params):
        return self.__call_api(self.nova_endpoints,method,path,params)
    
    def call_quantum_api(self,method,path,params):
        return self.__call_api(self.quantum_endpoints,method,path,params)

    def call_glance_api(self,method,path,params):
        return self.__call_api(self.glance_endpoints,method,path,params)
        
    def call_keystone_admin_api(self,method,path,params):
        return self.__call_api(self.keystone_endpoints,method,path,params,urltype='adminURL')    
    
    def call_keystone_api(self,method,path,params):
        return self.__call_api(self.keystone_endpoints,method,path,params)    
 
        