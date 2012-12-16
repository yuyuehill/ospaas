'''
Created on Oct 28, 2012

@author: hill
'''

import httplib
import json
import random
import test_os_base
import time



class  TestClinder(test_os_base.TestOpenStackBase): 
    
    def setUp(self):
        self.env = self.LOCAL
        test_os_base.TestOpenStackBase.setUp(self)
        
  
       
    def __list_volumes(self):
        params = json.dumps({})        
        dd = self.__call_cinder_api('GET', '/volumes', params)
        self.assertTrue(dd.has_key("volumes"), "failed to list volume")
       
        return dd['volumes']
        
    def __create_volume(self, name, size):
        
        params = json.dumps({"volume": {"display_name": name, "display_description": "hill_test_volume" + name, "size": size}})
        dd = self.__call_cinder_api("POST", "/volumes", params)       
        self.assertTrue(dd.has_key("volume"), "failed to create volume")
       
        return dd["volume"]
    
    def __delete_volume(self, tenant_id, volume_id):
        params = json.dumps({"tenant_id":tenant_id, "volume_id":volume_id})
        dd = self.__call_cinder_api("DELETE", "/volumes/%s" % volume_id , params)
        #the delete api will not return any body
        return {"volume_id":volume_id}
    
    def __get_volume(self, volume_id):
        dd = self.__call_cinder_api("GET", "/volumes/%s" % volume_id, json.dumps({}))
        self.assertTrue(dd.has_key("volume"), "failed to get volume")
        return dd['volume']
        
    def test_cinder_list_create_delet(self):

        
        volumes = self.__list_volumes()
        print "list volumes", volumes
        
        volume = self.__create_volume("hill_{0}".format(random.randint(1, 10000)), 1)
        print "create volume", volume
        
        for x in range(5):
            #get the status of the created volume until it is available or error
            volume = self.__get_volume(volume["id"])
            if volume["status"] == "available" or volume["status"] == "error":
                volume = self.__delete_volume(self.tenant_id, volume["id"])
                print "delete the created volume", volume
                break
            else:
                print "wait for next turn %d" % x
                time.sleep(5)  
            
           
        print "finished testing"
        
