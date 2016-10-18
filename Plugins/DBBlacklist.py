from Policy import Policy

class DBBlacklist(Policy):

  def __init__(self, db, attribute):
    self.db = db
    self.attribute = attribute

  def check(self, request_d):
    if self.db.is_in("%s_blacklist" % self.attribute, request_d[self.attribute]):
      return False, "REJECT %s: %s, is blacklisted" % (self.attribute, request_d[self.attribute])
    else:
      return True, 'OK'

