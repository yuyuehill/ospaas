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
        return "hill"
    

class TestMyObject(unittest.TestCase):
   
   def setup(self):
       self.obj_mocker=mox.Mox()
       
   def test_get_mydates(self):
       myobj = self.obj_mocker.CreateMock(MyObject)
       myobj.get_mydatas()
       mox.Replay(myobj)
       mox.Verify(myobj)     