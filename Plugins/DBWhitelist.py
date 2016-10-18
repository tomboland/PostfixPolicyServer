from Policy import Policy

class DBWhitelist(Policy):

  def __init__(self, db, attribute):
    self.db = db
    self.attribute = attribute

  def check(self, request_d):
    if self.db.is_in("%s_whitelist" % self.attribute, request_d[self.attribute]):
      return False, "OK"
    else:
      return True, "OK"
 
