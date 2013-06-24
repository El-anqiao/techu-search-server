# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys, time
import json, marshal
from hashlib import md5
import settings 
from django.db import connections, IntegrityError, DatabaseError
from libraries.generic import *
from techu.models import *
from libraries.sphinxapi import *
from libraries.caching import Cache, FunctionCache
from libraries.profiler import Profiler
from libraries.scripting import Scripting

@Scripting
@Profiler
def home(request):
  '''
  Home Page
  '''
  return R({ "Greetings-From" : "Techu Indexing Server" }, request)

@FunctionCache
def constants():
  '''
  |  Read all constants values from the database and associate via a 2-level dictionary
  |  1st level contains *name_of_table_name_of_field* keys and the 2nd level contains the constant value.
  '''
  constant_list = Constants.objects.all()  
  constants_hash = {}
  for c in constant_list:
    constant_key = c.table_name + '_' + c.table_field
    if not constant_key in constants_hash:
      constants_hash[constant_key] = {}
    constants_hash[constant_key][c.constant_value] = c.constant_name  
  return constants_hash

@Profiler
def option_list(request):
  ''' 
  |  Return a list of all available configuration options.
  |  Accepts the *data* parameter with a JSON object containing:

  1. *section* [1, 2, 3, 4] (see *constants* table for value meaning)
  2. *name* filter options by matching the start of their name with this value

  |  Example call:
  |  `curl -k --compressed 'https://techu/option/list/?pretty=1' --data-urlencode data='{ "section" : 4, "name" : "sql_attr" }'
  |  Returns all options belonging to datasources starting with "sql_attr".
  '''
  r = request_data(request)
  constant_list = constants()['sp_options_section']
  constant_list['0'] = '-'
  conditions = filter_list(r, { 'name' : 'startswith', 'section' : None })
  options = Option.objects.filter(**conditions).order_by('name')
  option_list = [ { 'id' : o.id, 'name' : o.name, 'section' : constant_list[unicode(o.section)] } for o in options ] 
  return R(option_list, request)

@Profiler
def option(request, section, section_instance_id):
  ''' 
  |  Connect options with searchd, indexes & sources and store their values.
  |  Receives a JSON object with the *data* parameter containing options (keys) and their values. 
  |  You can group parameters and assign values with a list.
  `curl -k --compressed 'https://techu/option/searchd/6/' --data-urlencode data='{
    "listen" : [ 
      "9312", 
      "9306:mysql41" 
      ], 
    "workers" : "threads", 
    "pid_file" : "/var/run/stackoverfow_searchd.pid", 
    "max_matches" : 1000 
  }'`
  '''
  section = section.lower()
  data = request_data(request)
  options = Option.objects.filter(name__in = data.keys())
  options_stored = []
  options_created = 0  
  options_found = 0
  for option in options:
    if not isinstance(data[option.name], list):
      values = [data[option.name]]
    else:
      values = data[option.name]
    for value in values:      
      value = unicode(value)
      value_hash = md5(value).hexdigest()
      if section == 'searchd':      
        o = SearchdOption.objects.get_or_create(
              sp_searchd_id = section_instance_id, 
              sp_option_id = option.id, 
              value = value,
              value_hash = value_hash)
      elif section == 'index':
        o = IndexOption.objects.get_or_create(
              sp_index_id = section_instance_id,
              sp_option_id = option.id,
              value = value,
              value_hash = value_hash)
      elif section == 'source':
        o = SourceOption.objects.get_or_create(
              sp_source_id = section_instance_id,
              sp_option_id = option.id,
              value = value,
              value_hash = value_hash)
      if o[1]:
        options_created += 1
      else:
        options_found += 1
      options_stored.append(o[0].id)
  if section == 'searchd':    
    options_stored = SearchdOption.objects.filter(id__in = options_stored)
  elif section == 'index':    
    options_stored = IndexOption.objects.filter(id__in = options_stored) 
  elif section == 'source':    
    options_stored = SourceOption.objects.filter(id__in = options_stored)
  options_stored = { 'created' : options_created, 'found' : options_found, 'options' : options_stored }
  return R(options_stored, request)

@Profiler
def index(request, index_id = 0):
  ''' 
  |  Add or modify information for an index.
  |  It can be associated with a configuration entity with the *configuration_id* parameter.
  `curl -k --compressed 'https://techu/index/' --data-urlencode name='so_posts_rt' --data-urlencode configuration_id='25'`
  '''
  data = request_data(request)
  fields = model_fields(Index, data)
  ci = None
  if index_id == 0:
    try:
      index = Index.objects.create(**fields)
      if 'configuration_id' in r:
        ci = ConfigurationIndex.objects.create(sp_index_id = i.id, 
                                               sp_configuration_id = int(r['configuration_id']), 
                                               is_active = 1)
      index = Index.objects.filter(pk = i.id)
    except IntegrityError as e:
      index = Index.objects.filter(name = fields['name']).update(**fields)
      index = Index.objects.filter(pk = index.id)
  else:
    try:
      index = Index.objects.filter(pk = index_id)
    except:
      return E(message = 'Error while retrieving object with primary key "%d"' % index_id)
  return R({ 'index' : index, 'configurations' : ci }, request)

@Profiler
def index_list(request):
  ''' 
  Return a JSON Array with all indexes 
  '''
  return R(Index.objects.all(), request)

@Profiler
def configuration_list(request):
  ''' 
  Return a list of all configurations.
  '''
  return R(Configuration.objects.all(), request)

@Profiler
def searchd(request, searchd_id = 0):
  ''' 
  Store a new searchd 
  '''
  data = request_data(request)
  fields = model_fields(Searchd, data)
  if searchd_id > 0:
    s = Searchd.objects.filter(pk = searchd_id).update(**fields)
  else:
    s = Searchd.objects.create(**fields)
  cs = None
  if 'configuration_id' in r:
    cs = ConfigurationSearchd.objects.create(sp_configuration_id = int(r['configuration_id']), sp_searchd_id = searchd_id)
  return R({ 'searchd' : s, 'configurations' : cs }, request)

@Profiler
def configuration(request, configuration_id = 0):
  ''' 
  Get or update information for a configuration 
  '''
  data = request_data(request)
  fields = model_fields(Configuration, data)
  if configuration_id > 0:
    configuration = Configuration.objects.get(pk = conf_id)
  else:
    if not regex_check(r['name']):
      return E(message = 'Illegal configuration name "%s"' % r['name'])
    try:
      c = Configuration.objects.create(**fields)
      c.hash = md5(str(c.id) + c.name).hexdigest()
      c.save(update_fields = ['hash'])
      configuration = Configuration.objects.filter(pk = c.id)
    except Exception as e:
      return E(message = str(e))
    except IntegrityError as e:
      return E('IntegrityError: ' + str(e))
  return R(configuration, request)

@Profiler
def batch_indexer(request, action, index_id):
  '''
  Bulk indexing 
  '''
  action = action.lower()
  data = request_data(request)
  queue = is_queued(request)  
  if not isinstance(data, list):
    data = [ data ]
  responses = []
  if action == 'insert':
    values = []
    fields = data[0].keys()
    for document in data:
      values.append(document.values())
    responses.append( insert(index_id, fields, values, queue) )
  elif action == 'update':
    fields = data[0].keys()
    fields.remove('id')
    for document in data:
      responses.append( update(index_id, document['id'], fields, [ document[field] for field in fields ], queue) )
  elif action == 'delete':
    for document in data:
      responses.append(delete(index_id, document['id'], queue))
  else:
    return E(message = 'Unknown action. Valid types are [ insert, update, delete ]')
  return R(responses)    

@Profiler
def indexer(request, action, index_id, doc_id = 0):
  ''' Add, delete, update documents '''
  action = action.lower()
  data = request_data(request)
  if 'id' in data and doc_id == 0:
    doc_id = int(data['id'])
  queue = is_queued(request)  
  if action == 'insert':
    response = insert(index_id, data.keys(), [ data.values() ], queue)
  elif action == 'update':
    response = update(index_id, doc_id, data.keys(), data.values(), queue) 
  elif action == 'delete':
    response = delete(index_id, doc_id, queue) 
  else:
    return E(message = 'Unknown action. Valid types are [ insert, update, delete ]')
  return R(response)

def insert(index_id, fields, values, queue = True):
  ''' 
  Build INSERT statement. 
  Supports multiple VALUES sets for batch inserts.
  '''
  index = fetch_index_name(index_id)
  sql  = "INSERT INTO %s(%s) VALUES" % (index, ',' . join(fields))
  sql += '(' + ','.join([ '%s' for v in values[0] ]) + ')'
  return modify_index(index_id, sql, queue, values)

def delete(index_id, doc_id, queue = True):
  ''' Build DELETE statement '''
  index = fetch_index_name(index_id)
  sql = 'DELETE FROM ' + identq(index) + ' WHERE id = %d' % (int(doc_id),)
  return modify_index(index_id, sql, queue)

def update(index_id, doc_id, fields, values, queue = True):
  ''' Build UPDATE statement '''
  index = fetch_index_name(index_id)
  sql = 'UPDATE %s SET ' % (identq(index),)
  for n, v in enumerate(values):
    sql += fields[n] + ' = %s,'
  sql = sql.rstrip(',') + ' WHERE id = ' + str(int(doc_id))
  return modify_index(index_id, sql, queue, values)

def modify_index(index_id, sql, queue, values = None, retries = 0):
  ''' 
  Either adds to index directly or queues statements 
  for async execution by storing them in Redis 
  If either Redis or searchd is unresponsive MAX_RETRIES attempts will be performed 
  in order to store the request to the alternative
  '''
  if retries > settings.MAX_RETRIES: 
    return E(message = 'Maximum retries %d exceeded' % retries)
  queue_action = None
  if sql.find('INSERT') == 0:
    queue_action = 'insert'
  elif sql.find('UPDATE') == 0:
    queue_action = 'update'
  elif sql.find('DELETE') == 0:
    queue_action = 'delete'
  response = None
  cache = Cache()
  if not queue:
    try:
      c = connections['sphinx:' + str(index_id)]
      cursor = c.cursor()
      if queue_action == 'delete':
        cursor.execute( sql )
      elif queue_action == 'update':
        cursor.execute(sql, values)
      elif queue_action == 'insert':
        cursor.executemany(sql, values)
      cache.dirty(index_id)
      response = { 'searchd' : 'ok' }
    except Exception as e:
      return str(e)
      response = modify_index(index_id, sql, True, values, retries + 1)
  else:
    try:
      rkey = rqueue(queue_action, index_id, sql, values)
      response = { 'redis' : rkey }
    except Exception as e:
      response = modify_index(index_id, sql, False, values, retries + 1)
  return response

@Profiler
def fetch_index_name(index_id):
  ''' Fetch index name by id '''
  try:
    c = Cache()
    if not c.exists('structures:indexes'):
      for index in Index.objects.all():
        if index_id == index.id:
          index_name = index.name
        c.hset('structures:indexes', str(index.id), index.name, True)
    else:
      indexes = c.hget('structures:indexes')
      index_id = str(index_id)
      if index_id in indexes:
        index_name = indexes[index_id]
      else:
        return E(message = 'No such index')
    return index_name
  except Exception as e:
    return E(message = 'Error while retrieving index')

def rqueue(queue, index_id, sql, values):
  '''
  Redis queue for incoming requests
  Applier daemon continuously reads from this queue 
  and executes asynchronously 
  TODO: check if it works better with Pub/Sub
  '''
  r = redis_client()
  c = r.incr(settings.TECHU_COUNTER)
  request_time = int(time.time()*10**6)
  key = ':' . join(map(str, [ queue, index_id, request_time, c ]))
  if queue == 'delete':
    data = { 'sql' : sql, 'values' : [] }
  else:
    data = { 'sql' : sql, 'values' : values }
  ''' marshal serialization is much faster than JSON '''
  data = marshal.dumps(data)
  ''' Transaction '''
  p = r.pipeline()
  p.rpush('queue:' + str(index_id), key)
  p.set(key, data)
  p.execute()
  return key

@Scripting
@Profiler
def search(request, index_id):
  cache = Cache()
  index = fetch_index_name(index_id)
  ''' Search wrapper with SphinxQL '''
  r = request_data(request)
  if settings.SEARCH_CACHE:
    cache_key = md5(index + request.REQUEST['data']).hexdigest()
    lock_key = 'lock:' + cache_key
    version = cache.version(index_id)
    cache_key = 'cache:search:%s:%d:%s' % (cache_key, index_id, version)
    try:   
      response = cache.get(cache_key) 
      if not response is None:
        return R(response, 200, False)
      else:
        ''' lock this key for re-caching '''
        start = time.time()
        lock = cache.get(lock_key)
        while ( not lock is None ):
          lock = cache.get(lock_key)
          if (time.time() - start) > settings.CACHE_LOCK_TIMEOUT:
            return E(message = 'Cache lock wait timeout exceeded')
        ''' check if key now exists in cache '''
        response = cache.get(cache_key)
        if not response is None:
          return R(response, 200, False)
        ''' otherwise acquire lock for this session '''
        cache.set(lock_key, 1, True, settings.CACHE_LOCK_TIMEOUT) # expire in 10sec        
    except:
      pass    
  
  option_mapping = {
    'mode' : {
        'extended' : SPH_MATCH_EXTENDED2,
        'boolean'  : SPH_MATCH_BOOLEAN,
        'all'      : SPH_MATCH_ALL,
        'phrase'   : SPH_MATCH_PHRASE,
        'fullscan' : SPH_MATCH_FULLSCAN,
        'any'      : SPH_MATCH_ANY,
      }
  }
  options = {
      'sortby'      : '',
      'mode'        : 'extended',
      'groupby'     : '',
      'groupsort'   : '',
      'offset'      : 0,
      'limit'       : 1000,
      'max_matches' : 0,
      'cutoff'      : 0,
      'fields'      : '*',
    }
  
  sphinxql_list_options = {
    'ranker' : [ 'proximity_bm25', 'bm25', 'none', 'wordcount', 'proximity',
                 'matchany', 'fieldmask', 'sph04', 'expr', 'export' ],
    'idf' : [ 'normalized', 'plain'],
    'sort_method'  : ['pq', 'kbuffer' ]
  }
  sphinxql_options = { 
    'agent_query_timeout' : 10000,
    'boolean_simplify' : 0,
    'comment' : '',
    'cutoff'  : 0,
    'field_weights' : '',
    'global_idf' : '',
    'idf' : 'normalized',
    'index_weights'  : '',
    'max_matches' : 10000,
    'max_query_time' : 10000,
    'ranker' : 'proximity_bm25',
    'retry_count' : 2,
    'retry_delay' : 100,
    'reverse_scan' : 0,
    'sort_method'  : 'pq'
  }
  order_direction = {
    '-1'   : 'DESC',
    'DESC' : 'DESC',
    '1'    : 'ASC',
    'ASC'  : 'ASC',
  }

  try:
    ''' Check attributes from request with stored options (sp_index_option) '''
    ''' Preload host and ports per index '''
    '''
    SELECT
    select_expr [, select_expr ...]
    FROM index [, index2 ...]
    [WHERE where_condition]
    [GROUP BY {col_name | expr_alias}]
    [WITHIN GROUP ORDER BY {col_name | expr_alias} {ASC | DESC}]
    [ORDER BY {col_name | expr_alias} {ASC | DESC} [, ...]]
    [LIMIT [offset,] row_count]
    [OPTION opt_name = opt_value [, ...]]
    '''
    sql_sequence = [ ('SELECT', 'fields'), ('FROM', 'indexes'), ('WHERE', 'where'), 
                     ('GROUP BY', 'group_by'), ('WITHIN GROUP ORDER BY', 'order_within_group'), 
                     ('ORDER BY', 'order_by'), ('LIMIT', 'limit'), ('OPTION', 'option') ]
    sql = {}
    for sql_clause, key in sql_sequence:
      sql[key] = ''
      if not key in r:
        r[key] = ''
    sql['indexes'] = index + ','.join( r['indexes'] )
    if isinstance(r['fields'], list):
      sql['fields'] = ',' . join(r['fields'])
    else:
      sql['fields'] = options['fields']
    if r['group_by'] != '':
      sql['group_by'] = r['groupby']
    if not isinstance(r['limit'], dict):
      r['limit'] = { 'offset' : '0', 'count' : options['limit'] }
    r['limit'] = '%(offset)s, %(count)s' % r['limit']
    sql['order_by'] = ',' . join([ '%s %s' % (order[0], order_direction(order[1].upper())) for order in r['order_by'] ])
    if r['order_within_group'] != '':
      sql['order_within_group'] = ',' . join([ '%s %s' % (order[0], order_direction(order[1].upper())) for order in r['order_within_group'] ])
    sql['where'] = [] #dictionary e.g. { 'date_from' : [[ '>' , 13445454350] ] } 
    value_list = []
    if isinstance(r['where'], dict):
      for field, conditions in r['where'].iteritems():
        for condition in conditions:
          operator, value = condition
          value_list.append(value)
          sql['where'].append('%s%s%%s' % (field, operator,))
    value_list.append(r['q'])
    sql['where'].append('MATCH(%%s)')
    sql['where'] = ' ' . join(sql['where'])
    if isinstance(r['option'], dict):
      sql['option'] = []
      for option_name, option_value in r['option'].iteritems():
        if isinstance(option_value, dict): 
          option_value = '(' + (','. join([ '%s = %s' % (k, option_value[k]) for k in option_value.keys() ])) + ')'
          sql['option'].append('%s = %s' % (option_name, option_value))
      sql['option'] = ',' . join(sql['option'])
    response = { 'results' : None, 'meta' : None }
    try:    
      cursor = connections['sphinx:' + index].cursor()
      sql =  ' ' . join([ clause[0] + ' ' + sql[clause[1]] for clause in sql_sequence if sql[clause[1]] != '' ]) 
      cursor.execute(sql, value_list)
      response['results'] = cursorfetchall(cursor)
    except Exception as e:
      error_message = 'Sphinx Search Query failed with error "%s"' % str(e)
      return E(message = error_message)
    try:
      cursor.execute('SHOW META')
      response['meta'] = cursorfetchall(cursor)
    except:
      pass
    if settings.SEARCH_CACHE:
      cache.set(cache_key, response, True, SEARCH_CACHE_EXPIRE, lock_key)
  except Exception as e:
    return E(message = str(e))
  return R(response)

@Scripting
@Profiler
def excerpts(request, index_id):
  cache = Cache()
  ''' 
  Returns highlighted snippets 
  Caches responses in Redis
  '''
  index_id = int(index_id)
  index = fetch_index_name(index_id)
  r = request_data(request)
  cache_key = md5(index + json.dumps(r)).hexdigest()
  lock_key = 'lock:' + cache_key
  version = cache.version(index_id)
  cache_key = 'cache:excerpts:%s:%d:%s' % (cache_key, index_id, version)
  if not 'docs' in r:
    return R({})
  if settings.EXCERPTS_CACHE:
    try:   
      response = cache.get(cache_key) 
      if not response is None:
        return R(response, request, code = 200, serialize = False) 
      ''' lock this key for re-caching '''
      start = time.time()
      lock = cache.get(lock_key)
      while ( not lock is None ):
        lock = cache.get(lock_key)
        if (time.time() - start) > settings.CACHE_LOCK_TIMEOUT:
          return E(message = 'Cache lock wait timeout exceeded')
      ''' check if key now exists in cache '''
      response = cache.get(cache_key)
      if not response is None:
        return R(response, request, code = 200, serialize = False)
      ''' otherwise acquire lock for this session '''
      cache.set(lock_key, 1, True, settings.CACHE_LOCK_TIMEOUT) # expire in 10sec         
    except:
      return E(message = 'Error while examining excerpts cache')    

  options = {
      "before_match"      : '<b>',
      "after_match"       : '</b>',
      "chunk_separator"   : '...',
      "limit"             : 256,
      "around"            : 5,    
      "exact_phrase"      : False,
      "use_boundaries"    : False,
      "query_mode"        : True,
      "weight_order"      : False,
      "force_all_words"   : False,
      "limit_passages"    : 0,
      "limit_words"       : 0,
      "start_passage_id"  : 1,
      "html_strip_mode"   : 'index',
      "allow_empty"       : False,
      "passage_boundary"  : 'paragraph',
      "emit_zones"        : False
  }
  for k, v in options.iteritems():
    if k in r:
      if isinstance(v, int):
        options[k] = int(r[k])
      elif isinstance(v, bool):
        options[k] = bool(r[k])
      else:
        options[k] = r[k]
  if 'ttl' in r:      
    cache_expiration = int(r['ttl'])
  else:
    cache_expiration = settings.EXCERPTS_CACHE_EXPIRE
  if isinstance(r['docs'], dict):
    document_ids = r['docs'].keys()
    documents = r['docs'].values()
  elif isinstance(r['docs'], list):
    document_ids = range(len(r['docs'])) # get a list of numeric indexes from the list
    documents = r['docs']
  else:
    return E(message = 'Documents are passed as a list or dictionary structure')
  del r['docs'] # free up some memory
  '''
  docs = { 838393 : 'a document with lots of text', 119996 : 'another document with text' }
  '''
  ci = ConfigurationIndex.objects.filter(sp_index_id = index_id)[0]
  searchd_id = ConfigurationSearchd.objects.filter(sp_configuration_id = ci.sp_configuration_id)[0].sp_searchd_id
  ''' TODO: convert hard coded option ids to constants '''
  so = SearchdOption.objects.filter(sp_searchd_id = searchd_id, sp_option_id = 138,).exclude(value__endswith = ':mysql41')
  sphinx_port = int(so[0].value)
  try:
    so = SearchdOption.objects.filter(sp_searchd_id = searchd_id, sp_option_id = 188,)
    if so:
      sphinx_host = so[0].value
    else:
      sphinx_host = 'localhost'
  except:
    sphinx_host = 'localhost'
  try:
    cl = SphinxClient()
    cl.SetServer(host = sphinx_host, port = sphinx_port)
    excerpts = cl.BuildExcerpts( documents, index, r['q'], options )
    del documents
    if not excerpts:
      return E(message = 'Sphinx Excerpts Error: ' + cl.GetLastError())
    else:      
      if settings.EXCERPTS_CACHE:
        cache.set(cache_key, excerpts, True, cache_expiration, lock_key)
      excerpts = { 
        'excerpts' : dict(zip(document_ids, excerpts)), 
        'cache-key' : cache_key,        
        }
      return R(json.dumps(excerpts), request)
  except Exception as e:
    return E(message = 'Error while building excerpts ' + str(e))

@Profiler
def generate(request, configuration_id):
  import codecs
  ''' 
  |  Generate configuration file and restart searchd instances. 
  |  Response contains a dictionary with the configuration file contents, 
  |  the stop/start commands and the current status.
  
  **Parameters**
  *dryrun*
      |  Whether to store/overwrite the generated configuration and restart searchd.
      |  Useful in cases when you want to inspect a configuration file.
      |  Values [0,1]

      Example:
      `curl -k 'https://techu/generate/25/?pretty=1' --data-urlencode data='{ "dryrun" : 1 }'`
  '''
  r = request_data(request)
  searchd_start = 'searchd --config %(config)s %(switches)s'
  searchd_stop  = 'searchd --config %(config)s --stopwait'
  params = {}
  params['switches'] = ' '.join([ '--iostats', '--cpustats' ])
  c = Configuration.objects.get(pk = configuration_id)
  params['config'] = os.path.join(settings.PROJECT_ROOT, settings.SPHINX_CONFIGURATION_DIR, c.name) + '.conf'
  ci = ConfigurationIndex.objects.filter(sp_configuration_id = configuration_id).exclude(is_active = 0)
  si = ConfigurationSearchd.objects.filter(sp_configuration_id = configuration_id)
  searchd_options = SearchdOption.objects.filter(sp_searchd_id = si[0].sp_searchd_id)
  option_list = [ option.sp_option_id for option in searchd_options ]  
  indexes = Index.objects.filter(id__in = [ index.sp_index_id for index in ci ]).exclude(is_active = 0)
  parent_indexes = Index.objects.filter(id__in = [ index.parent_id for index in indexes ])
  index_options = IndexOption.objects.filter(sp_index_id__in = [ index.id for index in indexes ] + [index.id for index in parent_indexes ] )
  option_list += [ option.sp_option_id for option in index_options ]
  options = Option.objects.filter(id__in = option_list).values()
  option_names = {}
  for o in options:
    option_names[o['id']] = o['name']
  configuration = []
  for index in indexes:
    parent_name = ''
    if index.parent_id > 0:
      for pi in parent_indexes:
        if pi.id == index.parent_id:
          parent_name = ':' + pi.name
    index_name = index.name + parent_name
    configuration.append('index ' + index_name + ' {')
    for option in index_options:
      if option.sp_index_id == index.parent_id:
        configuration.append('  %s = %s' % ( unicode(option_names[option.sp_option_id]).ljust(30), unicode(option.value)))
      if option.sp_index_id == index.id:
        configuration.append('  %s = %s' % ( unicode(option_names[option.sp_option_id]).ljust(30), unicode(option.value)))
    configuration.append('}')  
  configuration.append('searchd {')
  for option in searchd_options:    
    configuration.append('  %s = %s' % ( unicode(option_names[option.sp_option_id].ljust(30)), unicode(option.value)))
  configuration.append('}')
  configuration.append("")
  configuration = "\n" . join(configuration)
  if 'dryrun' in r and int(r['dryrun']) != 1:
    f = codecs.open(params['config'], mode = 'w', encoding = 'utf-8')
    f.write(configuration)
    f.close()
    try:
      stopped = os.system(searchd_stop % params)
      started = os.system(searchd_start % params)
    except Exception as e:
      return E(message = 'Error while restarting searchd ' + str(e))
  else:
    stopped = 1
    started = 1
  response = { 
    'configuration' : configuration, 
    'stopped' : { 'command' : searchd_stop % params,  'status' : not bool(stopped) }, 
    'started' : { 'command' : searchd_start % params, 'status' : not bool(started) },
    }
  return R(response, request)

