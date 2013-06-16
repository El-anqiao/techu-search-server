from techu.libraries.generic import *
from django.shortcuts import render
from django.http import HttpResponse
from techu.models import *
import requests
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def highlighter(request):
  code = request.REQUEST['code']
  if not 'lang' in request.REQUEST:
    language = 'json'
  else:
    language = request.REQUEST['lang']
  lexer = get_lexer_by_name(language)
  formatter = HtmlFormatter(linenos = False)
  result = highlight(code, lexer, formatter)
  return R({ 'code' : result })

def home(request):
  params = { 'content' : '<h1>Dashboard</h1>' }
  params['json_data'] = configurations()
  params['url'] = request.get_full_path()
  return render(request, 'dashboard.html', params)

def configurations():
  data = {
    'configurations'        : json.dumps(Configuration.objects.all().order_by('name'), cls=Serializer),
    'indexes'               : json.dumps(Index.objects.all().order_by('name'), cls=Serializer),
    'searchd'               : json.dumps(Searchd.objects.all(), cls=Serializer),
    'configuration_index'   : json.dumps(ConfigurationIndex.objects.all(), cls=Serializer),
    'configuration_searchd' : json.dumps(ConfigurationSearchd.objects.all(), cls=Serializer),
    'index_options'         : json.dumps(IndexOption.objects.all(), cls=Serializer),
    'searchd_options'       : json.dumps(SearchdOption.objects.all(), cls=Serializer),
    'options'               : json.dumps(Option.objects.all().order_by('name'), cls=Serializer),
  }
  return ";\n".join([ k + ' = ' + data[k] for k in data.keys() ])

def api_playground(request, request_type = ''):
  base_url = 'https://techu'
  params = { 
    'request_type' : request_type,
    'url'          : base_url + '/' + request_type,    
    'data'         : {}
    }
  if request_type == '':
    params['data']['pretty'] = 1
    api_response = fetch_url(params['url'], params['data']) 
    params['api_response'] = api_response
  params['json_data'] = configurations()
  params['url'] = request.get_full_path()
  return render(request, 'api-playground.html', params)

def fetch_url(url, data):
  r = requests.post(url, data = data, verify = False)
  r.encoding = 'utf-8'
  return r.content

def fetch_api(request):
  data = {}
  url = request.POST['url']
  if 'pretty' in request.POST and request.POST['pretty'] == '1':
    data['pretty'] = 1
  else:
    data['pretty'] = 0
  return R(fetch_url(url, data), request, serialize=False)
