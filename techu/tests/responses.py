#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, codecs
import unittest
sys.path.append('..')
import requests
import re, json

class TestResponses(unittest.TestCase):
  BaseURL = 'http://techu:81'

  def _status(self, r):
    self.assertEqual(r.status_code, 200)

  def setUp(self):
    f = codecs.open('./responses.txt', encoding = 'utf-8', mode = 'r')
    self.responses = [ response.replace("\\\n", "\n")  for response in f.readlines() ]
    f.close()

  def testHome(self):
    r = requests.get(self.BaseURL)
    self._status(r)

  def testIndexOptions(self):
    data = { "path" : "/usr/local/sphinx/data/so_posts_rt" }
    data = { "data" : json.dumps(data) }
    print data
    print self.BaseURL + '/option/index/28/'
    r = requests.post(self.BaseURL + '/option/index/28/', data = data)
    self._status(r)


  def testGenerateConfiguration(self):
    r = requests.get(self.BaseURL + '/generate/25/')
    self._status(r)
    self.assertEqual(json.loads(r.content), json.loads(self.responses[0].strip()))

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestResponses)
  unittest.TextTestRunner(verbosity=2).run(suite)    
