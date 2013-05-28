'''
Created on May 22, 2013

@author: hill
'''


from webob import Request

import unittest

class TestWSGI(unittest.TestCase):
    def test_request(self):
       
        req = Request.blank("/mytest?id=1")
        print req.environ
    
    def test_web_app(self):
        