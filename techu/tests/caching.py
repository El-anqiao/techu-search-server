#!/usr/bin/python
import sys
import unittest
import random
sys.path.append('..')
from libraries import caching
import time

class TestCaching(unittest.TestCase):

  def setUp(self):
    self.cache = caching.Cache()
    self.prefix = str(random.randint(1, 10**6)) + '-'

  def _testSet(self):
    ''' Set some keys & values '''
    self.assertTrue(self.cache.set(self.prefix + 'key-1', 'value-1'))
    self.assertTrue(self.cache.set(self.prefix + 'key-2', { 'a' : 1, 'b' : 2 }))

  def _testGet(self):
    value_1 = self.cache.get(self.prefix + 'key-1')
    value_2 = self.cache.get(self.prefix + 'key-2')
    self.assertEqual(value_1, 'value-1')
    self.assertEqual(value_2, {'a' : 1, 'b' : 2})
    
  def _testDelete(self):
    self.cache.delete(self.prefix + 'key-1', 1000)
    value_1 = self.cache.get(self.prefix + 'key-1')
    ''' check that key still exists '''
    self.assertEqual(value_1, 'value-1')
    ''' check that it is deleted after 1000 msec '''
    time.sleep(1.001)
    self.assertEqual(self.cache.get(self.prefix + 'key-1'), None)
    ''' delete key-2 immediately '''
    self.cache.delete(self.prefix + 'key-2', 0)
    self.assertEqual(self.cache.get(self.prefix + 'key-2'), None)

  def testSetGetDelete(self):
    self._testSet()
    self._testGet()
    self._testDelete()


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCaching)
  unittest.TextTestRunner(verbosity=2).run(suite)
