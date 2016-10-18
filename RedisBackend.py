from redis import Redis


class RedisBackend(object):

  def __init__(self, host = 'localhost', db = 0):
    self.db_conn = Redis(host = host, db = db)


  def get_conn(self):
    if self.db_conn is None:
      self.db_conn = Redis(host = host, db = db)
    return self.db_conn

    
  def close_conn(self):
    if self.db_conn is None:
      return
    try:
      del self.db_conn
    except:
      pass
    _conn = None


  def get(self, key):
    ret = self.get_conn().get(key)
    if ret == None:
      return 0
    else:
      return ret


  def incr(self, key, increment = 1):
    if not self.get_conn().exists(key):
      return self.get_conn().set(key, increment, ex = 86400)
    else:
      if increment == 1:
        return self.get_conn().incr(key)
      else:
        return self.get_conn().incrby(key, increment)


  def is_in(self, key, field):
    if self.get_conn().hexists(key, field) == 0:
      return False
    else:
      return True
      
