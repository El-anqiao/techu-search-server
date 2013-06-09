from techu.libraries.generic import *
from django.shortcuts import render
from django.http import HttpResponse
from techu.models import *
import requests

def home(request):
  params = { 'content' : '<h1>Dashboard</h1>' }
  return render(request, 'dashboard.html', params)


def api_playground(request, request_type = ''):
  base_url = 'https://techu'
  params = { 
    'request_type' : request_type,
    'url'          : base_url + '/' + request_type,    
    'data'         : {}
    }
  if request_type == '':
    api_response = fetch_url(params['url'], params['data']) 
    params['api_response'] = api_response
  return render(request, 'api-playground.html', params)

def fetch_url(url, data):
  r = requests.post(url, data = data, verify = False)
  r.encoding = 'utf-8'
  return r.content

def fetch_api(request):
  url = request.POST['url']
  if 'data' in request.POST:
    data = request.POST['data']  
  else:
    data = {}
  return R(json.loads(fetch_url(url, data)), request)
