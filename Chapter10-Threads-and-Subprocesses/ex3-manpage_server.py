import sys

from twisted.internet import protocol, utils, reactor
from twisted.protocols.basic import LineReceiver
from twisted.python import log

class RunCommand(LineReceiver):
    def lineReceived(self, line):
        log.msg("Man pages requested for: %s" % (line,))
        commands = line.strip().split(" ")
        output = utils.getProcessOutput("man", commands, errortoo=True)
        output.addCallback(self.writeSuccessResponse)

    def writeSuccessResponse(self, result):
        self.transport.write(result)
        self.transport.loseConnection()

class RunCommandFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RunCommand()

log.startLogging(sys.stdout)
reactor.listenTCP(8000, RunCommandFactory())
reactor.run()
