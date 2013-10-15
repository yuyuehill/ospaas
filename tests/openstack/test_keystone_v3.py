'''
Created on 2013

@author: yuyue
'''
import unittest
import httplib
import json


class Test(unittest.TestCase):

    TIVX043 = {'url':'tivx043:5000', 'adminurl':'tivx013:35357','username':'admin' , 'password':'admin' , 'tenant':'admin','domain':'Default'}
    RTP = {'url':'172.17.43.48:5000', 'adminurl':'172.17.43.48:35357','username':'admin' , 'password':'passw0rd' , 'tenant':'admin','domain':'Default'}
    
    SVT = {'url':'172.16.133.232:5000', 'adminurl':'172.16.133.232:35357','username':'admin' , 'password':'passw0rd' , 'tenant':'admin','domain':'Default'}
    def setUp(self):
        
        self.env = self.SVT
  

    def test_auth_token(self):
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
        print params
        
        headers= {"Content-Type":"application/json"}

        self.conn = httplib.HTTPConnection(self.env['url'])
     
        self.conn.request("POST","/v3/auth/tokens",params,headers)
       
        response = self.conn.getresponse()
        
        data = response.read()
        
        print "Got reponse %s" % data
        
        #get the subject token
        headers = response.getheaders()
        for header in headers:
            if header[0] == "x-subject-token":
               self.apitoken = header[1]
               
        headers= {"Content-Type":"application/json", "X-Auth-Token":self.apitoken}

        self.conn.request("GET","/v3/users",None,headers)
        response = self.conn.getresponse()
        print "Get response %s " % response.read()

        
        self.conn.request("GET","/v3/projects",None,headers)
        response = self.conn.getresponse()
        print "Get response %s " % response.read()

        
        self.conn = httplib.HTTPConnection(self.env['adminurl'])
        self.conn.request("GET","/v3/endpoints",None,headers)
        response = self.conn.getresponse()
        print "Get response %s " % response.read()
        self.conn.close()

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()