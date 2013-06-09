'''
Created on Jun 6, 2013

@author: hill
'''


import ConfigParser
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

OS_PROJECTS= {"nova":"/etc/nova/nova.conf",
              "keystone":"/etc/keystone/keystone.conf",
              "glance":"/etc/glance/glance-registry.conf",
              "cinder":"/etc/cinder/cinder.conf"
              }

config = ConfigParser.RawConfigParser()
config.read('/etc/nova/nova.conf')
connection = config.get("DEFAULT", "sql_connection")
graph = create_schema_graph(metadata=MetaData(connection),
                 show_datatypes=False,
                 show_indexes=False,
                 rankdir='LR',
                 concentrate=False)
graph.write_png('nova.png')