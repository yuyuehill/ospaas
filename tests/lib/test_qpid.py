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
    
        broker =  "172.16.100.176:5672"
        topic = "amq.topic"
        connection = Connection(broker)
        try:
            connection.open()
            session = connection.session()
            sender = session.sender(topic)
            receiver = session.receiver(topic)
            update_time = datetime.datetime.now().__str__()
            msg = Message({u'created_at': datetime.datetime.now(), 'update_at':update_time})
            
            sender.send(msg)
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