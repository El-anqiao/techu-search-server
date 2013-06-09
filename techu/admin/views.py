from techu.libraries.generic import *
from django.shortcuts import render
from django.http import HttpResponse
from techu.models import *
import requests

def home(request):
  params = { 'content' : '<h1>Dashboard</h1>' }
  return render(request, 'dashboard.html', params)


def api_playground(request, request_type = ''):
  params = { 'request_type' : request_type }
  return render(request, 'api-playground.html', params)

def fetch_api(request):
  url = request.POST['url']
  data = request.POST['data']  
  r = requests.post(url, data = data)
  r.encoding = 'utf-8'
  response = HttpResponse()
  response.content = r.content
  response.status_code = 200

