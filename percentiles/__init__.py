#!/usr/bin/env python

import time

class Tracker:
    def __init__(self, percentile_list, maximum=None):
        self.__percentile_list = [ x/100.0 for x in percentile_list ]
        self.__data = []
        self.__total = 0
        self.__maximum = maximum
    
    def add(self, *args):
        for value in args:
            if self.__maximum:
                value = min(value, self.__maximum)
            if value >= len(self.__data):
                self.__data.extend([0]* int(value - len(self.__data)))
            for i in range(int(value)):
                self.__data[i] += 1
            self.__total += value
    
    def get_all(self):
        result = []
        for per in self.__percentile_list:
            goal = per * self.__total
            count = 0
            for i in range(len(self.__data)):
                count += self.__data[i]
                if count >= goal:
                    result.append(i + 1)
                    break
        return result


class ContextTracker():
    def __init__(self, percentile_list):
        self.percentile_list = percentile_list
        self.path = []
        self.times = []
        self.trackers = {}

    def enter(self, name):
        self.path.append(name)
        self.times.append(time.time())
    
    def leave(self):
        duration = time.time() - self.times.pop()
        self.getTrackerForPath(self.currentPath()).add(duration)
        self.path.pop()

    def getTrackerForPath(self, path):
        t = self.trackers.get(path, None)
        if t is None:
            t = self.trackers[path] = Tracker(self.percentile_list)
        return t

    def currentPath(self):
        return '/'.join(self.path)
