import time

from twisted.internet import reactor, threads
from twisted.internet.task import LoopingCall

def blockingApiCall(arg):
    time.sleep(1)
    return arg

def nonblockingCall(arg):
    print arg

def printResult(result):
    print result

def finish(result):
    reactor.stop()

d = threads.deferToThread(blockingApiCall, "Goose")
d.addCallback(printResult)
d.addCallback(finish)

LoopingCall(nonblockingCall, "Duck").start(.25)

reactor.run()
