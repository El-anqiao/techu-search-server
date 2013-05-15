#!/usr/bin/python
import sys
from urllib import urlencode

variable = sys.argv[1]
data = sys.argv[2]

print urlencode({ variable : data})
