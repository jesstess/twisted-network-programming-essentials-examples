import sys
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer

from zope.interface import implements

class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class ResourcePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, data):
        print data

    def connectionLost(self, reason):
        self.finished.callback(None)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished

def printError(failure):
    print >>sys.stderr, failure

def stop(result):
    reactor.stop()

if len(sys.argv) != 3:
    print >>sys.stderr, "Usage: python post_resource.py URL 'POST DATA'"
    exit(1)

agent = Agent(reactor)
body = StringProducer(sys.argv[2])
d = agent.request('POST', sys.argv[1], bodyProducer=body)
d.addCallbacks(printResource, printError)
d.addBoth(stop)

reactor.run()
