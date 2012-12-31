

from eventlet import wsgi
import eventlet

def hook(env, arg1, arg2, kwarg3=None, kwarg4=None):
    print 'Hook called: %s %s %s %s %s' % (env, arg1, arg2, kwarg3, kwarg4)

def hello_world(env, start_response):
    env['eventlet.posthooks'].append(
        (hook, ('arg1', 'arg2'), {'kwarg3': 3, 'kwarg4': 4}))
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello, World!\r\n']

wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 5000)),
                              certfile='/root/ssl/certs/keystone.pem',
                              keyfile='/root/ssl/private/keystonekey.pem',
                              server_side=True),
            hello_world)
