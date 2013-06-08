import os, imp
import MySQLdb
import re, json, datetime
import redis
settings_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1])
settings = imp.load_source('settings', os.path.join( settings_path,  'settings.py'))
from django.http import HttpResponse
from django.db import models

modules = None
def _import(module_list):
  ''' 
  Dynamic imports may boost performance since functions require different packages 
  e.g. libraries.sphinxapi is only used for search and excerpts calls
  '''
  global modules
  for m in map(__import__, module_list):
    if not m in modules:
      modules.append(m)

def is_queryset(o):
  return isinstance(o, models.query.QuerySet)

def is_model(o):
  return isinstance(o, models.Model)

def debug(r):
  ''' Serialize and return object for debugging '''
  return R(r)

def is_queued(request):
  if 'queue' in request.REQUEST:
    return ( int(request.REQUEST['queue']) == 1 )
  else:
    return False

class Serializer(json.JSONEncoder):
  ''' JSON serializer for list, dict and QuerySet objects '''
  def default(self, o):
    if is_queryset(o):
      obj = []
      for q in o:
        opts = q._meta
        data = {}
        for field in opts.fields:
          if field.name == 'id':
            value = q.pk 
          else:
            value = field.value_from_object(q)
          name = field.name                      
          data[name] = value
        obj.append(data)
      return obj
    if isinstance(o, datetime.datetime):
      return int( time.mktime(o.timetuple()) )
    return json.JSONEncoder.default(self, o)

def E(code = 500, **kwargs):
  ''' Return an HttpResponse with error code '''
  response = HttpResponse()
  response.status_code = code
  if 'message' in kwargs:
    message = kwargs['message']
  else:
    message = 'Internal Server Error'
  response.content = message
  return response

def R(data, request = None, **kwargs):
  ''' 
  Return a successful, normal HttpResponse (code 200). 
  Serializes by default any object passed.
  '''
  if not request is None:
    if 'pretty' in request.REQUEST:
      kwargs['pretty'] = (request.REQUEST['pretty'].lower() in [ '1', 'true'])
  r = HttpResponse()
  defaults = { 'code' : 200, 'serialize' : True, 'pretty' : False }
  kwargs = dict(defaults.items() + kwargs.items())
  r.status_code = kwargs['code']
  if kwargs['pretty']:
    indent = 4
    separators = (',', ': ')
  else:
    indent = None
    separators = (',', ':')
  if kwargs['serialize']:
    data = json.dumps(data, cls=Serializer, indent = indent, separators = separators)
  r.content = data
  r.content_type = 'application/json;charset=utf-8'
  return r

def redis26():
  ''' Redis 2.6 client '''
  return redis.StrictRedis(
                 host = settings.REDIS_HOST, 
                 port = settings.REDIS_PORT, 
                 password = settings.REDIS_PASSWORD)

def cursorfetchall(cursor):
  ''' Returns all rows from a cursor as a dictionary '''
  desc = cursor.description
  return [
      dict(zip([col[0] for col in desc], row))
      for row in cursor.fetchall()
  ]

def regex_check(s, r = r'[^a-zA-Z0-9\-_]+'):
  return (re.match(r, s) is None)

def identq(s):
  ''' Quote an SQL identifier '''
  return '`' + s.replace('`', '') + '`'

def q(s):
  ''' DEPRECATED: Escape SQL parameter '''
  if not isinstance(s, basestring):
    s = unicode(s)
  return "'" + MySQLdb.escape_string(s) + "'"

def model_to_dict(instance):
  data = {}
  for field in instance._meta.fields:
    data[field.name] = field.value_from_object(instance)
  return data

def request_data(req):
  ''' Combine GET & POST dictionaries '''
  p = req.POST.dict()
  g = req.GET.dict()
  r = {}
  for k, v in g.iteritems():
    r[k] = v
  for k, v in p.iteritems():
    r[k] = v
  if 'data' in r:
    r = json.loads(r['data'])
  return r

def model_fields(model, r):  
  opts = model._meta
  model_data = {}
  for f in model._meta.fields:
    if f.name in r:
      model_data[f.name] = r[f.name]  
  return model_data
