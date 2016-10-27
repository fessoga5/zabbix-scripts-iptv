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

if __name__ == "__main__":
  formedList = createDict(getProcessInfo())
  print createZabbixJson(formedList)
  #try:
  #  if sys.argv[1] == 'discovery':
  #    print createDict(getProcessInfo())
  #    #print createZabbixJson(getDictTemp())
  #  else:
  #    #print getTemp(sys.argv[1])
  #    pass
  #except Exception as e:
  #  print e
  #  print 0
