import asyncore, socket, logging, os
from os import path
from pwd import getpwnam
from grp import getgrnam
from PolicyRequestHandler import PolicyRequestHandler

logger = logging.getLogger('Base')

class PolicyServer(asyncore.dispatcher):

  def __init__(self, name, type = 'tcp', host = '127.0.0.1', port = 10023, unix_path = None, unix_owner = 'postfix', unix_group = 'postfix', unix_permissions = 0660):

    self.policies = []
    self.unix_path = unix_path
    self.name = name
    asyncore.dispatcher.__init__(self)

    if type == 'tcp':
      self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
      self.set_reuse_addr()
      self.bind((host, port))
    elif type == 'unix':
      self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
      self.set_reuse_addr()
      self.bind(unix_path)
      if path.exists(unix_path):
        uid = getpwnam(unix_owner).pw_uid
        gid = getgrnam(unix_group).gr_gid
        os.chown(unix_path, uid, gid)
        os.chmod(unix_path, unix_permissions)
    else:
      msg = '%s, no valid listening socket specified' % name
      logger.info(msg)
      raise Exception(msg)
    self.listen(1)


  def cleanup(self):
    if path.exists(self.unix_path):
      os.remove(self.unix_path)


  def handle_accept(self):
    socket, address = self.accept()
    logger.debug("%s, accepted connection from %s" % (self.name, address))
    PolicyRequestHandler(socket, self.name, self.policies)


  def register_policy(self, policy):
    self.policies.append(policy)
    logger.info("%s, registered policy, %s" % (self.name, policy))
