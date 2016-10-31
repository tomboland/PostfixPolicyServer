from Policy import Policy

class DBWhitelist(Policy):

  def __init__(self, db, key):
    self.db = db
    self.key = key

  # Return False if user in whitelist, with 'OK' as the action as this short-circuits the other checks
  def check(self, req):
    fields = self.get_fields(str(req[self.key]))
    try:
      for field in fields:
        if self.db.is_in_hash("%s_whitelist" % self.key, field):
          return False, "OK %s is whitelisted" % self.key
    except Exception, e:
      raise Exception("DBWhitelist: request failed, skipping checks: %s" % str(e))
    return True, 'OK'
