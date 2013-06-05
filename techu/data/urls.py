#!/usr/bin/python
import codecs
from urllib import urlencode

f = codecs.open('data.json', encoding = 'utf-8', mode = 'r')
print '#!/bin/bash'
for r in f.readlines():
  print "echo '%s'" % urlencode({ 'data' : r })
  print "curl --silent 'http://techu:81/indexer/insert/28/' -d '%s'" % urlencode({ 'data' : r })
f.close()
