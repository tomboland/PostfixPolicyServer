import ConfigParser, os

class Config(object):
  def __init__(self, name):
    for conf_dir in [ "/etc/%s" % name, '/etc', '.' ]:
      if os.path.exists("%s/%s.conf" % (conf_dir, name)):
        print "found config file at %s/%s.conf" % (conf_dir, name)
        file_name = "%s/%s.conf" % (conf_dir, name)
        break

    conf = ConfigParser.RawConfigParser()
    conf.read(file_name)
    self.conf = conf
