from twisted.internet import protocol, reactor

class EchoProcessProtocol(protocol.ProcessProtocol):
    def connectionMade(self):
        print "connectionMade called"
        reactor.callLater(10, self.terminateProcess)

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
        reactor.stop()

pp = EchoProcessProtocol()

commandAndArgs = ["twistd", "-ny", "echo_server.tac"]
reactor.spawnProcess(pp, commandAndArgs[0], args=commandAndArgs)
reactor.run()
