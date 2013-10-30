

      
import unittest
import sqlalchemy
from sqlalchemy import *
import sys
import ibm_db_sa
      
      
      
      
SVT_172_16_11_205="ibm_db_sa://noa37366:passw0rd@172.16.11.205:50000/openstac"
db2 = sqlalchemy.create_engine(SVT_172_16_11_205)
    

metadata = MetaData()
instances_table = Table('instances', metadata, autoload=True, autoload_with=db2)
print instances_table

