from django.conf import settings
from django.db import connections, connection
from generic import *
from copy import deepcopy
from traceback import format_exception
import sys, re

class ExceptionLoggingMiddleware(object):
  '''
  |  Exception middleware which allows more clear & efficient printouts of errors raised.
  |  Particularly, it overrides the default debug pages of Django which contain extensive HTML
  |  and returns plain text in case the request is performed with the *curl* command-line tool
  |  or JSON-formatted as an API response inside client applications.
  '''
  def process_response(self, request, response):
    if response.status_code != 200:
      ''' 
      If called from command line print output plain text, otherwise return as JSON
      '''
      if not re.match(r'^curl/', request.META['HTTP_USER_AGENT'].lower()) is None:
        response.content = r
      else:      
        indent = 4
        separators = (',', ': ')
        response.content = json.dumps(r, cls=Serializer, indent = indent, separators = separators)
    return response

class ConnectionMiddleware(object):
  '''    
  |  Automatically setup connections to the mysql41 interface of the Sphinx realtime indexes. 
  |  One connection is created for each index. 
  |  This is implemented as a middleware in order to make connections available to all requests.
  '''
  def process_request(self, request):
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

    sql = '''SELECT sci.sp_index_id 
             FROM sp_configuration_index sci 
             JOIN sp_configuration_searchd scs 
             ON sci.sp_configuration_id = scs.sp_configuration_id
             WHERE scs.sp_searchd_id = %d'''
    for searchd, port in ports.iteritems():          
      cursor.execute(sql % searchd)
      r = cursorfetchall(cursor)
      for row in r:
        alias = 'sphinx:' + str(row['sp_index_id'])
        connections.databases[alias] = deepcopy(connections.databases['default'])
        connections.databases[alias]['NAME'] = '_'
        connections.databases[alias]['USER'] = ''
        connections.databases[alias]['PASSWORD'] = ''
        host = settings.APPHOST
        if searchd in hosts:
          host = hosts[searchd]
        connections.databases[alias]['HOST'] = host
        connections.databases[alias]['PORT'] = ports[searchd]
    return None

