'''
Created on Dec 31, 2012

@author: hill
'''


import eventlet
import socket
from eventlet import util
import os

certfile = "/home/hill/git/ospaas/examples/pki/certs/ssl_cert.pem"
keyfile = "/home/hill/git/ospaas/examples/pki/private/ssl_key.pem"

def listen_ssl_socket(address=('127.0.0.1', 0)):
    sock = util.wrap_ssl(socket.socket(), certfile,
          keyfile, True)
    sock.bind(address)
    sock.listen(5000)
  
    return sock

def serve(listener):
    sock, addr = listener.accept()
    stuff = sock.read(8192)
    sock.write('response')
  
sock = listen_ssl_socket()
  
server_coro = eventlet.spawn(serve, sock)

client = util.wrap_ssl(eventlet.connect(('127.0.0.1', sock.getsockname()[1])))
client.write('line 1\r\nline 2\r\n\r\n')
print client.read(8192)
server_coro.wait()

