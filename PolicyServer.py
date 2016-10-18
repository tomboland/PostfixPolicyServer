import asyncore, socket
from PolicyRequestHandler import PolicyRequestHandler

class PolicyServer(asyncore.dispatcher):
  def __init__(self, host, port):
    self.policies = []
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.set_reuse_addr()
    self.bind(('', port))
    self.listen(1)

  def cleanup(self):
    pass

  def handle_accept(self):
    socket, address = self.accept()
    PolicyRequestHandler(socket, self.policies)

  def register_policy(self, policy):
    self.policies.append(policy)

