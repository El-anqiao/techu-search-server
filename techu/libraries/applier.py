#!/usr/bin/python
import imp, os, sys
import time, redis, re 
from django.core.management import setup_environ
settings_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1])
settings = imp.load_source('settings', os.path.join( settings_path,  'settings.py'))
setup_environ(settings)
from django.db import transaction, connections
from django.db import IntegrityError, DatabaseError
from daemon import Daemon
from generic import *
import logging
from middleware import ConnectionMiddleware

class QueueDaemon(Daemon):
  '''
  *NOTES*
  - different instances should be spawned for each index
  '''
  Logger = None
  def fetch_indexes(self):
    sql = '''SELECT i.name FROM sp_indexes i 
      JOIN sp_configuration_index sci ON i.id = sci.sp_index_id 
      WHERE sci.is_active'''
    c = connections['default'].cursor()
    c.execute(sql)
    return [ row['name'] for row in cursorfetchall(c)]

  def run(self):
    sys.stdout.write("Applier daemon started ...\n" )
    sys.stdout.flush()
    indexes = self.fetch_indexes()
    r = redis.StrictRedis()
    replace = re.compile(r'^INSERT\s+')
    while(True):
      for index in indexes:
        m = connections['sphinx:' + index].cursor()
        keys = r.lrange('queue:' + index, 0, -1)
        if keys:
          for key in keys:
            sql = r.get(key)
            self.Logger.info('Applying key ' + key + '->' + sql.replace("\n", ' '))
            action = key.split(':')[0]
            try:
              m.execute(sql)
            except IntegrityError as e:
              pass
            except DatabaseError as e:
              if action == 'insert':
                m.execute(replace.sub('REPLACE ', sql))
              else:
                pass
            p = r.pipeline()
            p.lpop('queue:' + index)
            p.delete(key)
            p.hset(index + ':last-modified', action, int(time.time()*10**6))
            p.execute()
      time.sleep(0.001) #sleep for 1ms

if __name__ == '__main__':
  connection = ConnectionMiddleware()
  connection.process_request({})
  try:
    action = sys.argv[1].lower()
  except:
    action = 'start'
  queue = QueueDaemon('/var/run/sphinxqueue.pid', stdout = 'queue.out' )
  if action == 'start':
    logging.basicConfig(format = '%(asctime)s %(message)s', filename = 'sphinxqueue.log', datefmt = '%Y%m%d %H:%M:%S', level = logging.DEBUG)
    queue.Logger = logging.getLogger('Queue Applier')
    queue.start()
  elif action == 'status':
    queue.status()
  elif action == 'restart':
    queue.restart()
  elif action == 'stop':
    queue.stop()
