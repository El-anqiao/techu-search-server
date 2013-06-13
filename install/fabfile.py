from fabric.api import run
from fabric.context_manages import cd, lcd

OPTIONAL_PACKAGES = [ 'beautifulsoup4', 'hiredis', ]
REQUIRED_PACKAGES = [
  'django', 'django_graceful', 'redis', 'hiredis',  
]

def compiler(url, folder):
  with cd('/tmp'):
    run('wget "%s" -O source.tar.gz' % url)
    run('tar -zxvf source.tar.gz')
    run('cd %s' % folder)
    run('make')
    run('make install')
    run('make test')
    run('rm -rf /tmp/' + folder.strip('/'))
  
#  redis-2.6.13')
  run('cd redis-2.6.13')
  
  run('wget http://redis.googlecode.com/files/redis-2.6.13.tar.gz')

run('apt-get install python-setuptools')
run('apt-get install nginx python-flup')
run('apt-get install mysql-server python-mysqldb')
http://sphinxsearch.com/files/sphinx-2.1.1-beta.tar.gz
run('apt-get install libhiredis0.10 libhiredis-dev')

python_packages = REQUIRED_PACKAGES + OPTIONAL_PACKAGES
for package in python_packages:
  run('easy_install %s' % package)


