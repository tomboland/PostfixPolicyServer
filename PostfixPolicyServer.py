#!/usr/bin/env python

import asyncore, socket, signal

from Config import Config
MyConfig = Config('PostfixPolicyServer.conf')

from RedisBackend import RedisBackend
MyRedisBackend = RedisBackend(host = MyConfig.conf.get('RedisBackend', 'redis_host'), db = MyConfig.conf.get('RedisBackend', 'redis_db'))

def shutdown_handler(signum, frame):
  global MyPolicyServer
  MyPolicyServer.cleanup()
  del MyPolicyServer
  raise asyncore.ExitNow()

from PolicyServer import PolicyServer
HeloCheckPolicyServer = PolicyServer('0.0.0.0', 10023)
RecipientCheckPolicyServer = PolicyServer('0.0.0.0', 10024)

from Plugins.DBRateLimit import DBRateLimit
HeloCheckPolicyServer.register_policy(DBRateLimit(MyRedisBackend, attribute = 'client_address', time_interval = 1, limits = ((1, 10),)))
RecipientCheckPolicyServer.register_policy(DBRateLimit(MyRedisBackend, attribute = 'sender', time_interval = 1, limits = ((1, 10),)))

from Plugins.DBWhitelist import DBWhitelist
HeloCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'client_address'))
RecipientCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'sender'))
RecipientCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'recipient'))

from Plugins.DBBlacklist import DBBlacklist
HeloCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'client_address'))
RecipientCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'sender'))
RecipientCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'recipient'))

if __name__ == "__main__":

  signal.signal(signal.SIGHUP, shutdown_handler)

  try:
    asyncore.loop()
  except:
    MyPolicyServer.cleanup()
    del MyPolicyServer
    raise asyncore.ExitNow()
