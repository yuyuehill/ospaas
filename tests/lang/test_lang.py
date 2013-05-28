'''
Created on May 19, 2013

@author: hill
'''

import unittest
import urlparse 

class LangTest(unittest.TestCase):
    
    def test_file_open(self):
        
        passfile=open("/etc/passwd","rb")
        print passfile
   
    def test_url(self):
        mytest="myschedume://xxxx-xxx-xxx"    
        uri=urlparse.urlparse(mytest)
        print "this is the schema" ,uri.scheme
        print "this is the netloc" ,uri.netloc
        
    def test_attr(self):
        assert hasattr(self, "test_attr") 
        mymethod=getattr(self,"test_url")
        mymethod()  
         