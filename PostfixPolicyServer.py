#!/usr/bin/env python

import asyncore, socket, signal, os

from Config import Config
MyConf = Config('PostfixPolicyServer.conf').conf

from RedisBackend import RedisBackend
MyRedisBackend = RedisBackend(host = MyConf.get('RedisBackend', 'redis_host'), db = MyConf.get('RedisBackend', 'redis_db'))

from PolicyServer import PolicyServer
HeloCheckPolicyServer = PolicyServer(MyConf.get('HeloCheckPolicyServer', 'listen_addr'), int(MyConf.get('HeloCheckPolicyServer', 'listen_port')))
RecipientCheckPolicyServer = PolicyServer(MyConf.get('RecipientCheckPolicyServer', 'listen_addr'), int(MyConf.get('RecipientCheckPolicyServer', 'listen_port')))

from Plugins.DBRateLimit import DBRateLimit
from Plugins.DBWhitelist import DBWhitelist
from Plugins.DBBlacklist import DBBlacklist

HeloCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'client_address'))
HeloCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'client_address'))
HeloCheckPolicyServer.register_policy(DBRateLimit(MyRedisBackend, attribute = 'client_address', time_interval = 1, limits = ((1, 10),)))

RecipientCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'sender'))
RecipientCheckPolicyServer.register_policy(DBWhitelist(MyRedisBackend, 'recipient'))
RecipientCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'sender'))
RecipientCheckPolicyServer.register_policy(DBBlacklist(MyRedisBackend, 'recipient'))
RecipientCheckPolicyServer.register_policy(DBRateLimit(MyRedisBackend, attribute = 'sender', time_interval = 1, limits = ((1, 10),)))


def shutdown_handler(signum, frame):
  global HeloCheckPolicyServer
  HeloCheckPolicyServer.cleanup()
  del HeloCheckPolicyServer
  global RecipientCheckPolicyServer
  RecipientCheckPolicyServer.cleanup()
  del RecipientCheckPolicyServer
  raise asyncore.ExitNow()


if __name__ == "__main__":

  signal.signal(signal.SIGHUP, shutdown_handler)

  try:
    asyncore.loop()
  except:
    os.kill(os.getpid(), signal.SIGHUP)
