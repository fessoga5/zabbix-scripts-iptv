#!/usr/bin/python2.7
# vim: sts=2 ts=2 sw=2 et ai
import json
import sys

def getDictTemp():
  import xmlrpclib
  server = xmlrpclib.Server('http://localhost:9001/RPC2')
  return server.getProcessInfo()

def getTemp(name):
  result = dict()
  sensors.init()
  try:
    for chip in sensors.iter_detected_chips():
        for feature in chip:
          try:
              if feature.label == name:
                return feature.get_value()
          except:
            pass
  finally:
      sensors.cleanup()

def createZabbixJson(data):
    """
    Create json for zabbix discovery service
    """
    try:
      result = {"data":[]}
      for dom, value in data.iteritems():
        result['data'].append({"{#NAME}":dom})
      return json.dumps(result) 
    except:
      return 0

if __name__ == "__main__":
  try:
    if sys.argv[1] == 'discovery':
      print getDictTemp()
      #print createZabbixJson(getDictTemp())
    else:
      #print getTemp(sys.argv[1])
      pass
  except:
    print 0
