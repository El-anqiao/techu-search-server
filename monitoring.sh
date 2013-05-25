#!/bin/bash
while [ 1 ]; do
  modified=$(find /home/techu-search-server/techu/ -mtime 0 \( -name '*.py' \))
  if [[ -n "$modified" ]]; then
    /home/techu-search-server/manage.py update
  fi
  sleep 5
done
