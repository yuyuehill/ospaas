'''
Created on Dec 11, 2012

@author: hill
'''
import unittest
import sys
import datetime
from qpid.messaging import *


class TestQpid(unittest.TestCase):


    def testDateTime(self):
    
        broker =  "tivx013:5672"
        address = "amq.topic"
        connection = Connection(broker)
        try:
            connection.open()
            session = connection.session()
            sender = session.sender(address)
            receiver = session.receiver(address)
            sender.send(Message({u'created_at': datetime.datetime.now()}))
            message = receiver.fetch()
            print message.content
            session.acknowledge()
        except MessagingError,m:
            print m
        
        connection.close()
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()