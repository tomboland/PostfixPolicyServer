#!/usr/bin/env python

import asyncore, socket, signal

from Config import Config
MyConfig = Config('MailLogRates.conf')

from RedisBackend import RedisBackend
MyRedisBackend = RedisBackend(host = MyConfig.conf.get('RedisBackend', 'redis_host'), db = MyConfig.conf.get('RedisBackend', 'redis_db'))

from RateLimits import RateLimits
MyRateLimits = RateLimits(MyRedisBackend, int(MyConfig.conf.get('RateLimits', 'time_interval')))


def shutdown_handler(signum, frame):
  global MyPolicyServer
  MyPolicyServer.cleanup()
  del MyPolicyServer
  raise asyncore.ExitNow()

from PolicyServer import PolicyServer
MyPolicyServer = PolicyServer('0.0.0.0', 10023)

from Plugins.DBWhitelist import DBWhitelist
MyPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'sender'))
MyPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'recipient'))
MyPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'client_address'))

from Plugins.DBBlacklist import DBBlacklist
MyPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'sender'))
MyPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'recipient'))
MyPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'client_address'))

if __name__ == "__main__":

  signal.signal(signal.SIGHUP, shutdown_handler)

  try:
    asyncore.loop()
  except:
    MyPolicyServer.cleanup()
    del MyPolicyServer
    raise asyncore.ExitNow()
