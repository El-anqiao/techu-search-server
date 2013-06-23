#!/usr/bin/python
import imp, os, sys
import time, re 
import marshal
from generic import *
from django.db import transaction, connections
from django.db import IntegrityError, DatabaseError
from daemon import Daemon
from middleware import ConnectionMiddleware
import logging

class QueueDaemon(Daemon):
  '''
  |  Daemon script that applies queued operations to indexes
  
  *Notes*
  * Different instances should be spawned for each index
  '''
  Logger = None
  def fetch_indexes(self):
    '''
    Get all active realtime indexes.
    '''
    sql = '''SELECT i.id, i.name FROM sp_indexes i 
      JOIN sp_configuration_index sci ON i.id = sci.sp_index_id 
      WHERE sci.is_active AND i.index_type = 1'''
    c = connections['default'].cursor()
    c.execute(sql)
    indexes = {}
    for row in cursorfetchall(c):
      indexes[row['id']] = row['name']
    return indexes

  def run(self):
    '''
    **UNDER DEVELOPMENT**
    The actual code for applying operations.
    '''
    sys.stdout.write("Applier daemon started ...\n" )
    sys.stdout.flush()
    indexes = self.fetch_indexes()
    r = redis_client()
    replace = re.compile(r'^INSERT\s+')
    while(True):
      for index_id, index in indexes.iteritems():
        m = connections['sphinx:' + str(index_id)].cursor()
        keys = r.lrange('queue:' + str(index_id), 0, -1)
        if keys:
          for key in keys:
            data = r.get(key)
            data = marshal.loads(data) 
            self.Logger.info('Applying key ' + key)
            action = key.split(':')[0]
            try:
              m.executemany(data['sql'], data['values'])
            except IntegrityError as e:
              pass
            except DatabaseError as e:
              if action == 'insert':
                m.executemany(replace.sub('REPLACE ', data['sql']), data['values'])
              else:
                pass            
            p = r.pipeline()
            p.lpop('queue:' + str(index_id))
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
  ''' Move to settings.py '''
  LOGFORMAT = '%(asctime)s %(message)s' 
  DATEFORMAT = '%Y%m%d %H:%M:%S'
  PIDFILE = os.path.join( '/' . join(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-2]), 'sphinxqueue.pid')
  OUTFILE = os.path.join(os.path.dirname(PIDFILE), 'sphinxqueue.out')
  LOGFILE = os.path.join(os.path.dirname(PIDFILE), 'sphinxqueue.log')
  queue = QueueDaemon(PIDFILE, stdout = OUTFILE)
  if action == 'start':
    logging.basicConfig(format = LOGFORMAT, filename = LOGFILE, datefmt = DATEFORMAT, level = logging.DEBUG)
    queue.Logger = logging.getLogger('Queue Applier')
    queue.start()
  elif action == 'status':
    queue.status()
  elif action == 'restart':
    queue.restart()
  elif action == 'stop':
    queue.stop()
