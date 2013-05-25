from generic import *
import time
import marshal

class Cache:
  R = None

  def __init__(self):
    self.R = redis26()
  
  def __delete(self, keys, expires = 500):
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

  def get(self, key, unserialize = True):
    if unserialize:
      return marshal.loads(self.R.get(key))
    else:
      return self.R.get(key)

  def set(self, key, value, watch = False, expire = 0., lock = None, keylist = None):
    ''' expire parameter is float -> multiplied by 10**3 and passed to pexpire '''
    try:
      cache_time = int(time.time() * 10**6)
      marshal.dumps(value)
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
    self.__delete( self.R.keys(version_pattern) )
  
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

