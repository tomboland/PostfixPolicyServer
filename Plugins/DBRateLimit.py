from Policy import Policy
from TimeBucket import TimeBucket
from datetime import datetime

class DBRateLimit(Policy):

  def __init__(self, db, attribute = 'sender', time_interval = 15, limits = ((15, 100), (60, 1000))):
    self.db = db
    self.attribute = attribute
    self.MyRateLimiter = TimeBucket(db, time_interval, limits)
    

  def check(self, request_d):
    now = datetime.now()
    try:
      recipient_count = int(request_d['recipient_count']) if int(request_d['recipient_count']) > 0 else 1
    except IndexError:
      recipient_count = 1

    if self.MyRateLimiter.check("%s:%s" % (self.attribute, request_d[self.attribute]), now) is not True:
      return False, "DEFER %s: %s, hit rate-limit" % (self.attribute, request_d[self.attribute])
    else:
      self.MyRateLimiter.increment_counter("%s:%s" % (self.attribute, request_d[self.attribute]), now, increment = recipient_count)
      return True, 'OK'

