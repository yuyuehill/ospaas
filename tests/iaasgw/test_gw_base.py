


'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import unittest
import urlparse



class  TestIaasGatewayBase(unittest.TestCase): 
    
    TIVX013 = {'url':'http://tivx013:9973', 'username':'admin', 'password':'admin', 'tenant':'admin', 'domain':"Default","tenant_id":""}
    RTP = {'url':'http://172.17.43.49:9973', 'username':'admin', 'password':'passw0rd', 'tenant':'admin', 'domain':"Default","tenant_id":""}
    #get the service from keystone
    def setUp(self):
        self.conn = None     
        #get providers
        providers = json.loads(self.__do_get(self.env['url']+"/providers"))
        print "providers ===== %s " % providers
        ksendpoint=providers["serviceCatalog"][0]["endpoints"]
        print "endpoints ===== %s " % ksendpoint
        #get the endpoints of keystone
        for endpoint in  ksendpoint:
            if endpoint["interface"] == "public":
                ksurl= endpoint["url"]                     
            if endpoint["interface"] == "admin":
                ksadminurl=endpoint["url"]           
        
        print "ks url %s  ksadmin url %s " % (ksurl,ksadminurl)       
          
        body = self._get_auth_info_v3() 
                
        headers= {"Content-Type":"application/json"}
        
        users,headers=self.__do_post(ksurl+"/auth/tokens", body, headers)
        
        for header in headers:
            if header[0] == "x-subject-token":
               self.apitoken = header[1]
               
        #get the tokens
        print "get tokens %s  %s  token=%s " % (users,headers,self.apitoken )  
        
        services = self.__call_api(ksendpoint,"GET","/services",  None,"admin")
        print "====get services %s " % services
        endpoints = self.__call_api(ksendpoint,"GET","/endpoints",None,"admin")
        print "===get endpoints %s " % endpoints
        
        projects = self.__call_api(ksendpoint,"GET","/projects",None,"admin")
        print "===get projects %s " % projects
        
        for project in projects["projects"]:
            if project["name"] == self.env["tenant"]:
                self.env["tenant_id"]=project["id"]
            
        #parse the endpoints from services list        
        self._get_endpoints_v3(services, endpoints)
    
    def tearDown(self):
        if (self.conn != None):
            self.conn.close()
               
    def _is_service(self,service_id,services,type):
        for service in services["services"]:
            if service["type"] == type and service["id"] == service_id:
                return True
        return False             
        
    def _get_endpoints_v3(self,services,endpoints):
        
        self.cinder_endpoints = []
        self.nova_endpoints = []
        self.glance_endpoints = []
        self.keystone_endpoints = []
        
        for endpoint in endpoints["endpoints"]:
            print "endpiont %s " % endpoint
            if  self._is_service(endpoint["service_id"], services,'volume'):
                print "cinder endpoints " , endpoint['links']
                self.cinder_endpoints.append(endpoint)
            elif self._is_service(endpoint["service_id"], services,'compute'):
                print "compute endpoints", endpoint['links'] 
                self.nova_endpoints.append(endpoint)
            elif self._is_service(endpoint["service_id"], services,'image'):
                print "image endpoints",endpoint['links']
                self.glance_endpoints.append(endpoint) 
            elif self._is_service(endpoint["service_id"], services,'network'):
                print 'network endpoints', endpoint['links']
                self.quantum_endpoints.append(endpoint)
            elif self._is_service(endpoint["service_id"], services,'identity'):
                print 'identify endpoints', endpoint['links']
                self.keystone_endpoints.append(endpoint)
                
    
    def _get_auth_info_v3(self):
        params = '''
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": "%s"
                            },
                            "name": "%s",
                            "password": "%s"
                        }
                    }
                },
                "scope":{
                    "project":{
                        "domain":{
                            "name":"Default"
                         },
                        "name":"admin"
                    }
                }
            }
         }
        ''' % (self.env["domain"],self.env["username"],self.env["password"])
        return params
     
    def __do_post(self,url,body,header):
        urlobj=urlparse.urlparse(url)
        
        if (self.conn == None):
            conn = httplib.HTTPConnection(urlobj.netloc)
        
        conn.request("POST",urlobj.path, body, header)
        response = conn.getresponse()
        
        data = response.read()
        return data, response.getheaders()
    
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
    
    def __call_api(self,endpoints,method,path,params, urltype='public' ):
        
        for endpoint in endpoints:
            if endpoint["interface"] == urltype:
                converted_url = endpoint["url"]
                if endpoint["url"].find("tenant_id") != -1:
                    converted_url = endpoint["url"] % self.env
                scheme, netloc, rootpath, query, frag = urlparse.urlsplit(converted_url)
                    
        
        print "call_api with",scheme,netloc,rootpath,query,frag
        
        if netloc.split(':')[0] == 'localhost':
            netloc = self.env['url'].split(':')[0] + ":" + netloc.split(':')[1]
        
        api_conn =  httplib.HTTPConnection(netloc)
        headers = {"Content-Type":"application/json","X-Auth-Token":self.apitoken,"X-Subject-Token": self.apitoken ,"Vary":"X-Auth-Token,X-Subject-Token" }
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
 
        