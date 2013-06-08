#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import codecs
import re

def readfile(path):
  f = codecs.open(path, mode = 'r', encoding = 'utf-8')
  text = u"".join(f.readlines())
  f.close()
  return text

sequence = [
  'header.html',
  'features.html',
  'how-it-works.html',
  'installation.html',
  'examples.html',
  'whats-next.html',
  'footer.html',
]

os.system('mv ../index.html ../index.html.bak')
f = codecs.open('../index.html', mode = 'w', encoding = 'utf-8')
includes = re.compile(r'\{\{\s+[a-z\.]+\s+\}\}')
for index, section in enumerate(sequence):
  html = readfile(section)
  for include in includes.findall(html):
    include_file = 'includes/' + include.strip('{}').strip()
    replacement_text = readfile(include_file)
    html = html.replace(include, replacement_text)
  f.write(html + "\n")
f.close()
