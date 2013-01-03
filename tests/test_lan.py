
import tests.openstack.test_os_base

abc = { "test":"111",
       "test2":"fff"
       }

abc2 = { "test":"111",
       "test2":"fff"
       }


print abc.items()+ abc2.items()

def func1 (p1 = None, p2 = None, p3= None):
    print 'params %s %s %s ' % (p1, p2, p3)

class  myclass():
    def __init__(self, param = None, param2= None):
        print "param %s, %s" % (param,param2)
    def _hide_methd(self):    
        print "i am in hide method"
       
        
    def __hide_methd1(self):    
        print "i am in hide method1"
        
class myparent(myclass):
    def public_methd(self):
        self._hide_methd()

myc = myclass(param2 = "Params")    

myp = myparent()
myp.public_methd()

func1 (p2 = "test") 
import os


import json

print json.dumps({'username':'test','expiration':'1355854311344.885'})
json.loads('{"username":"test","expiration":"1355854311344.885"}')


          
