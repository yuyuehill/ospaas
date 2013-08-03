'''
Created on Dec 11, 2012

@author: hill
'''


from qpid.messaging import *
import datetime
import sys
import unittest
import json
import time
#from nova.openstack.common import jsonutils

class TestQpid(unittest.TestCase):


    def testDateTime(self):
    
        broker =  "tivx013:5672"
        topic = "amq.topic"
        connection = Connection(broker,reconnect=True)
        try:
            connection.open()
            session = connection.session()
            sender = session.sender(topic)

            while True:
                update_time = datetime.datetime.now().__str__()
                msg = Message({u'created_at': datetime.datetime.now(), 'update_at':update_time})
            
                sender.send(msg)
                #print message.content['created_at'].datetime()
            
                print msg
                time.sleep(2)
            
            session.acknowledge()
        except MessagingError,m:
            print m
        
        connection.close()
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()