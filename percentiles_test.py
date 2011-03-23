import percentiles
import unittest
import time


class TestBasicPercentiles(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([25, 50, 75])
      
  def test_values(self):
    self.tracker.add(1, 3, 4, 8, 10)
    self.assertEqual(1,  self.tracker.value_for_rank(1))
    self.assertEqual(3,  self.tracker.value_for_rank(2))
    self.assertEqual(4,  self.tracker.value_for_rank(3))
    self.assertEqual(8,  self.tracker.value_for_rank(4))
    self.assertEqual(10, self.tracker.value_for_rank(5))

  def test_get_percent_ranks(self):
    self.assertEqual([5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0], percentiles.Tracker.get_percent_ranks(10))
    self.assertEqual([10.0, 30.0, 50.0, 70.0, 90.0], percentiles.Tracker.get_percent_ranks(5))

  def test_simple(self):
    self.tracker.add(1, 3, 4, 8, 10)
    self.assertEqual([2.5, 4, 8.5], self.tracker.get_all())    
    self.tracker.add(7, 2, 9, 5)
    self.assertEqual([2.7650000000000001, 5.0899999999999999, 8.3149999999999995], self.tracker.get_all())

  def test_interpolation(self):
    self.tracker.add(0, 1000)
    #self.assertEqual([250, 500, 750], self.tracker.get_all())
    self.assertEqual([0, 500, 1000], self.tracker.get_all())



class TestClampedPercentiles(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([50], maximum=100)


  def test_simple(self):
    self.tracker.add(20, 40, 80, 100, 110, 140)
    self.assertEqual([92], self.tracker.get_all())

  def test_interpolation(self):
    self.tracker.add(0, 1000)
    self.assertEqual([50], self.tracker.get_all())

"""
class TestExpiringPercentiles(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([50], expire = 60 * 60)
    
  
  def test_simple(self):
    self.tracker.add(100, time = 0)
    self.assertEqual([100], self.tracker.get_all(time = 500))
    
    self.tracker.add(200, time = 1000)
    self.assertEqual([150], self.tracker.get_all(time = 1500))
    
    self.tracker.add(300, time = 2000)
    self.assertEqual([200], self.tracker.get_all(time = 2500))
    
    self.tracker.add(200, time = 3000)
    self.assertEqual([200], self.tracker.get_all(time = 3500))
    
    self.tracker.add(100, time = 4000)
    self.assertEqual([200], self.tracker.get_all(time = 4500))
    
    self.tracker.add(900, time = 5000)
    self.assertEqual([200], self.tracker.get_all(time = 5500))

"""

class TestContextTimeTracker(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.ContextTracker([50])
    

  def test_simple(self):
    self.tracker.enter('a')
    time.sleep(0.5)
    self.tracker.enter('b')
    time.sleep(0.1)
    self.tracker.leave()
    time.sleep(0.1)
    self.tracker.leave()
    self.assertEqual([701], self.tracker.trackers['a'].get_all())
    self.assertEqual([100], self.tracker.trackers['a/b'].get_all())

if __name__ == '__main__':
  unittest.main()
