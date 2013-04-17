from twisted.mail import pop3client
from twisted.internet import reactor, protocol, defer
from cStringIO import StringIO
import email

USERNAME = 'recipient@localhost'
PASSWORD = 'pass'

class POP3LocalClient(pop3client.POP3Client):
    def serverGreeting(self, greeting):
        pop3client.POP3Client.serverGreeting(self, greeting)
        login = self.login(USERNAME, PASSWORD).addCallbacks(
            self._loggedIn, self._ebLogin)

    def connectionLost(self, reason):
        reactor.stop()

    def _loggedIn(self, result):
        return self.listSize().addCallback(self._gotMessageSizes)

    def _ebLogin(self, result):
        print result
        self.transport.loseConnection()

    def _gotMessageSizes(self, sizes):
        retreivers = []
        for i in range(len(sizes)):
            retreivers.append(self.retrieve(i).addCallback(
                self._gotMessageLines))
        return defer.DeferredList(retreivers).addCallback(
            self._finished)

    def _gotMessageLines(self, messageLines):
        for line in messageLines:
            print line

    def _finished(self, downloadResults):
        return self.quit()

class POP3ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return POP3LocalClient()

    def clientConnectionFailed(self, connector, reason):
        print reason
        reactor.stop()

reactor.connectTCP("localhost", 1100, POP3ClientFactory())
reactor.run()
