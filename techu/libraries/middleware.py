from django.conf import settings
from django.db import connections, connection
from generic import *
from copy import deepcopy

class ConnectionMiddleware(object):
  def process_request(self, request):
    '''
    Automatically setup connections to the mysql41 interface
    of the Sphinx realtime indexes. 
    One connection is created for each index.
    '''
    cursor = connection.cursor()
    sql = '''SELECT sp_searchd_id, value FROM sp_searchd_option 
             WHERE sp_option_id = 138 AND value LIKE "%%mysql41"'''
    cursor.execute(sql)
    ports = {}
    for row in cursorfetchall(cursor):
      ports[row['sp_searchd_id']] = int(row['value'].split(':')[-2])
    sql = '''SELECT sp_searchd_id, value FROM sp_searchd_option 
             WHERE sp_option_id = 188'''
    hosts = {}
    for row in cursorfetchall(cursor):
      hosts[row['sp_searchd_id']] = row['value']

    sql = '''SELECT sci.sp_index_id, 
             (SELECT name FROM sp_indexes si WHERE si.id = sci.sp_index_id) AS index_name 
             FROM sp_configuration_index sci 
             JOIN sp_configuration_searchd scs 
             ON sci.sp_configuration_id = scs.sp_configuration_id
             WHERE scs.sp_searchd_id = %d'''
    for searchd, port in ports.iteritems():          
      cursor.execute(sql % searchd)
      r = cursorfetchall(cursor)
      for row in r:
        alias = 'sphinx:' + str(row['index_name'])
        connections.databases[alias] = deepcopy(connections.databases['default'])
        connections.databases[alias]['NAME'] = '_'
        connections.databases[alias]['USER'] = ''
        connections.databases[alias]['PASSWORD'] = ''
        host = 'techu.local'
        if searchd in hosts:
          host = hosts[searchd]
        connections.databases[alias]['HOST'] = host
        connections.databases[alias]['PORT'] = ports[searchd]
    return None
