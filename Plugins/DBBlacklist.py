from Policy import Policy

class DBBlacklist(Policy):

  def __init__(self, db, key):
    self.db = db
    self.key = key

  def check(self, req):
    fields = self.get_fields(str(req[self.key]))
    try:
      for field in fields:
        if self.db.is_in_hash("%s_blacklist" % self.key, field):
          return False, "REJECT %s: %s, is blacklisted" % (self.key, field)
    except Exception, e:
      raise Exception ("DBBlacklist: request failed, skipping checks: %s" % str(e))
    return True, 'OK'
