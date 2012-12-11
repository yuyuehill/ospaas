'''
Created on Oct 28, 2012

@author: hill
'''

import json
import re
import random
import test_os_base
import time

class  TestNova(test_os_base.TestOpenStackBase): 
   
    def setUp(self):
        
        self.env = self.HILLOPEN
        test_os_base.TestOpenStackBase.setUp(self)
        
    
    def _list_extends(self):
        params = json.dumps({})        
        dd = self._call_nova_api('GET', '/extensions', params)
       
        return dd
    
  
    
    def _list_flavors(self):
        params = json.dumps({})
        dd = self._call_nova_api('GET', '/flavors', params)
        return dd
    
    def _list_images(self):
        params = json.dumps({})
        dd = self._call_nova_api('GET', '/images', params)
        return dd
    
    def _list_servers(self, server_id):
        params = json.dumps({})
        if server_id is None:
            dd = self._call_nova_api('GET', '/servers', params)
            return dd['servers']
        else:
            dd = self._call_nova_api('GET', '/servers/%s' % server_id, params)
            return dd['server']
        
    def _list_networks(self):
        
        params = json.dumps({})
        
        #if quantum used as network service
        if self.__dict__.has_key('quantum_endpoints') :
            dd = self._call_quantum_api('GET', '/networks', params)
            return dd
        else:
            dd = self._call_nova_api('GET', '/os-networks', params)
            return dd
                                        
    @classmethod    
    def _get_flavor(self):
        
        for flavor in self._list_flavors()['flavors']:
            print flavor['name']
            name = flavor['name']
            ref = flavor['links'][0]['href']
            if name == 'm1.tiny':
                break
        return name, ref
    
    
    def _get_image(self):
        for image in self._list_images()['images']:
            print 'get image ', image
            name = image['name']
            uri = image['links'][0]['href']
            if re.search('cirros', name):
                return name, uri
            
        return None
    
    def _get_network(self):
        
        #return the first network
        for network in self.self._list_networks()['networks']:
            print network
            return network
    
    def _create_server(self, image_uri, flavor_uri, config_drive=True):
        server_params = json.dumps({
                            'server' : {
                                        'flavorRef':flavor_uri,
                                        'imageRef':image_uri,
                                        'metadata': {'owner':'hill'} ,
                                        'name':'hill_server_%d' % random.randint(1, 10000),
                                        'config_drive':config_drive
                            }
                         })
        
        dd = self._call_nova_api('POST', '/servers', server_params)
        return dd['server']
    
    def _delete_server(self, server_id):
        server_params = json.dumps({})
        self._call_nova_api('DELETE', '/servers/%s' % server_id, server_params)
        return {"id":server_id} 
       
    #test extends    
    def test_extends(self):
                
        dd = self._list_extends()    
        for extension in dd['extensions']:
            print "name", extension["name"]
    
    #test servers        
    def _test_server(self):
       
        flavor_name, flavor_ref = self._get_flavor()
        image_name, image_ref = self._get_image()
        
        #boot server
        dd = self._create_server(image_ref, flavor_ref, image_ref)
        
        #check the status
        for x in range(100):
            #get the status of the created volume until it is available or error
            server = self._list_servers(dd['id'])
            if server['status'] == 'ACTIVE':
                print server 
                #self._delete_server(dd['id'])
                break
            elif server['status'] == 'ERROR':
                #self._delete_server(dd['id'])
                break
            
            else:
                print 'wait for next turn %d' % x
                time.sleep(5)  
        
        
