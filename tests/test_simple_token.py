'''
Created on Dec 12, 2012

@author: hill
'''
import unittest
import base64
from Crypto.Cipher import AES
import json

class Test(unittest.TestCase):

    def _unpad(self, string):
        # remove padding from decrypted string
        return string[0:-ord(string[-1])]


    def testSimpleToken(self):
        secret = "EzzNhXb17ZsOu9j18Ek7jg=="
        _iv = '\0' * 16
        secret_key = base64.b64decode(secret)
        
        json_str=json.dumps({"username":"hill"})
      
        print 'secret_key', secret_key , "json_str" , json_str
        BLOCK_SIZE=16
        decryptor=AES.new(secret_key,AES.MODE_CBC,_iv)
        encryptor=AES.new(secret_key,AES.MODE_CBC,_iv)
        PADDING='\0'
        pad= lambda s: s +(BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
  
              
        padding_json=pad(json_str)
        print 'padding_json', padding_json
        
        encrpt_json= decryptor.encrypt(padding_json)
        print 'encrpty_json', encrpt_json
        
        simple_token=base64.b64encode(encrpt_json)
             
        print "simple token_json ", simple_token
        
        decoded_token = base64.b64decode(simple_token)
        print "decoded  token", decoded_token
       
        decrypt_str= encryptor.decrypt(decoded_token)
        
        print "decrpt_str", decrypt_str
        charset='ISO8859-1'
        convert_str = decrypt_str.decode(charset)
        
        print 'decoded str ', convert_str
        json_token= json.loads(self._unpad(convert_str))
        print "json_token", json_token

    def test_sample_aes(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()