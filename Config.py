import ConfigParser

class Config(object):
  def __init__(self, file_name):
    conf = ConfigParser.ConfigParser()
    conf.read(file_name)
    self.conf = conf
