'''
Created on Jun 2, 2013

This is a test for functools which has a convienced way to generate
@author: hill
'''

import functools



def log_call(f):
    @functools.wraps(f)
    def logging(*args, **kargs):
        print 'calling %(arg)s %(kargs)s' % {"arg":args,"kargs":kargs}
        output = f(*args,**kargs)
        print 'called  %s' %output
    return logging   

@log_call
def foo(*args, **kargs):
    #print 'args is ' , args

    for v in args:
        print "arg ",v
        

    for (k,v) in kargs.iteritems():
        print "karg",k,v
    print '==========='
    return 'output'
 
foo(1,2,3,4)
foo(1,3,a=3,b=4)
foo(a=3,b=4)   