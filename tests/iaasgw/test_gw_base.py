


'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import urlparse



class  TestIaasGatewayBase(unittest.TestCase): 
    
    TIVX013 = {'url':'http://tivx013:9973', 'username':'admin', 'password':'admin', 'tenant':'admin'}
    
   
    #get the service from keystone
    def setUp(self):
        self.conn = None     
        #get providers
        providers = json.loads(self.__do_get(self.env['url']+"/providers"))
        print providers
        
        #get the endpoints of keystone
        ksurl=providers["serviceCatalog"][0]["endpoints"][0]["publicURL"]
        print "ks url %s" % ksurl       
          
        body = '{"auth":{"passwordCredentials":{"username":\"%s\","password":\"%s\"},"tenantName":\"%s\"}}' %(self.env['username'],self.env['password'],self.env['tenant'])
                
        headers= {"Content-Type":"application/json"}
        
        
        catalog=json.loads(self.__do_post(ksurl+"/tokens", body, headers))

        print "service catalog is %s " % catalog        
        
        self.apitoken = catalog['access']['token']['id']
        
    
        self.tenant_id = catalog['access']['token']['tenant']['id']
        
        for service in catalog['access']['serviceCatalog']:
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
    
    def tearDown(self):
        if (self.conn != None):
             self.conn.close()
               
    def __do_post(self,url,body,header):
        urlobj=urlparse.urlparse(url)
        
        if (self.conn == None):
            conn = httplib.HTTPConnection(urlobj.netloc)
        
        conn.request("POST",urlobj.path, body, header)
        response = conn.getresponse()
        data = response.read()
        return data
    
    def __do_get(self,url):
        urlobj=urlparse.urlparse(url)
        if(self.conn == None ):
            print "create connection %s " % url 
            conn =  httplib.HTTPConnection(urlobj.netloc)
       
        conn.request("GET",urlobj.path)
        response = conn.getresponse()
        print "doGet %s response %s" %(urlobj.path,response.status)
        data = response.read()
        return data
    
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
            
        if api_conn :   
            api_conn.close()
        
        return dd
    
    def __call_api_put_file(self,endpoints,path,file_name):
        
        for endpoint in endpoints:
            public_url = endpoint["publicURL"]
            scheme, netloc, rootpath, query, frag = urlparse.urlsplit(public_url)
        
        print scheme,netloc,rootpath,query,frag  
        
        if netloc.split(':')[0] == 'localhost':
            netloc = self.env['url'].split(':')[0] + ":" + netloc.split(':')[1]
        
        api_conn =  httplib.HTTPConnection(netloc)
        headers = {"Content-Type":"application/octet-stream","x-auth-token":self.apitoken }
        print "headers",headers,"path", rootpath + path
        
        api_conn.request("PUT",rootpath + path, file(file_name),headers)
        
        response = api_conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        
        if data is None or data == "":
            dd = {}
        else:
            dd = json.loads(data)
            
        if api_conn :   
            api_conn.close()
        
        return dd
    
    def call_cinder_api(self,method,path,params):
        return self.__call_api(self.cinder_endpoints,method,path,params)
        
    
    def call_nova_api(self,method,path,params):
        return self.__call_api(self.nova_endpoints,method,path,params)
    
    def call_quantum_api(self,method,path,params):
        return self.__call_api(self.quantum_endpoints,method,path,params)

    def call_glance_api(self,method,path,params):
        return self.__call_api(self.glance_endpoints,method,path,params)
        
    def call_glance_api_put_file(self,path,data):
        return self.__call_api_put_file(self.glance_endpoints,path,data)
        
    def call_keystone_admin_api(self,method,path,params):
        return self.__call_api(self.keystone_endpoints,method,path,params,urltype='adminURL')    
    
    def call_keystone_api(self,method,path,params):
        return self.__call_api(self.keystone_endpoints,method,path,params)    
 
        