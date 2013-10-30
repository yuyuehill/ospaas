'''
Created on Dec 11, 2012

@author: hill
'''



import datetime
import traceback
import sys
import unittest
import json
import logging
import time
import memcache
from keystone.openstack.common import jsonutils

#from nova.openstack.common import jsonutils

SVT1 =  {"server":"172.16.135.202:11211", "user_id":"0dbc10b9434e4b9892713c7496a5f1ab"}
SVT2 =  {"server":"172.16.133.232:11211", "user_id":"77853224da524a8da5019a023eece238"}

class TestMemcache(unittest.TestCase):
    
    def setUp(self):
        self.env = SVT2
        #self.client = memcache.Client([""],debug=1,cache_cas=True)
        self.client = memcache.Client([self.env["server"]],debug=1,cache_cas=True)
    
    def _prefix_user_id(self,user_id):
        return 'usertokens-%s' % user_id.encode('utf-8')
    
    def _prefix_token_id(self,token_id):
        return 'token-%s' % token_id.encode('utf-8')
    
    def test_list_tokens(self):
        user_key = self._prefix_user_id(self.env["user_id"])
        user_record = self.client.get(user_key) or ""
        token_list = jsonutils.loads('[%s]' % user_record)
        i = 0                                  
        #for token_id in token_list:
        #    ptk = self._prefix_token_id(token_id)
        #    token = self.client.get(ptk)
        #    i = i + 1
        #    if not token:
        #        print "skip %s %s " % (i, len(token_list))
        #        continue    
            #print token['expires']
        print "total %s " % len(token_list)
            
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
