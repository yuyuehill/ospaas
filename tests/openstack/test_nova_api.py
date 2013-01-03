'''
Created on Oct 28, 2012

@author: hill
'''

import json
import re
import random
from tests.openstack import test_os_base
import time

class  TestNova(test_os_base.TestOpenStackBase): 
   
    def setUp(self):
        
        self.env = self.GEMINI
        test_os_base.TestOpenStackBase.setUp(self)
        
    
    def list_extends(self):
        params = json.dumps({})        
        dd = self.call_nova_api('GET', '/extensions', params)
        return dd
    
    
    def list_flavors(self):
        params = json.dumps({})
        dd = self.call_nova_api('GET', '/flavors', params)
        return dd
    
    def list_images(self):
        params = json.dumps({})
        dd = self.call_nova_api('GET', '/images', params)
        return dd
    
    def list_servers(self, server_id):
        params = json.dumps({})
        if server_id is None:
            dd = self.call_nova_api('GET', '/servers', params)
            return dd['servers']
        else:
            dd = self.call_nova_api('GET', '/servers/%s' % server_id, params)
            return dd['server']
        
    def list_networks(self):
        
        params = json.dumps({})
        
        #if quantum used as network service
        if self._dict.has_key('quantum_endpoints') :
            dd = self.call_quantum_api('GET', '/networks', params)
            return dd
        else:
            dd = self.call_nova_api('GET', '/os-networks', params)
            return dd
                                        
      
    def get_flavor(self):
       
        for flavor in self.list_flavors()['flavors']:
            print flavor['name']
            name = flavor['name']
            ref = flavor['links'][0]['href']
            if name == 'm1.tiny':
                break
        return name, ref
    
    
    def get_image(self):
        for image in self.list_images()['images']:
            print 'get image ', image
            name = image['name']
            uri = image['links'][0]['href']
            if re.search('cirros', name):
                return name, uri
            if re.search('rhel',name):
                return name, uri
            
        return None, None
    
    def get_network(self):
        
        #return the first network
        for network in self.list_networks()['networks']:
            print network
            return network
        
    def update_meta_data(self,service_id):
        
        meta_data = json.dumps({
                                'metadata': {
                                         'pattern_name':'hiltest',
                                         'service_name':'hillservice'}})
        dd = self.call_nova_api('PUT', '/servers/%s' % service_id, meta_data)
        
        print 'update meta data %s' % dd
        return dd
    
    def create_server(self, image_uri, flavor_uri, config_drive='true'):
        server_params = json.dumps({
                            'server' : {
                                        'flavorRef':flavor_uri,
                                        'imageRef':image_uri,
                                        'metadata': {'owner':'hill'} ,
                                        'name':'hill_server_%d' % random.randint(1, 10000),
                                        'config_drive':config_drive
                            }
                         })
        
        dd = self.call_nova_api('POST', '/servers', server_params)
        return dd['server']
    
    def delete_server(self, server_id):
        server_params = json.dumps({})
        self.call_nova_api('DELETE', '/servers/%s' % server_id, server_params)
        return {"id":server_id} 
       
    #test extends    
    def test_extends(self):
                
        dd = self.list_extends()    
        for extension in dd['extensions']:
            print "name", extension["name"]
    
    #test servers        
    def test_server(self):
       
        flavor_name, flavor_ref = self.get_flavor()
        image_name, image_ref = self.get_image()
        
        self.assertFalse(image_name is None, "failed to get image name")
        self.assertFalse(image_ref is None, "failed to get image ref")
        
        #boot server
        dd = self.create_server(image_ref, flavor_ref, 'True')
        
        #update meta data
        self.update_meta_data(dd['id'])
                
        #check the status
        for x in range(100):
            #get the status of the created volume until it is available or error
            server = self.list_servers(dd['id'])
            
            if server['status'] == 'ACTIVE':
                print server 
                #self.delete_server(dd['id'])
                break
            elif server['status'] == 'ERROR':
                #self.delete_server(dd['id'])
                break
            
            else:
                print 'wait for next turn %d' % x
                time.sleep(5)  
        
     
        
        
