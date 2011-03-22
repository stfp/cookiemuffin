import percentiles
import unittest


class TestBasicPercentiles(object):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([25, 50, 70])

    
  def test_simple(self):
    self.tracker.add(1, 3, 4, 8, 10)
    self.assertEqual([3, 4, 8], self.tracker.get_all())
    
    self.tracker.add(7, 2, 9 5)
    self.assertEqual([3, 5, 8])

    
  def test_interpolation(self):
    self.tracker.add(0, 100)
    self.assertEqual([25, 50, 75], self.tracker.get_all())
    


class TestClampedPercentiles(object):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([50], max = 100)


  def test_simple(self):
    self.tracker.add(20, 40, 80, 100, 110, 140)
    self.assertEqual([90], self.tracker.get_all())


  def test_interpolation(self):
    self.tracker.add(0, 1000)
    self.assertEqual([50], self.tracker.get_all())



if __name__ == '__main__':
  unittest.main()