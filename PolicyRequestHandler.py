import asyncore, socket

class PolicyRequestHandler(asyncore.dispatcher_with_send):

  def __init__(self, socket, policies):
    self.policies = policies
    asyncore.dispatcher_with_send.__init__(self, socket)

  def handle_read(self):
    request_d = {}
    req_string = self.recv(16384)
    lines = req_string.split("\n")
    for line in lines:
      if len(line) > 0:
        k, v = line.split("=", 1)
        request_d[k] = v
    print request_d
    self.send("action=%s\n\n" % self.check_policies(request_d))
    self.close()


  def check_policies(self, request_d):
    for policy in self.policies:
      result, action = policy.check(request_d)
      if result is not True:
        return action
        break
    return "OK"

