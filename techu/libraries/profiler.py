from generic import redis_client
from generic import settings
from time import time

class Profiler(object):
  '''
  |  Simple Profiling. Stores number of requests and total time for a function.
  |  Used as a view decorator. Can be disabled by setting `PROFILER = False` in *settings.py*.
  '''
  def __init__(self, fn):
    self.fn = fn

  def __call__(self, *args, **kwargs):
    if settings.PROFILER:
      r = redis_client()
      r.incr('hits:' + self.fn.__name__)
      start_time = time()
      response = self.fn(*args, **kwargs)
      r.set('time:' + self.fn.__name__, time() - start_time)
      return response
    else:
      return self.fn(*args, **kwargs)

