from generic import *
import time
import marshal

class Cache:
  R = None

  def __init__(self):
    self.R = redis26()
  
  def delete(self, keys, expires = 500):
    ''' Set key expiration at specified time in milliseconds  '''
    if isinstance(keys, basestring):
      keys = [keys]
    p = self.R.pipeline()
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
    return self.R.exists(key)

  def hget(self, key):
    return self.R.hgetall(key)

  def get(self, key, unserialize = True):
    value = self.R.get(key)
    if value is None:
      return None
    if unserialize:
      return marshal.loads(value)
    else:
      return value

  def hset(self, key, inner_key, value, watch = False, expire = 0., lock = None):
    r = None
    try:
      p = self.R.pipeline()
      p.hset(key, inner_key, value)
      if watch:
        p.watch(key)
      r = p.execute()
    except:
      r = False
    return r

  def set(self, key, value, watch = False, expire = 0., lock = None, keylist = None):
    ''' expire parameter is float -> multiplied by 10**3 and passed to pexpire '''
    try:
      cache_time = int(time.time() * 10**6)
      value = marshal.dumps(value)
      p = self.R.pipeline()      
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
    version_pattern = '*:%d:%s' % (index_id, version)
    p = self.R.pipeline()
    self.delete( self.R.keys(version_pattern) )
  
  def version(self, index_id):
    index_key = 'version:%d' % (index_id,)
    return self.get(index_key, False)
   
  def dirty(self, index_id, action):
    modification_time = int(time.time() * 10**6)
    index_key = 'version:%d' % (index_id,)
    old_version = self.R.get(index_key)
    p = self.R.pipeline()
    p.watch(index_key)
    p.set(index_key, modification_time)
    try:
      p.execute()
      self.invalidate(index_id, old_version)
    except redis.WatchError as e:
      pass
    return True
    ''' specific actions will give finer control over invalidations in the future '''

