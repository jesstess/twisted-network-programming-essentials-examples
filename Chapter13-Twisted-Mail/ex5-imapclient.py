from twisted.internet import protocol, reactor
from twisted.mail import imap4

USERNAME = 'recipient@localhost'
PASSWORD = 'pass'

class IMAP4LocalClient(imap4.IMAP4Client):
    def connectionMade(self):
        self.login(USERNAME, PASSWORD).addCallbacks(
            self._getMessages, self._ebLogin)

    def connectionLost(self, reason):
        reactor.stop()

    def _ebLogin(self, result):
        print result
        self.transport.loseConnection()

    def _getMessages(self, result):
        return self.list("", "*").addCallback(self._cbPickMailbox)

    def _cbPickMailbox(self, result):
        mbox = filter(lambda x: "Inbox" in x[2], result)[0][2]
        return self.select(mbox).addCallback(self._cbExamineMbox)

    def _cbExamineMbox(self, result):
        return self.fetchMessage('1:*', uid=False).addCallback(self._cbFetchMessages)

    def _cbFetchMessages(self, result):
        for seq, message in result.iteritems():
            print seq, message["RFC822"]

        return self.logout()

class IMAP4ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return IMAP4LocalClient()

    def clientConnectionFailed(self, connector, reason):
        print reason
        reactor.stop()

reactor.connectTCP("localhost", 1430, IMAP4ClientFactory())
reactor.run()
