#!/usr/bin/python
import sys
sys.path.append('../../../')
from django.core.management import setup_environ
from techu import settings
setup_environ(settings)
from techu.models import Authentication
from time import time
import hashlib
from random import choice
from string import digits, ascii_letters
import hmac 

class Auth(object):
  token_salt   = ''
  consumer_key = ''
  secret       = ''

  def __init__(self, consumer_key = ''):
    self.token_salt = str(time())
    self.consumer_key = consumer_key

  def get_secret(self):
    if self.consumer_key == '': 
      return True
    auth = Authentication.objects.filter(consumer_key=self.consumer_key)
    if not auth:
      return False
    else:
      return auth[0].secret

  def update_secret(self, old_secret):
    if self.consumer_key != '':
      auth = Authentication.objects.filter(consumer_key = self.consumer_key, secret = old_secret)
      if not auth:
        return False
      else:
        auth.secret = self.generate_secret()
        auth.save()
        return auth.secret
    return False

  def randomize(self, length, elements = None):
    if elements is None:
      elements = ascii_letters + digits
    return ''.join([ choice(elements) for n in range(length) ])

  def generate_secret(self):
    return self.randomize(16, hashlib.sha1(self.token_salt + self.randomize(20)).hexdigest())
    
  def generate(self):
    ''' Generates consumer_key & secret pair '''
    self.consumer_key = ''
    while self.get_secret():
      self.consumer_key = self.randomize(8)
    self.secret = self.generate_secret()
    Authentication.objects.create(consumer_key = self.consumer_key, secret = self.secret)
   
  def verify(self, token):
    h = hmac.new(str(self.get_secret()), str(self.consumer_key), hashlib.sha1)
    print h.hexdigest()
    return ( h.hexdigest() == token )
  
  def __str__(self):
    return self.consumer_key + ' ' + self.secret

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append('test')
  if sys.argv[1] == 'test':
    ''' test pair -> NBA1e4Ah 1e7fc2c4a1d5d7d1 '''
    test_consumer = 'NBA1e4Ah'
    test_secret = '1e7fc2c4a1d5d7d1'
    auth = Auth(test_consumer)
    token = hmac.new(test_secret, test_consumer, hashlib.sha1).hexdigest()
    print token
    print auth.verify(token)  
  elif sys.argv[1] == 'generate':
    auth = Auth()
    auth.generate()
    print auth

