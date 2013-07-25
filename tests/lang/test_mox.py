'''
Created on Jun 2, 2013

@author: hill
'''

import os
import unittest
import mox


class MyObject(object):
    def __init__(self):
        pass
    def get_mydatas(self):
        if(os.path.exists("/home/hill")):
            print "hill"
        else:
            return "notfound"
    

class TestMyObject(unittest.TestCase):
   
   def setup(self):
       pass
       
   def test_get_mydatas(self):
       pass
   
   def test_path(self):
       m =  mox.Mox()
       m.StubOutWithMock(os.path, 'exists')
       os.path.exists("/home/hill").AndReturn(False)
       m.ReplayAll()
       mytest = MyObject()
       self.assertEquals(mytest.get_mydatas(),"notfound")
       m.VerifyAll()
       
      