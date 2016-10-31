import asyncore, socket, logging

logger = logging.getLogger('Base')

class PolicyRequestHandler(asyncore.dispatcher_with_send):

  def __init__(self, socket, srv_name, policies):
    self.srv_name = srv_name
    self.policies = policies
    asyncore.dispatcher_with_send.__init__(self, socket)


  def handle_read(self):
    req = {}
    req_string = self.recv(16384)
    lines = req_string.split("\n")

    for line in lines:
      if len(line) > 0:
        try:
          k, v = line.split("=", 1)
          req[k] = v
        except ValueError:
          pass

    action = "%s" % self.check_policies(req)
    self.log(action, req)
    self.send("action=%s\n\n" % action)
    self.close()


  def check_policies(self, req):
    try:
      for policy in self.policies:
        result, action = policy.check(req)
        if result is not True:
          return action
          break
    except Exception, e:
      logger.debug("%s, Unhandled error in policy check: %s" % (self.srv_name, str(e)))
    return "OK"


  def log(self, action, req):
    names = ['client_name', 'client_address', 'helo_name', 'sender', 'recipient', 'recipient_count' ]
    logger.info(', '.join(["%s" % self.srv_name] + ["%s=%s" % (name, req[name]) for name in names] + ["action=%s" % action]))
    logger.debug(', '.join(["%s" % self.srv_name] + ["%s=%s" % (name, req[name]) for name in req] + ["action=%s" % action]))


