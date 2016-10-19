from Policy import Policy

class DBWhitelist(Policy):

  def __init__(self, db, attribute):
    self.db = db
    self.attribute = attribute

  # Return False if user in whitelist, with 'OK' as the action as this short-circuits the other checks
  def check(self, request_d):
    if self.db.is_in("%s_whitelist" % self.attribute, request_d[self.attribute]):
      return False, 'OK'
    else:
      return True, 'OK'
 
