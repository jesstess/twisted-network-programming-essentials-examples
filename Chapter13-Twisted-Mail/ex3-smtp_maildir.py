import os
import sys

from email.Header import Header
from zope.interface import implements

from twisted.internet import reactor
from twisted.mail import smtp, maildir
from twisted.python import log

class LocalMessageDelivery(object):
    implements(smtp.IMessageDelivery)

    def __init__(self, protocol, baseDir):
        self.protocol = protocol
        self.baseDir = baseDir

    def receivedHeader(self, helo, origin, recipients):
        clientHostname, clientIP = helo
        myHostname = self.protocol.transport.getHost().host
        headerValue = "from %s by %s with ESMTP ; %s" % (
            clientHostname, myHostname, smtp.rfc822date())
        return "Received: %s" % Header(headerValue)

    def validateFrom(self, helo, origin):
        # Accept any sender.
        return origin

    def _getAddressDir(self, address):
        return os.path.join(self.baseDir, "%s" % address)

    def validateTo(self, user):
        # Accept recipients @localhost.
        if user.dest.domain == "localhost":
            return lambda: MaildirMessage(
                self._getAddressDir(str(user.dest)))
        else:
            log.msg("Received email for invalid recipient %s" % user)
            raise smtp.SMTPBadRcpt(user)

class MaildirMessage(object):
    implements(smtp.IMessage)

    def __init__(self, userDir):
        if not os.path.exists(userDir):
            os.mkdir(userDir)
        inboxDir = os.path.join(userDir, 'Inbox')
        self.mailbox = maildir.MaildirMailbox(inboxDir)
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line)

    def eomReceived(self):
        print "New message received."
        self.lines.append('') # Add a trailing newline.
        messageData = '\n'.join(self.lines)
        return self.mailbox.appendMessage(messageData)

    def connectionLost(self):
        print "Connection lost unexpectedly!"
        # Unexpected loss of connection; don't save.
        del(self.lines)

class LocalSMTPFactory(smtp.SMTPFactory):
    def __init__(self, baseDir):
        self.baseDir = baseDir

    def buildProtocol(self, addr):
        proto = smtp.ESMTP()
        proto.delivery = LocalMessageDelivery(proto, self.baseDir)
        return proto

log.startLogging(sys.stdout)

reactor.listenTCP(2500, LocalSMTPFactory("/tmp/mail"))
reactor.run()
