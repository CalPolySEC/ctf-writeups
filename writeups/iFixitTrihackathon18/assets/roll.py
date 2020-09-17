#!/usr/bin/env python3

from random import random
from entropy import shannon_entropy as entropy
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

PORT = 8093
FLAG = b"SUCCESS"  # CHANGEME
DIFFICULTY = 0.69
WELCOME = """They say not to roll your own crypto.
Today you're going to break that rule.

Give me three numbers like X, Y, Z

I'll use these numbers to make an encryption function
This encryption function takes each letter c and
applies (X*c + Y) % Z to the character c i times, where i
is the index of c in the input string.

You can't just give me any three numbers, though. They have to pass the test!

I'll put a predictable string like "AAAAAAAA..." through your encryption
function. The output has to look random enough.

What's random enough? Don't ask me. Shannon might be able to tell you...
""".encode('utf-8')

def mapper(a, b, c):
    x = 1
    out = ""
    for i in range(48):
        char = ord("A")
        for j in range(x):
            char = (a*char+b) % c
        out += chr(min(max(char, 65), 122))
        x += 1
    return out

class roll(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(WELCOME)

    def dataReceived(self, data):
        try:
            a, b, c = data.decode('utf-8').split(",")
            a = int(a)
            b = int(b)
            c = int(c)
        except:
            self.transport.write(b"Bad format, try again.\n")
            return
        if entropy(mapper(a, b, c)) > DIFFICULTY:
            self.transport.write(b"Congrats! " + FLAG + b"\n")
        else:
            self.transport.write(b"Nope.\n")


class rollFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return roll()


def test():
    """ brute force an answer
    """
    from random import randrange
    for a in sorted(range(123), key=lambda u: random()):
        for b in sorted(range(123), key=lambda u: random()):
            for c in sorted(range(1, 123), key=lambda u: random()):
                if entropy(mapper(a, b, c)) > DIFFICULTY:
                    print(a, b, c)
                    print(mapper(a, b, c))
                    print(entropy(mapper(a, b, c)))
                    break
        print(a)


def main(port):
    """ MUST use IPv4 to connect. Sorry """
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(rollFactory())
    reactor.run()


if __name__ == '__main__':
    main(PORT)
