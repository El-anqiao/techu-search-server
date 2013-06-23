#!/usr/bin/python
import sys
import unittest
sys.path.append('..')
from libraries.generic import *

class TestGeneric(unittest.TestCase):

  def testRedisConnection(self):
    self.assertTrue(isinstance(redis_client(), redis.StrictRedis))

  def testRegexCheck(self):
    self.assertTrue(regex_check('techu_123'))

  def testIdentq(self):
    self.assertEqual(identq('table`1'), '`table1`')
  
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneric)
  unittest.TextTestRunner(verbosity=2).run(suite)    
