#!/usr/bin/python
import os,sys
import string
import random
import urllib

action = sys.argv[1]

L = 1000
f = open(action + '-urls.sh', 'a')
characters = string.ascii_uppercase + "\n\t " + string.digits
for n in range(10000):
  content = ''.join(random.choice(characters) for x in range(L))
  title = ''.join(random.choice(characters) for x in range(50))
  c = urllib.urlencode({'title' : title, 'content' : content})
  params = ( action, n, c, random.randint(1, 100) )
  f.write( "curl --silent 'http://techu:81/indexer/%s/23/%d/?%s&gid=%d&queue=1' \n" % params)
f.close()
