

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
        

myc = myclass(param2 = "Params")    

func1 (p2 = "test") 
import os


ROOTDIR = os.path.dirname(os.path.abspath(os.curdir))
print ROOTDIR   