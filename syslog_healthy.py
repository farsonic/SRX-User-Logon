#!/usr/bin/python 
import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = ContextFilter.hostname
    return True

splunk = "192.168.0.253"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

f = ContextFilter()
logger.addFilter(f)

syslog = SysLogHandler(address=(splunk,514))
formatter = logging.Formatter('%(asctime)s %(hostname)s Posture_App: %(message)s', datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)

logger.info("user=harry ip=192.168.0.166 posture=Healthy")
