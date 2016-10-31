#!/usr/bin/env python

import asyncore, socket, signal, os, importlib
from os import path

MyName = path.splitext(path.basename(__file__))[0]

from Config import Config
MyConf = Config(MyName).conf

import Logging
logger = Logging.get_logger(dict(MyConf.items('Logging')))
logger.info('created logger')

from RedisBackend import RedisBackend
MyDB = RedisBackend(host = MyConf.get('RedisBackend', 'redis_host'), db = MyConf.get('RedisBackend', 'redis_db'))

mod = importlib.import_module(MyConf.get('PostfixPolicyServer', 'service_configuration'), MyConf)
PolicyServers = mod.PolicyServers(MyDB)

def shutdown_handler(signum, frame):
  global PolicyServers
  for PolicyServer in PolicyServers:
    PolicyServer.cleanup()
    del PolicyServer
  raise asyncore.ExitNow()


if __name__ == "__main__":
  logger.info('starting up')
  signal.signal(signal.SIGHUP, shutdown_handler)
  try:
    asyncore.loop()
  except:
    os.kill(os.getpid(), signal.SIGHUP)
