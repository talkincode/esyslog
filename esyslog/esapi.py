#!/usr/bin/env python
# coding=utf-8

from esyslog import httpclient
from twisted.internet import reactor
from twisted.python import log
import json
import time
import datetime
import base64
import traceback
import sys
import pytz

class EslogApi(object):

    def __init__(self,esconfig):
        self.apiurl = esconfig.apiurl
        self.apiuser = esconfig.apiuser
        self.apipwd = esconfig.apipwd
        self.index = "%s-%s" % (esconfig.get("index"),datetime.datetime.now().strftime("%Y%m"))
        self.tz = pytz.timezone(esconfig.get("tz","Asia/Shanghai"))
        reactor.callLater(1.0,self.init_index)

    def init_index(self):
        try:
            puturl = "{0}/{1}".format(self.apiurl,self.index)
            reqmsg = '{"mappings": {"esyslog": {"_ttl": {"enabled": true,"default": "7d"}}}}'
            user_and_pwd = "{0}:{1}".format(self.apiuser,self.apipwd)
            headers = {"Authorization": ["Basic {0}".format(base64.b64encode(user_and_pwd))]}
            d = httpclient.fetch(puturl,postdata=reqmsg,headers=headers)
            d.addCallback(lambda r:log.msg(r.body)).addErrback(lambda e:log.err(e))
        except:
            traceback.print_exc()

    def send(self,logitem={}):
        try:
            _ctime = self.tz.localize(logitem.pop('time',datetime.datetime.now()))
            ttl = logitem.pop("ttl","7d")
            reqmsg = dict(
                timestamp=_ctime.isoformat()
            )
            reqmsg.update(logitem)
            puturl = "{0}/{1}/esyslog?ttl={2}".format(self.apiurl,self.index,ttl)
            user_and_pwd = "{0}:{1}".format(self.apiuser,self.apipwd)
            headers = {"Authorization": ["Basic {0}".format(base64.b64encode(user_and_pwd))]}
            postdata = json.dumps(reqmsg,ensure_ascii=False).encode('utf-8')
            d = httpclient.fetch(puturl,postdata=postdata,headers=headers)
            d.addCallback(lambda r:logger.debug(r.body)).addErrback(lambda e:sys.stderr.write(repr(e)))
        except:
            traceback.print_exc()





