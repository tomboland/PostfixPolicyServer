import re

emailaddr_re = re.compile('[\w\-\.\+=]+@[\w\-\.]+')
ipaddr_re = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
hostname_re = re.compile('[\w\-\.]+')

class Policy(object):

  def check(self, request_d):
    return True, "OK"

 
  def expand_email_fields(self, addr):
    return (addr.split('@')[1], addr)


  def expand_ipaddr_fields(self, addr):
    return (addr, )


  def get_fields(self, val):

    fields = []    

    # email addresses
    if re.match(emailaddr_re, val):
      fields = self.expand_email_fields(val)

    # ip addresses
    elif re.match(ipaddr_re, val):
      fields = self.expand_ipaddr_fields(val)

    return fields
