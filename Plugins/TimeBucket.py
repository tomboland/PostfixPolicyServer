#!/usr/bin/env python

from hashlib import sha256
from datetime import datetime, timedelta

class TimeBucket(object):

  # dbc = the database connection that supports get and increment methods
  def __init__(self, db, t_interval = 15, limits = ((15, 100), (60, 1000))):
    self.t_interval = t_interval
    self.db = db
    self.limits = limits 


  def get_bucket_hash(self, name, t_time):
    return ''.join([name, '-', str(t_time)])


  def check(self, name, t_time):
    for window, limit in self.limits:
      if not self.check_limit(name, t_time, window, limit):
        return False
    return True


  def check_limit(self, name, t_time, t_window, limit):
    sum = 0
    for bucket in self.get_bucket_range(name, t_time, t_window):
      val = int(self.db.get(bucket))
      sum += val
      if val > 0:
        pass
      if sum >= limit:
        return False
    return True


  def acknowledge_request(self, name, t_time):
    self.db.incr(self.get_bucket_hash(name , self.get_bucket_time(t_time)))


  def get_bucket_val(self, bucket):
    ret = self.db.get(bucket)
    if ret == None:
      return 0
    else:
      return ret


  def get_bucket_time(self, t_time):
    ret = t_time - timedelta(minutes = t_time.minute % self.t_interval, seconds = t_time.second, microseconds = t_time.microsecond)
    return ret


  def get_bucket_range(self, name, t_time, t_window):
    for i in range(0, int(t_window / self.t_interval)):
      t_normalised_time = t_time - timedelta(minutes = self.t_interval * i)
      t_bucket_time = self.get_bucket_time(t_normalised_time)
      yield self.get_bucket_hash(name, t_bucket_time)

