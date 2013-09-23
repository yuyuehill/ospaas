'''
Created on 2013

@author: yuyue
'''
import unittest
import httplib
import json


class Test(unittest.TestCase):

    TIVX043 = {'url':'tivx043:5000', 'username':'admin' , 'password':'admin' , 'tenant':'admin','domain':'deFault'}
    def setUp(self):
        
        self.env = self.TIVX043
  

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
        dd = json.loads(data)
        self.conn.close()

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()