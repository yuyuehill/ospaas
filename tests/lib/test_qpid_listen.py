'''
Created on Dec 11, 2012

@author: hill
'''


from qpid.messaging import *
import datetime
import sys
import unittest
import json

#from nova.openstack.common import jsonutils

class TestQpid(unittest.TestCase):


    def testDateTime(self):
    
        broker =  "tivx013:5672"
        topic = "amq.topic"
        connection = Connection(broker, reconnect=True,heartbeat=10)
        try:
            connection.open()
            session = connection.session()

            receiver = session.receiver(topic)
            
            while True:
                message = receiver.fetch()
                #print message.content['created_at'].datetime()
            
                print message.content['created_at']
                print json.dumps(message.content)
                
            
            session.acknowledge()
        except MessagingError,m:
            print m
        
        connection.close()
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()