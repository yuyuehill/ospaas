

import unittest


import os
import ssl
from sqlalchemy import *


import sqlalchemy.util as util
import string,sys


class TestDB2(unittest.TestCase):
    
    def setup(self):
        self.engine = create_engine('mysql',
                             {'db':'test','user':'root','passwd':'caoyan','host':'127.0.0.1'}, echo=True)  

        
    
    def test_query(self):
        
        print self.engine