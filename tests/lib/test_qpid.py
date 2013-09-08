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
from qpid.messaging import *
#from nova.openstack.common import jsonutils

class TestQpid(unittest.TestCase):
    
    

    def _testDateTime(self):
        print "test date time "
        broker =  "tivx013:5672"
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
            
    def testConnection(self):
        print "begin to connect" 
        
        connection = Connection(
                                host="tivx013",
                                port=5672,
                                heartbeat=5,
                                reconnect=True,
                                reconnect_interval_min=0,
                                reconnect_interval_max=0,
                                reconnect_limit=0,
                                reconnect_timeout=0
                                )
        connection.open()
        print "open connection"
        session = connection.session()
        print "create session"
        sender = session.sender("test; {create: always}")
        print "get sender"
        id = 0
        while True:
            try:
                print("begin to sent %d" % id)
                sender.send(
                            { "hello": "world" }
                            )
                print("Sent %d" % id)
                id += 1
            except KeyboardInterrupt:
                break
            except Exception ,e :
                print "error in except %s " % e 
            finally:
                time.sleep(1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()