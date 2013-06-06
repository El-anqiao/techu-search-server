from generic import redis26
from generic import settings
from time import time

class Profiler(object):
  def __init__(self, fn):
    self.fn = fn

  def __call__(self, *args, **kwargs):
    if settings.PROFILER:
      r = redis26()
      r.incr('hits:' + self.fn.__name__)
      start_time = time()
      response = self.fn(*args, **kwargs)
      r.set('time:' + self.fn.__name__, time() - start_time)
      return response
    else:
      return self.fn(*args, **kwargs)

