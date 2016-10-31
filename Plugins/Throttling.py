from datetime import datetime, timedelta

class ThrottlingWindowLimit(object):

  def __init__(self, timeframe = None, limit = None):
    self.timeframe = timeframe
    self.limit = limit


class ThrottlingPolicy(object):

  def __init__(self, db, interval = 15, limits = ((15, 100), (60, 1000))):
    self.interval = interval
    self.db = db
    self.limits = limits 


  def get_bucket_key(self, name, timestamp):
    return ''.join([name, '-', str(timestamp)])


  def check_limits(self, name, timestamp):
    for timeframe, limit in self.limits:
      if not self.check_limit(name, timestamp, timeframe, limit):
        return False
    return True


  def check_limit(self, name, timestamp, timeframe, limit):
    sum = 0
    for bucket in self.get_bucket_range(name, timestamp, timeframe):
      val = int(self.db.get(bucket))
      sum += val
      if sum >= limit:
        return False
    return True


  def get_counts(self, name, timestamp):
    for timeframe, limit in self.limits:
      count = self.get_timeframe_count(name, timestamp, timeframe)
      if count > limit:
        yield (timeframe, limit, count)


  def get_timeframe_count(self, name, timestamp, timeframe):
    sum = 0
    for bucket in self.get_bucket_range(name, timestamp, timeframe):
      val = int(self.get_count(bucket))
      sum += val
    return sum


  def get_count(self, bucket):
    ret = self.db.get(bucket)
    if ret == None:
      return 0
    else:
      return ret


  def incr_counter(self, name, timestamp, incr = 1):
    bucket_key = self.get_bucket_key(name, self.getbucket_timestamp(timestamp))
    self.db.incr(bucket_key, incr = incr)


  def getbucket_timestamp(self, timestamp):
    ret = timestamp - timedelta(minutes = timestamp.minute % self.interval, seconds = timestamp.second, microseconds = timestamp.microsecond)
    return ret


  def get_bucket_range(self, name, timestamp, timeframe):
    for i in range(0, int(timeframe / self.interval)):
      normalised_time = timestamp - timedelta(minutes = self.interval * i)
      bucket_timestamp = self.getbucket_timestamp(normalised_time)
      yield self.get_bucket_key(name, bucket_timestamp)
