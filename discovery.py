#!/usr/bin/python2.7
# vim: sts=2 ts=2 sw=2 et ai
import json
import sys

def getProcessInfo():
  import supervisor.xmlrpc
  import xmlrpclib

  p = xmlrpclib.ServerProxy('http://127.0.0.1',
          transport=supervisor.xmlrpc.SupervisorTransport(
              None, None,
              'unix:///var/run/supervisor.sock'))

  return p.supervisor.getAllProcessInfo()

def createDict(RetProcessInfo):
  #[{'now': 1477550009, 'group': '238.0.5.21;5210;PerviiHD', 'description': 'pid 26674, uptime 0:00:05', 'pid': 26674, 'stderr_logfile': 'syslog', 'stop': 0, 'statename': 'RUNNING', 'start': 1477550004, 'state': 20, 'stdout_logfile': 'syslog', 'logfile': 'syslog', 'exitstatus': 0, 'spawnerr': '', 'name': '238.0.5.21;5210;PerviiHD'}, {'now': 1477550009, 'group': '238.0.5.22;5220;RossiaHD', 'description': 'pid 26675, uptime 0:00:05', 'pid': 26675, 'stderr_logfile': 'syslog', 'stop': 0, 'statename': 'RUNNING', 'start': 1477550004, 'state': 20, 'stdout_logfile': 'syslog', 'logfile': 'syslog', 'exitstatus': 0, 'spawnerr': '', 'name': '238.0.5.22;5220;RossiaHD'}]
  convert = dict()

  for value in RetProcessInfo:
    ip_stream, rc_port, name  = value['group'].split(";")
    convert[name]= dict({'ip_stream': ip_stream, 'rc_port': rc_port, 'name': name})

  return convert

def createZabbixJson(data):
    """
    Create json for zabbix discovery service
    """
    try:
      result = {"data":[]}
      for name, value in data.iteritems():
        result['data'].append({"{#NAME}":name, "{#IP_STREAM}": value['ip_stream'], "{#RC_PORT}": value['rc_port'] })
      return json.dumps(result) 
    except:
      return 0


def netcat(hostname, port, content):
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((hostname, port))
  s.sendall(content)
  s.shutdown(socket.SHUT_WR)
  while 1:
    data = s.recv(1024)
    #if data.startswith("input bytes read"):
    if data == "":
      break
    if repr(data).startswith("'+----[ begin of statistical info"):
      return repr(data)
  s.close()

def parseNetcat(attribute, Retnetcat):
#'+----[ begin of statistical info\r\n+-[Incoming]\r\n| input bytes read :     2712 KiB\r\n| input bitrate    :    10860 kb/s\r\n| demux bytes read :     2442 KiB\r\n| demux bitrate    :     9580 kb/s\r\n| demux corrupted  :        0\r\n| discontinuities  :        0\r\n|\r\n+-[Video Decoding]\r\n| video decoded    :       19\r\n| frames displayed :       15\r\n| frames lost      :        0\r\n|\r\n+-[Audio Decoding]\r\n| audio decoded    :       77\r\n| buffers played   :       77\r\n| buffers lost     :        0\r\n|\r\n+-[Streaming]\r\n| packets sent     :        0\r\n| bytes sent       :        0 KiB\r\n| sending bitrate  :        0 kb/s\r\n+----[ end of statistical info ]\r\n> Bye-bye!\r\n'
  import re
  channelDict = dict()
  try:
    m = re.match('^.*{}\s+:\s+([0-9]+).*$'.format(attribute.strip()), Retnetcat)
    return m.group(1)
  except:
    return 0

if __name__ == "__main__":
  #print netcat('127.0.0.1', 5210, 'stats\n')
  try:
    if sys.argv[1] == 'discovery':
      print createZabbixJson(createDict(getProcessInfo()))
    else:
      #print getTemp(sys.argv[1])
      print parseNetcat(sys.argv[1], netcat('127.0.0.1', int(sys.argv[2]), 'stats\n'))
  except Exception as e:
    print 0
