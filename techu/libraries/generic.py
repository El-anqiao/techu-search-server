import os, imp
import MySQLdb
import re, json
import redis
settings_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1])
settings = imp.load_source('settings', os.path.join( settings_path,  'settings.py'))

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
