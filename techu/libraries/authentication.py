#!/usr/bin/python
from generic import settings
import sys, hmac
from techu.models import Authentication
from time import time
from hashlib import sha1
from random import choice
from string import digits, ascii_letters

class Auth(object):
  '''
  Authentication protocol
  Resembles OAuth process: 
  *  Client receives a Consumer Key/Secret pair
  *  Constructs an authentication token with HMAC-SHA1 which is sent on each request.
  The Consumer Key and the Secret are comprised from ASCII uppercase & lowercase letters & digits
  This script can also be used as a command-line executable to generate key/secret pairs

  :ivar __token_salt: a salt for the generated secret
  :ivar __consumer_key: the consumer_key sent on each request and is unique for each client (8 characters)
  :ivar __secret: the secret from which a the request token is generated (16 characters)
  '''
  __token_salt   = ''
  __consumer_key = ''
  __secret       = ''

  def __init__(self, consumer_key = ''):
    self.__token_salt = str(time())
    self.__consumer_key = consumer_key

  def get_secret(self):
    '''
    Returns the secret for a consumer key.
    '''
    if self.__consumer_key == '': 
      return True
    auth = Authentication.objects.filter(consumer_key=self.__consumer_key)
    if not auth:
      return False
    else:
      return auth[0].secret

  def update_secret(self):
    '''
    Re-generate secret for a specific consumer key.
    '''
    if self.__consumer_key != '':
      auth = Authentication.objects.filter(consumer_key = self.__consumer_key, secret = self.__secret)
      if not auth:
        return False
      else:
        auth.secret = self.generate_secret()
        auth.save()
        self.__secret = auth.secret
        return True
    return False

  def randomize(self, length, elements = None):
    '''
    |  Return a random string of specified length.
    |  If *elements* parameter is *None* (default) ASCII uppercase, lowercase & digits are used as selection group.
    '''
    if elements is None:
      elements = ascii_letters + digits
    return ''.join([ choice(elements) for n in range(length) ])

  def generate_secret(self):
    '''
    Generate a random secret with a length of 16 characters.
    '''   
    return self.randomize(16, sha1(self.__token_salt + self.randomize(20)).hexdigest())
    
  def generate(self):
    '''
    Returns a consumer key & secret pair.
    '''
    self.__consumer_key = self.randomize(8)
    while self.get_secret():
      self.__consumer_key = self.randomize(8)
    self.__secret = self.generate_secret()
    Authentication.objects.create(consumer_key = self.__consumer_key, secret = self.__secret)
   
  def verify(self, token):
    '''
    Test token using HMAC-SHA1.
    '''
    h = hmac.new(str(self.get_secret()), str(self.__consumer_key), sha1)
    return ( h.hexdigest() == token, token )
  
  def __str__(self):
    '''
    Print consumer key/secret pair.
    '''
    return self.__consumer_key + ' ' + self.__secret

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append('test')
  if sys.argv[1] == 'test':
    ''' test pair -> NBA1e4Ah 1e7fc2c4a1d5d7d1 '''
    test_consumer = 'NBA1e4Ah'
    test_secret = '1e7fc2c4a1d5d7d1'
    auth = Auth(test_consumer)
    token = hmac.new(test_secret, test_consumer, sha1).hexdigest()
    print token
    print auth.verify(token)  
  elif sys.argv[1] == 'generate':
    auth = Auth()
    auth.generate()
    print auth

