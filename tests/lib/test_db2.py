

import unittest


import os
import ssl
import sqlalchemy
from sqlalchemy import *
import ibm_db_sa.ibm_db_sa

import sqlalchemy.util as util
import string,sys


class TestDB2(unittest.TestCase):
    
    def setup(self):
       db2 = sqlalchemy.create_engine('ibm_db_sa://noa14447:passw0rd@172.17.42.80:50000/openstac')
       
  
    def test_query(self):
        
        print self.engine