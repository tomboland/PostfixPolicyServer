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


  def incr(self, key, incr = 1):
    if not self.get_conn().exists(key):
      return self.get_conn().set(key, incr, ex = 86400)
    else:
      if incr == 1:
        return self.get_conn().incr(key)
      else:
        return self.get_conn().incrby(key, incr)


  def is_in_hash(self, key, field):
    if self.get_conn().hexists(key, field) == 0:
      return False
    else:
      return True


  def hset(self, key, field, value):
    self.get_conn().hset(key, field, value)


  def hget(self, key, field):
    return self.get_conn().hset(key, field)


  def hgetall(self, key):
    return self.get_conn().hgetall(key)


  def zadd(self, key, score, field):
    print key, score, field
    return self.get_conn().zadd(key, field, score)
