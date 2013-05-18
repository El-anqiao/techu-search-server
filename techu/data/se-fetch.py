#!/usr/bin/python
import os, sys
import time 
import json
import codecs
from bs4 import BeautifulSoup as bs
import requests

def strip_tags(el):
  return '' . join( el.findAll(text = True) )

fetch_url = r'wget -q -O- --header\="Accept-Encoding: gzip" "%(url)s" | gunzip > %(json)s'

url = 'http://api.stackexchange.com/2.1/posts?page=%d&pagesize=100&order=desc&sort=activity&site=stackoverflow'

''' Download 20x100 posts (questions & answers) from StackOverflow '''
fw = codecs.open('data.json', mode = 'a', encoding = 'utf-8')
for n in range(1, 21):
  print 'Downloading page', n
  cmd = fetch_url % { 'url' : url % n, 'json' : 'page.%d.json' % n }
  print cmd
  os.system(cmd)
  print 'Formatting JSON data for import ...'
  f = codecs.open('page.%d.json' %n, mode = 'r', encoding = 'utf-8')
  d = json.loads(''.join(f.readlines()))
  f.close()
  os.system("rm 'page.%d.json'" % n)
  for item in d['items']:
    post_item = {}
    post_item['id'] = item['post_id']
    post_item['title'] = ''
    post_item['body'] = ''
    post_item['creation_date'] = item['creation_date']
    post_item['last_activity_date'] = item['last_activity_date']
    post_item['is_answer'] = int(item['post_type'] == 'answer')
    post_item['score'] = item['score']
    if 'owner' in item:
      post_item['user_id'] = item['owner']['user_id']
    else:
      post_item['user_id'] = 0
    html = requests.get(item['link'])
    soup = bs(html.text)
    body = ''
    title = ''
    if item['post_type'] == 'answer':
      body = soup.find('div', id = 'answer-' + str(item['post_id']))      
    else:
      body = soup.find('div', id = 'question')
      title = soup.find('div', id = 'question-header').find('a', {'class' : 'question-hyperlink'});
    post_item['body'] = strip_tags( body.find('div', { 'class' : 'post-text' }))
    if title != '':
      post_item['title'] = strip_tags( title )
    fw.write(json.dumps(post_item) + "\n")
    time.sleep(0.001)
  time.sleep(10.0)

fw.close()
