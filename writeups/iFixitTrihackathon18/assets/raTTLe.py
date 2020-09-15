#!/usr/bin/env python3

from os import urandom
from time import sleep
from base64 import b64encode
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

PORT = 8092
FLAG = b"SUCCESS"  # CHANGEME
WELCOME = """Ticking away the moments that make up a dull day
Fritter and waste the hours in an off-hand way
Kicking around town
Waiting for someone or something to show you the flag
""".encode('utf-8')
PASSWORD = b64encode(urandom(16))

class raTTLe(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(WELCOME)

    def dataReceived(self, data):
        for i in range(min(len(data), len(PASSWORD))):
            if data[i] == PASSWORD[i]:
                sleep(0.3)
                continue
            else:
                self.transport.write(b"Nope.\n")
                return
        self.transport.write(b"Congrats! " + FLAG + b"\n")
        self.transport.loseConnection()


class raTTLeFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return raTTLe()


def main(port):
    """ MUST use IPv4 to connect. Sorry """
    print(PASSWORD)
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(raTTLeFactory())
    reactor.run()


if __name__ == '__main__':
    main(PORT)
