import email
import os
import random
from StringIO import StringIO
import sys
from zope.interface import implements

from twisted.cred import checkers, portal
from twisted.internet import protocol, reactor
from twisted.mail import imap4, maildir
from twisted.python import log

class IMAPUserAccount(object):
    implements(imap4.IAccount)

    def __init__(self, userDir):
        self.dir = userDir

    def _getMailbox(self, path):
        fullPath = os.path.join(self.dir, path)
        if not os.path.exists(fullPath):
            raise KeyError, "No such mailbox"
        return IMAPMailbox(fullPath)

    def listMailboxes(self, ref, wildcard):
        for box in os.listdir(self.dir):
            yield box, self._getMailbox(box)

    def select(self, path, rw=False):
        return self._getMailbox(path)

class ExtendedMaildir(maildir.MaildirMailbox):
    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i]

class IMAPMailbox(object):
    implements(imap4.IMailbox)

    def __init__(self, path):
        self.maildir = ExtendedMaildir(path)
        self.listeners = []
        self.uniqueValidityIdentifier = random.randint(1000000, 9999999)

    def getHierarchicalDelimiter(self):
        return "."

    def getFlags(self):
        return []

    def getMessageCount(self):
        return len(self.maildir)

    def getRecentCount(self):
        return 0

    def isWriteable(self):
        return False

    def getUIDValidity(self):
        return self.uniqueValidityIdentifier

    def _seqMessageSetToSeqDict(self, messageSet):
        if not messageSet.last:
            messageSet.last = self.getMessageCount()

        seqMap = {}
        for messageNum in messageSet:
            if messageNum >= 0 and messageNum <= self.getMessageCount():
                seqMap[messageNum] = self.maildir[messageNum - 1]
        return seqMap

    def fetch(self, messages, uid):
        if uid:
            raise NotImplementedError("This server only supports lookup by sequence number")

        messagesToFetch = self._seqMessageSetToSeqDict(messages)
        for seq, filename in messagesToFetch.items():
            yield seq, MaildirMessage(file(filename).read())

    def addListener(self, listener):
        self.listeners.append(listener)

    def removeListener(self, listener):
        self.listeners.remove(listener)

class MaildirMessage(object):
    implements(imap4.IMessage)

    def __init__(self, messageData):
        self.message = email.message_from_string(messageData)

    def getHeaders(self, negate, *names):
        if not names:
            names = self.message.keys()

        headers = {}
        if negate:
            for header in self.message.keys():
                if header.upper() not in names:
                    headers[header.lower()] = self.message.get(header, '')
        else:
            for name in names:
                headers[name.lower()] = self.message.get(name, '')

        return headers

    def getBodyFile(self):
        return StringIO(self.message.get_payload())

    def isMultipart(self):
        return self.message.is_multipart()

class MailUserRealm(object):
    implements(portal.IRealm)

    def __init__(self, baseDir):
      self.baseDir = baseDir

    def requestAvatar(self, avatarId, mind, *interfaces):
        if imap4.IAccount not in interfaces:
            raise NotImplementedError(
                "This realm only supports the imap4.IAccount interface.")

        userDir = os.path.join(self.baseDir, avatarId)
        avatar = IMAPUserAccount(userDir)
        return imap4.IAccount, avatar, lambda: None

class IMAPServerProtocol(imap4.IMAP4Server):
  def lineReceived(self, line):
      print "CLIENT:", line
      imap4.IMAP4Server.lineReceived(self, line)

  def sendLine(self, line):
      imap4.IMAP4Server.sendLine(self, line)
      print "SERVER:", line

class IMAPFactory(protocol.Factory):
    def __init__(self, portal):
        self.portal = portal

    def buildProtocol(self, addr):
        proto = IMAPServerProtocol()
        proto.portal = portal
        return proto

log.startLogging(sys.stdout)

dataDir = sys.argv[1]

portal = portal.Portal(MailUserRealm(dataDir))
checker = checkers.FilePasswordDB(os.path.join(dataDir, 'passwords.txt'))
portal.registerChecker(checker)

reactor.listenTCP(1430, IMAPFactory(portal))
reactor.run()
