#!/usr/bin/env python
# coding=utf-8
from esyslog import choosereactor
choosereactor.install_optimal_reactor(False)
from esyslog import config as iconfig
import argparse
import sys
import json
import os
import time
from twisted.internet import protocol
from syslog_protocol import SyslogProtocol
from twisted.python import log
from twisted.internet import reactor
from esyslog import esapi

class SyslogTCPFactory(protocol.Factory):
    noisy = 0
    numberConnections = 0
    maxNumberConnections = 1024


class SyslogTCP(protocol.Protocol):

    esclient = None

    def connectionMade(self):
        self.factory.numberConnections += 1
        if self.factory.numberConnections > self.factory.maxNumberConnections:
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.factory.numberConnections -= 1

    def dataReceived(self, data):
        for log_item in SyslogProtocol.decode(data):
            log_item["host"] = self.transport.getPeer().host
            self.esclient.send(log_item)


class SyslogUDP(protocol.DatagramProtocol):

    esclient = None

    def datagramReceived(self, data, (host, port)):
        log.msg(data)
        for log_item in SyslogProtocol.decode(data):
            log_item["host"] = host
            self.esclient.send(log_item)


def run(config):
    host = config.server.host
    udp_port = config.server.get("udp_port",0)
    tcp_port = config.server.get("tcp_port",0)
    eslogger = esapi.EslogApi(config.elasticsearch)

    if udp_port > 0:
        udpapp = SyslogUDP()
        udpapp.esclient = eslogger
        reactor.listenUDP(udp_port, udpapp, interface=host)

    if tcp_port > 0:
        tcpapp = SyslogTCPFactory()
        tcpapp.esclient = eslogger
        tcpapp.protocol = SyslogTCP
        reactor.listenTCP(tcp_port, tcpapp, interface=host)

    reactor.run()

def main():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--conf', type=str,default="esyslog.json",dest='conf',help='json config file')
    args =  parser.parse_args(sys.argv[1:])  

    if not os.path.exists(args.conf):
        print 'config file not exists'
        sys.exit(1)

    run(iconfig.find_config(args.conf))


if __name__ == '__main__':
    main()











