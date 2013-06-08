from techu.libraries.generic import *
from django.shortcuts import render
from django.http import HttpResponse
from techu.models import *

def home(request):
  params = { 'content' : '<h1>Dashboard</h1>' }
  return render(request, 'h5bp/base.html', params)

