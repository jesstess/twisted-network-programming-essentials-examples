from twisted.internet import protocol, reactor

class EchoProcessProtocol(protocol.ProcessProtocol):
    def __init__(self, reactor):
        self.reactor = reactor

    def connectionMade(self):
        print "connectionMade called"
        self.reactor.callLater(10, self.terminateProcess)

    def terminateProcess(self):
        self.transport.signalProcess('TERM')

    def outReceived(self, data):
        print "outReceived called with %d bytes of data:\n%s" % (
            len(data), data)

    def errReceived(self, data):
        print "errReceived called with %d bytes of data:\n%s" % (
            len(data), data)

    def inConnectionLost(self):
        print "inConnectionLost called, stdin closed."

    def outConnectionLost(self):
        print "outConnectionLost called, stdout closed."

    def errConnectionLost(self):
        print "errConnectionLost called, stderr closed."

    def processExited(self, reason):
        print "processExited called with status %d" % (
            reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded called with status %d" % (
            reason.value.exitCode,)
        print "All FDs are now closed, and the process has been reaped."
        self.reactor.stop()
