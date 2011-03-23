#!/usr/bin/env python

import time
import logging


class Tracker:
    def __init__(self, percentile_list, maximum=None, expire=None):
        self.__percentile_list = percentile_list # [ x/100.0 for x in percentile_list ]
        self.__data = []
        self.__count = 0
        self.__maximum = maximum
    
    @staticmethod
    def get_percent_ranks(count):
        return [ 100/count * (n-1.0/2.0) for n in range(1, count+1) ]
    
    def add(self, *args, **kwargs):
        for value in args:
            logging.debug("%s - adding value %.2f", self, value)
            value = int(value)
            if self.__maximum:
                value = min(value, self.__maximum)
            if value >= len(self.__data):
                self.__data.extend([0]* (value - len(self.__data) + 1))
            self.__data[value] += 1
            self.__count += 1
    
    def value_for_rank(self, rank):
        cur = 0
        for i in range(len(self.__data)):
            cur += self.__data[i]
            if cur >= rank:
                return i
        return 0

    def get_percentile(self, percentile):
        pcranks = Tracker.get_percent_ranks(self.__count)
        if percentile < pcranks[0]:
            k = 1
        elif percentile > pcranks[-1]:
            k = self.__count
        elif percentile in pcranks:
            k = pcranks.index(percentile) + 1
        else:
            k = 1
            for i in range(self.__count - 1):
                if pcranks[i] <= percentile and percentile <= pcranks[i+1]:
                    k = i + 1
                    break
        value = self.value_for_rank(k)
        value_next = self.value_for_rank(k+1)
        #print "percentile", percentile, "k", k, "data", self.__data, "pcranks", pcranks, "value", value, "value_next", value_next
        return value + self.__count * (max(0, percentile - pcranks[k-1]))/100.0*(value_next - value)

    def get_all(self, time=None):
        result = []
        for per in self.__percentile_list:
            result.append(self.get_percentile(per))
        return result


class ContextTracker():
    """ a contextual time tracker with a 1ms precision
    """
    def __init__(self, percentile_list):
        self.percentile_list = percentile_list
        self.path = []
        self.times = []
        self.trackers = {}

    def enter(self, name):
        self.path.append(name)
        self.times.append(time.time())
    
    def leave(self):
        duration = int((time.time() - self.times.pop()) * 1000)
        self.getTrackerForPath(self.currentPath()).add(duration)
        self.path.pop()

    def getTrackerForPath(self, path):
        t = self.trackers.get(path, None)
        if t is None:
            t = self.trackers[path] = Tracker(self.percentile_list)
        return t

    def currentPath(self):
        return '/'.join(self.path)
