#!/usr/bin/env python3

from hashlib import sha256 as H
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

PORT = 8091
FLAG = "SUCCESS"  # CHANGEME
WELCOME = """How do you brew your coffee?
Some people like pour-overs, others prefer the aeropress..
I, for one, like to use SHA256. Can you give me the right ingredients?
""".encode('utf-8')


def test(s):
    return 'c0ffee' in s or 'c0ff33' in s or 'c0ffe3' in s or 'c0ff3e' in s


class SHAke(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(WELCOME)

    def dataReceived(self, data):
        h = H(data.strip()).hexdigest()
        if test(h):
            self.transport.write(
                "Thanks for the c0ff33! \
Here you go: {}\n".format(FLAG).encode('utf-8')
            )
        else:
            self.transport.write(
                "I can\'t digest {}! \
There\'s no coffee!\n".format(h).encode('utf-8')
            )


class SHAkeFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SHAke()


def main(port):
    """ MUST use IPv4 to connect. Sorry """
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(SHAkeFactory())
    reactor.run()


if __name__ == '__main__':
    main(PORT)
