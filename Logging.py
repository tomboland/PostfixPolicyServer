import logging, logging.handlers, syslog

def get_logger(config_d):
  logger = logging.getLogger('Base')
  try:
    logger.setLevel(logging.DEBUG)

    if config_d['file_enable'] == 'True':
      handler = logging.handlers.RotatingFileHandler( \
        config_d['file_name'], \
        maxBytes = int(config_d['file_max_bytes']), \
        backupCount = int(config_d['file_backup_count']))
      handler.setFormatter(logging.Formatter(config_d['file_format']))
      logger.addHandler(handler)

    if config_d['syslog_enable'] == 'True':
      handler = logging.handlers.SysLogHandler( \
        address = (config_d['syslog_server'], 514), \
        facility = syslog.LOG_MAIL)
      handler.setFormatter(logging.Formatter(config_d['syslog_format']))
      logger.addHandler(handler)

  except IndexError, e:
    raise Exception("fixme: %s", e)

  return logger
