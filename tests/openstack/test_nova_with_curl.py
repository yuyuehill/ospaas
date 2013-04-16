



import unittest
import pycurl
import urllib
import json
import StringIO
import random

class TestCurlNova(unittest.TestCase):
    
    GEMINI = {"host":"geminios", "tenant":"admin", "user":"admin", "password":"admin"}
    TIVX043 = {"host":"tivx043", "tenant":"admin", "user":"admin", "password":"admin"}
    
    def setUp(self):
        self.env = self.TIVX043
        self.keystone_url = "http://%s:5000/v2.0/tokens" % self.env["host"]
        self.auth_data = "{\"auth\":{\"passwordCredentials\":{\"username\":\"%s\",\"password\":\"%s\"},\"tenantName\":\"%s\"}}" % (self.env["user"], self.env["password"], self.env["tenant"])
        self.nova_url = "http://%s:8773"
        
    
        b = StringIO.StringIO()
       
        #get tokens
        c = pycurl.Curl()
        c.setopt(c.URL, self.keystone_url)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
      
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, self.auth_data)
        c.setopt(c.WRITEFUNCTION, b.write)
        c.setopt(c.VERBOSE, True)
        c.perform()
        ret = json.loads(b.getvalue())
        print 'return data', ret
        
        self.token = ret["access"]["token"]["id"]
        
        for service in ret['access']['serviceCatalog']:
            if service['type'] == 'volume':
                print "cinder endpoints " , service['endpoints']
                self.cinder_endpoints = service['endpoints']
            elif service['type'] == 'compute':
                print "compute endpoints", service['endpoints'] 
                self.nova_endpoints = service['endpoints']
            elif service['type'] == 'image':
                print "image endpoints", service['endpoints']
                self.glance_endpoints = service['endpoints'] 
            elif service['type'] == 'network':
                print 'network endpoints', service['endpoints']
                self.quantum_endpoints = service['endpoints']
            elif service['type'] == 'identity':
                print 'identify endpoints', service['endpoints']
                self.keystone_endpoints = service['endpoints']
    
        
        
    
    def _test_run_server_with_config_drive(self):
        
        new_server_with_config_drive = """<?xml version="1.0" encoding="UTF-8"?>
            <server name="hill_server_xml"  imageRef="43d5adf1-3390-46d2-9061-1e8aeb16826a" flavorRef="1" config_drive="true" whatiswon="hh"> 
            </server>
           """
        print new_server_with_config_drive
        b = StringIO.StringIO()
       
        c = pycurl.Curl()
        url = "%s/servers" % self.nova_endpoints[0]["publicURL"]
        
        #c.setopt(c.URL, url)
        c.setopt(c.URL,str(url))
        auth_token = 'X-Auth-Token:%s' % self.token
        c.setopt(c.HTTPHEADER, ['Content-Type: application/xml; charset=ISO-8859-1', str(auth_token) ])
        c.setopt(c.WRITEFUNCTION, b.write)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, new_server_with_config_drive)
        c.setopt(c.VERBOSE, True)
        c.perform()
        
        print b.getvalue()

    def _test_run_server_with_config_drive_json(self):
        

        config_drive_json = json.dumps({
                            'server' : {
                                        'flavorRef':'1',
                                        'imageRef':'43d5adf1-3390-46d2-9061-1e8aeb16826a',
                                        'metadata': {'owner':'hill'} ,
                                        'name':'hill_server_%d' % random.randint(1, 10000),
                                        'config_drive': 'true'
                              }
                          })
         
        print config_drive_json
        
        b = StringIO.StringIO()
       
        c = pycurl.Curl()
        url = "%s/servers" % self.nova_endpoints[0]["publicURL"]
        
        #c.setopt(c.URL, url)
        c.setopt(c.URL,str(url))
        auth_token = 'X-Auth-Token:%s' % self.token
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json', str(auth_token) ])
        c.setopt(c.WRITEFUNCTION, b.write)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, config_drive_json)
        c.setopt(c.VERBOSE, True)
        c.perform()
        
        print b.getvalue()
        
    def test_os_network(self):
        b = StringIO.StringIO()
       
        c = pycurl.Curl()
        url = "%s/os-networks" % self.nova_endpoints[0]["publicURL"]
        
        #c.setopt(c.URL, url)
        c.setopt(c.URL,str(url))
        auth_token = 'X-Auth-Token:%s' % self.token
        #c.setopt(c.HTTPHEADER, ['Content-Type: application/xml; charset=ISO-8859-1 ; Accept: application/xml', str(auth_token) ])
        c.setopt(c.HTTPHEADER, ['Accept: application/xml', str(auth_token) ])
        c.setopt(c.WRITEFUNCTION, b.write)
        c.setopt(c.VERBOSE, True)
        c.perform()
        
        
        buff = b.getvalue();
        print buff
        b.close()
        networks=json.loads(buff)
        
        if networks["networks"][0]["bridge_interface"] is None:
            print "the bridge interface is none"
        else:
            print "this bridge interface is string"
        
        
        
