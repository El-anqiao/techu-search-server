import os, imp
import MySQLdb
import re, json, datetime
import redis
from django.core.management import setup_environ
settings_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1])
settings = imp.load_source('settings', os.path.join( settings_path,  'settings.py'))
setup_environ(settings)
from django.http import HttpResponse
from django.db import models
from time import mktime

modules = None
def _import(module_list):
  ''' 
  Dynamic imports may boost performance since functions require different packages 
  e.g. libraries.sphinxapi is only used for search and excerpts calls (needs some benchmarking)
  '''
  global modules
  for m in map(__import__, module_list):
    if not m in modules:
      modules.append(m)

def filter_list(r, fields):
  '''
  |  Filter conditions from a request and create an appropriate dictionary which is passed to *filter* as kwargs.
  |  Example:

  `filter_list(r, { 'name' : 'startswith', 'section' : None })`
  
  | Passing *None* will use *__exact* as an operator.
  '''
  conditions = {}
  for param, field in fields.iteritems():
    if param in r:
      if field is None:
        field = param + '__exact'
      else:
        field = param + '__' + field
      conditions[field] = r[param]
  return conditions

def is_queryset(o):
  '''
  Check if a variable is QuerySet. Returns Boolean.
  '''
  return isinstance(o, models.query.QuerySet)

def is_model(o):
  '''
  Check if a variable is instance of Model. Returns Boolean.
  '''
  return isinstance(o, models.Model)

def debug(r):
  '''
  Raise exception so that passes through the Exception logging middleware.
  '''
  indent = 4
  separators = (',', ': ')
  r = { 'debug' : r }
  raise Exception(json.dumps(r, cls=Serializer, indent = indent, separators = separators))

def is_queued(request):
  '''
  Check if a request requires operation queueing. Returns Boolean.
  '''
  if 'queue' in request.REQUEST:
    return ( int(request.REQUEST['queue']) == 1 )
  else:
    return False

class Serializer(json.JSONEncoder):
  ''' 
  JSON serializer for list, dict and QuerySet objects.
  '''
  def default(self, o):
    '''
    Default serializer method. Enables QuerySet & datetime support.
    '''
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
      return int( mktime(o.timetuple()) )
    return json.JSONEncoder.default(self, o)

def E(code = 500, **kwargs):
  '''
  Return an HttpResponse with error code. 
  '''
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
  |  Return a successful, normal HttpResponse (status code 200).   
  |  Serializes by default any object passed.
  |  Passing the GET/POST parameter *pretty=1* will result in pretty-printed output.
  '''
  if not request is None:
    if 'pretty' in request.REQUEST:
      kwargs['pretty'] = (request.REQUEST['pretty'].lower() in [ '1', 'true'])
  defaults = { 'code' : 200, 'serialize' : True, 'pretty' : False }
  kwargs = dict(defaults.items() + kwargs.items())
  if kwargs['pretty']:
    indent = 4
    separators = (',', ': ')
  else:
    indent = None
    separators = (',', ':')
  if kwargs['serialize']:
    data = json.dumps(data, cls=Serializer, indent = indent, separators = separators)
  r = HttpResponse(content = data, status = kwargs['code'], content_type = 'application/json;charset=utf-8')
  return r

def redis_client():
  '''
  Return a Redis 2.6 `client instance <https://github.com/andymccurdy/redis-py>`_
  '''
  return redis.StrictRedis(
                 host = settings.REDIS_HOST, 
                 port = settings.REDIS_PORT, 
                 password = settings.REDIS_PASSWORD)

def cursorfetchall(cursor):
  '''
  Returns all rows from a DB cursor as a dictionary 
  '''
  desc = cursor.description
  return [
      dict(zip([col[0] for col in desc], row))
      for row in cursor.fetchall()
  ]

def regex_check(s, r = r'[^a-zA-Z0-9\-_]+'):
  '''
  Regex check for ASCII letters & digits, dash & underscore
  '''
  return (re.match(r, s) is None)

def identq(s):
  '''
  Quote an SQL identifier.
  '''
  return '`' + s.replace('`', '') + '`'

def model_to_dict(instance, fields_only = []):
  '''
  |  Convert a model instance to dictionary.
  |  Use *fields_only* parameter to narrow down the returned field values.
  '''
  data = {}
  for field in instance._meta.fields:
    if fields_only and not field in fields_only:
      continue 
    data[field.name] = field.value_from_object(instance)
  return data

def request_data(req):
  ''' 
  |  Combine GET & POST dictionaries. POST has higher priority.
  |  If request contains *data* parameter then it is unserialized from JSON format and the result is returned.  
  '''
  p = req.POST.dict()
  g = req.GET.dict()
  r = dict(req.GET.dict().items() + req.POST.dict().items())
  if 'data' in r:
    try:
      r = json.loads(r['data'])
    except:
      pass
  return r

def model_fields(model, r):  
  '''
  |  Filter values from dictionary parameter *r* which are fields of the model parameter *model*.
  |  Returns dictionary with the model field values and fields as keys.
  '''
  opts = model._meta
  model_data = {}
  for f in model._meta.fields:
    if f.name in r:
      model_data[f.name] = r[f.name]  
  return model_data
