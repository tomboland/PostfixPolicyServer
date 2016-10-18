from redis import Redis


class RedisBackend(object):

  def __init__(self, host = 'localhost', db = 0):
    self.db_conn = Redis(host = host, db = db)


  def get(self, key):
    ret = self.db_conn.get(key)
    if ret == None:
      return 0
    else:
      return ret


  def incr(self, key):
    if not self.db_conn.exists(key):
      return self.db_conn.set(key, 1, ex = 86400)
    else:
      return self.db_conn.incr(key)


  def is_in(self, key, field):
    print "is_in", key, field
    if self.db_conn.hexists(key, field) == 0:
      return False
    else:
      return True
      
