'''
Created on Dec 12, 2012

@author: hill
'''
import unittest
import base64
from Crypto.Cipher import AES
import json




BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]
mode = AES.MODE_CBC

class TestSimpleToken(unittest.TestCase):

    def _encrypt(self, raw):
        raw = pad(raw)
        iv = '\0' * 16
        
        #iv = Random.new().read( AES.block_size )
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw))

    def _decrypt(self, enc):
        iv = '\0' * 16
      
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        return unpad(cipher.decrypt(base64.b64decode(enc)))


    def test_encrypt(self):
        
        key = base64.b64decode("JLQAGzg0jju4PW0ty3jKFw==")
        
        #text = '{"username": "test", "expiration": 1355854311344.885}';
        
        text = "{'username': 'admin', 'expiration': 1355854311344.885}"
        self.key = key

        enc= self._encrypt(text)
        
        print 'ref','AI6fCV/tt6dfoDuv0kShB9M2AMMEl5fUE7TfZ4LWzohwHTi8IuLIVjafLKpOg47k'
        
        print 'encrpty',enc
        
        raw =self._decrypt(enc)
        
        print 'decrpty',raw
        
    def test_decrypt(self):
        key = base64.b64decode("JLQAGzg0jju4PW0ty3jKFw==")
        print 'key is %s' % key
        self.key=key
        
        token='+jeRFU5xCMi7DquRjEKWS69WnY/tMWfj0zARBu7/OLXoUGRwgwRWadb8dngt8j1/fjrGY3aetyddqqTHXaB/cceJISI1mKSV68oAUq/GBhM='
        
        raw = self._decrypt(token)
        
        print "descrpt  %s" % raw

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
