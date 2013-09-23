'''
Created on 20130914

@author: yuyue
'''

import json
import re
import random

from tests.openstack import test_os_base
import time


class TestNovaFixedip(test_os_base.TestOpenStackBase):
    '''
    classdocs
    '''
   

    def setUp(self):
        '''
        Constructor
        '''
        self.env = self.TIVX043
        test_os_base.TestOpenStackBase.setUp(self)
   
    def test_fixed_ip_show(self):
        #works for tivx013
        #dd = self.call_nova_api('GET', '/os-fixed-ips/172.16.0.4', None)
        
        dd=self.call_nova_api('GET','/os-fixed-ips/9.111.102.187', None)
        print("=====test_fixed_ip_show %s" % dd)
        return dd

    def get_network_id(self):
        dd = self.call_nova_api('GET','/os-networks',None)
        print("======get network")
        return dd["networks"][0]['id']
    
    def _test_get_extends(self):
        dd = self.call_nova_api('GET','/extensions',None)
        #print("===get all extendsion %s" % dd)
        for ex in dd["extensions"]:
          print ex
        return dd
    
    def test_fixed_ip_by_net(self):
        network_id=self.get_network_id()
        print 'get network id %s' % network_id
        dd = self.call_nova_api('GET', '/os-networks/%s/net-fixed-ips ' % network_id  , None)
        print("=====test_fixed_ip_by_net %s" % dd)
        return dd
