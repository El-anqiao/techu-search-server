from __future__ import unicode_literals
from generic import *
import time
import marshal
from hashlib import sha1

class FunctionCache(object):
  '''
  |  Creates a key with the function name and a hash of the arguments.
  |  Parameter values (or keyword argument parameter values) **must be serializable**.
  |  Used as a view decorator.
  '''
  __cache = None
  def __init__(self, fn):
    self.fn = fn
    self.__cache = Cache()

  def __call__(self, *args, **kwargs):
    if settings.FUNCTION_CACHE and not (len(args) > 0 and 'c' in args[0].REQUEST and args[0].REQUEST['c'] == '0'):
      cache_key = json.dumps(args, cls=Serializer) + json.dumps(kwargs, cls=Serializer)
      cache_key = cache_key.encode('utf-8')
      cache_key = self.fn.__name__ + ':' + sha1(cache_key).hexdigest()
      ''' check if function result is cached '''
      result = self.__cache.get(cache_key)
      if result:
        return result
      else:
        result = self.fn(*args, **kwargs)
        self.__cache.set(cache_key, result)
      return result
    else:
      return self.fn(*args, **kwargs)

class Cache(object):
  '''
  |  Caching wrapper around Redis client.
  |  Supports setting keys with *WATCH* as a CAS device along with expiration.
  |  Also supports hash (dictionary) operations, handles invalidations and marks indexes as "dirty".
  '''
  __R = None

  def __init__(self):
    self.__R = redis_client()
  
  def delete(self, keys, expires = 500):
    ''' 
    |  Set key expiration at specified time in milliseconds.
    |  Allows *soft* deletion by setting low expiration times.
    |  If you set the *expires* parameter to 0 an immediate delete is performed (via the *DELETE* command)
    '''
    if isinstance(keys, basestring):
      keys = [keys]
    p = self.transaction()
    for key in keys:
      try:
        if expires == 0:
          p.delete(key)
        else:
          p.pexpire(key, expires)
      except:
        return False
    try:
      p.execute()
    except:
      return False
    return True

  def exists(self, key):
    '''
    Check if a key exists in Redis
    '''
    return self.__R.exists(key)

  def hget(self, key):
    '''
    Return all entries in a Redis hash structure as a dict
    '''
    return self.__R.hgetall(key)

  def get(self, key, unserialize = True):
    '''
    Return a value from Redis.
    Optionally transforms result ( when *unserialize* parameter is True - default ) through `marshal.loads <http://docs.python.org/2/library/marshal.html#marshal.loads>`_
    '''
    value = self.__R.get(key)
    if value is None:
      return None
    if unserialize:
      return marshal.loads(value)
    else:
      return value

  def hset(self, key, inner_key, value, watch = False, expire = 0., lock = None):
    '''
    Set a hash entry in the structure specified by *key* and hash key *inner_key*
    '''
    r = None
    try:
      p = self.transaction()
      p.hset(key, inner_key, value)
      if watch:
        p.watch(key)
      r = p.execute()
    except:
      r = False
    return r

  def set(self, key, value, watch = False, expire = 0., lock = None, keylist = None):
    ''' 
    |  Store a key-value pair in Redis.
    |  Optionally add *WATCH* for implementing CAS.
    |  Supports also key-lock releasing in case cache locks are implemented (avoiding stampeding herd).
    |  *expire* parameter is in seconds but of float type, multiplied by 10**3 and passed to *PEXPIRE* command
    '''
    try:
      cache_time = int(time.time() * 10**6)
      value = marshal.dumps(value)
      p = self.transaction()      
      if watch:
        p.watch(key)
      p.set(key, value)
      if not keylist is None:
        p.rpush(keylist, key)
      if expire > 0:
        p.pexpire(key, int(expire * 10**3))
      if not lock is None:
        p.delete(lock)
      p.execute()
      return True
    except:
      return False

  def invalidate(self, index_id, version):
    '''
    Invalidate cache entries
    '''
    version_pattern = '*:%d:%s' % (index_id, version)
    p = self.transaction()
    self.delete( self.__R.keys(version_pattern) )
  
  def version(self, index_id):
    '''
    Index version
    '''
    index_key = 'version:%d' % (index_id,)
    version = self.get(index_key, False)
    if version is None:
      return 1
    else:
      return int(version)
  
  def transaction(self):
    '''
    Start a consistent & isolated operation (transaction)
    '''
    return self.__R.pipeline()

  def dirty(self, index_id, action = ''):
    '''
    |  Mark an index as "dirty" thus containing changes that 
    |  require cache entries concerning that index to be invalidated.
    |  Specific actions will give finer control over invalidations in the future.
    '''
    modification_time = int(time.time() * 10**6)
    index_key = 'version:%s' % (str(index_id),)
    old_version = self.__R.get(index_key)
    p = self.transaction()
    p.watch(index_key)
    p.set(index_key, modification_time)
    try:
      p.execute()
      self.invalidate(index_id, old_version)
    except redis.WatchError as e:
      pass
    return True

