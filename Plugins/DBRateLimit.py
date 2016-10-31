from Policy import Policy
from Throttling import ThrottlingPolicy
from datetime import datetime

class DBRateLimit(Policy):

  def __init__(self, db, key = 'sender', time_interval = 15, limits = ((15, 100), (60, 1000)), softfail = False):
    self.db = db
    self.key = key
    self.limiter = ThrottlingPolicy(db, time_interval, limits)
    self.softfail = softfail
    

  def check(self, req):
    now = datetime.now()
    try:
      recipient_count = int(req['recipient_count'])
      incr = recipient_count if recipient_count > 0 else 1
    except ValueError:
      incr = 1

    try:
      fields = self.get_fields(str(req[self.key]))
      breaches = []
      for field in fields:
        name = "%s:%s" % (self.key, field)
        if not self.limiter.check_limits(name, now):
          breaches.append(field)

      if len(breaches) >= 1 and self.softfail == False:
        return False, "DEFER %s: %s, hit rate-limit" % (self.key, breaches)

      elif len(breaches) >= 1:
        self.limiter.incr_counter(name, now, incr = incr)
        for field in breaches:
          self.update_leaderboard(field, now)
        return True, "OK %s: %s over rate-limit threshold" % (self.key, breaches)

      else:
        self.limiter.incr_counter(name, now, incr = incr)

    except Exception, e:
      raise Exception("DBRatelimit: request failed, skipping checks: %s" %str(e))
    return True, 'OK'


  def update_leaderboard(self, field, now):
    count = self.limiter.get_timeframe_count("%s:%s" % (self.key, field), now, 1440)
    self.db.zadd("leaderboard:%s" % self.key, int(count), "%s" % (field))
