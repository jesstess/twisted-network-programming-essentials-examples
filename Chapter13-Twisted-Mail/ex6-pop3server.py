import os
import sys
from zope.interface import implements

from twisted.cred import checkers, portal
from twisted.internet import protocol, reactor
from twisted.mail import maildir, pop3
from twisted.python import log

class UserInbox(maildir.MaildirMailbox):
    def __init__(self, userDir):
        inboxDir = os.path.join(userDir, 'Inbox')
        maildir.MaildirMailbox.__init__(self, inboxDir)

class POP3ServerProtocol(pop3.POP3):
    def lineReceived(self, line):
        print "CLIENT:", line
        pop3.POP3.lineReceived(self, line)

    def sendLine(self, line):
        print "SERVER:", line
        pop3.POP3.sendLine(self, line)

class POP3Factory(protocol.Factory):
    def __init__(self, portal):
        self.portal = portal

    def buildProtocol(self, address):
        proto = POP3ServerProtocol()
        proto.portal = self.portal
        return proto

class MailUserRealm(object):
    implements(portal.IRealm)

    def __init__(self, baseDir):
      self.baseDir = baseDir

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pop3.IMailbox not in interfaces:
            raise NotImplementedError(
                "This realm only supports the pop3.IMailbox interface.")

        userDir = os.path.join(self.baseDir, avatarId)
        avatar = UserInbox(userDir)
        return pop3.IMailbox, avatar, lambda: None

log.startLogging(sys.stdout)

dataDir = sys.argv[1]

portal = portal.Portal(MailUserRealm(dataDir))
checker = checkers.FilePasswordDB(os.path.join(dataDir, 'passwords.txt'))
portal.registerChecker(checker)

reactor.listenTCP(1100, POP3Factory(portal))
reactor.run()
