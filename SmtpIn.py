from PolicyServer import PolicyServer
from Plugins.DBRateLimit import DBRateLimit
from Plugins.DBWhitelist import DBWhitelist
from Plugins.DBBlacklist import DBBlacklist

class PolicyServers(list):

  def __init__(self, db):
    ClientCheckSrv = PolicyServer('ClientCheckSrv', type = 'unix', unix_path = '/var/run/PostfixPolicyServer/ClientCheckSrv.sock')
    ClientCheckSrv.register_policy(DBWhitelist(db, 'client_address'))
    ClientCheckSrv.register_policy(DBBlacklist(db, 'client_address'))
    ClientCheckSrv.register_policy(DBRateLimit(db, key = 'client_address', time_interval = 1, limits = ((1, 10),), softfail = True))
    self.append(ClientCheckSrv)

    RecpCheckSrv = PolicyServer('RecpCheckSrv', type = 'unix', unix_path = '/var/run/PostfixPolicyServer/RecpCheckSrv.sock')
    RecpCheckSrv.register_policy(DBWhitelist(db, 'sender'))
    RecpCheckSrv.register_policy(DBWhitelist(db, 'recipient'))
    RecpCheckSrv.register_policy(DBBlacklist(db, 'sender'))
    RecpCheckSrv.register_policy(DBBlacklist(db, 'recipient'))
    RecpCheckSrv.register_policy(DBRateLimit(db, key = 'sender', time_interval = 1, limits = ((1, 10),)))
    self.append(RecpCheckSrv)

