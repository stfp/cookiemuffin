import percentiles
import unittest


class TestBasicPercentiles(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([25, 50, 75])

    
  def test_simple(self):
    self.tracker.add(1, 3, 4, 8, 10)
    self.assertEqual([3, 4, 8], self.tracker.get_all())
    
    self.tracker.add(7, 2, 9, 5)
    self.assertEqual([3, 5, 8])

    
  def test_interpolation(self):
    self.tracker.add(0, 100)
    self.assertEqual([25, 50, 75], self.tracker.get_all())
    


class TestClampedPercentiles(unittest.TestCase):
  
  def setUp(self):
    self.tracker = percentiles.Tracker([50], maximum=100)


  def test_simple(self):
    self.tracker.add(20, 40, 80, 100, 110, 140)
    self.assertEqual([90], self.tracker.get_all())


  def test_interpolation(self):
    self.tracker.add(0, 1000)
    self.assertEqual([50], self.tracker.get_all())


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



if __name__ == '__main__':
  unittest.main()
